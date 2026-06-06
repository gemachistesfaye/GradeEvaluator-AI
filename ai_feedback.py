import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
import markdown

SYSTEM_PROMPT = """You are GradeBot, a friendly and 
smart academic coach inside GradeEvaluator AI app.

You are talking to a student who just evaluated 
their grade. You know their result:
- Student Name: {student_name}
- Subject: {subject}
- Score: {score}/100
- Letter Grade: {letter_grade}
- GPA Points: {gpa_points}
- Date: {date}

GRADING SCALE:
A+ = 90-100 (4.0) | A = 85-89.9 (4.0)
A- = 80-84.9 (3.75) | B+ = 75-79.9 (3.5)
B = 70-74.9 (3.0) | B- = 65-69.9 (2.75)
C+ = 60-64.9 (2.5) | C = 55-59.9 (2.0)
C- = 50-54.9 (1.75) | D = 40-49.9 (1.5)
F (NG) = below 40 (0.0) — No Grade, very serious

YOUR PERSONALITY:
- Friendly, warm, encouraging like a real tutor
- Short responses — max 4-5 sentences per message
- Use the student's name naturally
- Use emojis occasionally but not too much
- Never write long walls of text
- Be conversational, not formal
- If F(NG): extra gentle and supportive

YOUR FIRST MESSAGE (when grade is submitted):
- 2-3 sentences max
- Acknowledge their grade warmly
- Ask ONE question to start the conversation
  Examples:
  "How did you feel about the exam?"
  "Which topic was hardest for you?"
  "Want some study tips for next time?"

FOLLOW-UP RESPONSES:
- Answer what the student asks directly
- Keep it short and actionable
- Offer to help with something specific
- Never repeat information already said

THINGS YOU CAN HELP WITH:
- Study tips for their specific subject
- Weekly study plan
- Free resources (real URLs only)
- GPA impact explanation
- Motivation and encouragement
- What to focus on before next exam
- How to improve from their current grade
"""

FIRST_MESSAGE_PROMPT = """Based on the student's 
grade result above, send your FIRST short greeting 
message (2-3 sentences max). 
Acknowledge their grade warmly and ask ONE 
follow-up question to start the conversation.
Do NOT use markdown headers or bullet points.
Write naturally like a chat message."""

def generate_first_message(student_name, subject, 
    score, letter_grade, gpa_points, date_str):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Hi! I'm GradeBot. Set your GEMINI_API_KEY to enable AI coaching."
    try:
        client = genai.Client(api_key=api_key)
        system = SYSTEM_PROMPT.format(
            student_name=student_name,
            subject=subject,
            score=score,
            letter_grade=letter_grade,
            gpa_points=gpa_points,
            date=date_str
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=system + "\n\n" + FIRST_MESSAGE_PROMPT
        )
        return response.text
    except Exception as e:
        return f"Hi {student_name}! Great job submitting your {subject} grade. I'm having trouble connecting right now. Try again shortly!"

GENERAL_SYSTEM_PROMPT = """You are GradeBot, a friendly and smart academic coach inside the GradeEvaluator AI app.

Student Name: {student_name}
{grade_context}

YOUR PERSONALITY:
- Friendly, warm, encouraging like a real tutor
- Short responses — max 4-5 sentences per message
- Use the student's name naturally
- Use emojis occasionally but not too much
- Never write long walls of text
- Be conversational, not formal

THINGS YOU CAN HELP WITH:
- Study tips and strategies
- Weekly study plans
- GPA explanations and calculations
- Academic motivation and encouragement
- How to improve grades
- Time management advice
- General academic questions

If the student asks about their specific grades or GPA analysis and they haven't calculated yet,
encourage them to use the dashboard to add their grades first, then come back for detailed analysis.
But ALWAYS answer general academic questions, study tips, and motivation regardless.
"""

def generate_chat_reply(student_name, subject,
    score, letter_grade, gpa_points,
    date_str, conversation_history, user_message, has_grades=False):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "GEMINI_API_KEY not set."
    try:
        client = genai.Client(api_key=api_key)

        if subject and score is not None:
            grade_context = f"""Current grade context:
- Subject: {subject}
- Score: {score}/100
- Letter Grade: {letter_grade}
- GPA Points: {gpa_points}
- Date: {date_str}

GRADING SCALE:
A+ = 90-100 (4.0) | A = 85-89.9 (4.0)
A- = 80-84.9 (3.75) | B+ = 75-79.9 (3.5)
B = 70-74.9 (3.0) | B- = 65-69.9 (2.75)
C+ = 60-64.9 (2.5) | C = 55-59.9 (2.0)
C- = 50-54.9 (1.75) | D = 40-49.9 (1.5)
F (NG) = below 40 (0.0) — No Grade"""
        elif has_grades:
            grade_context = "The student has recorded grades in the system. You can discuss them generally but for specific analysis, reference the dashboard."
        else:
            grade_context = "The student has not yet calculated any grades. Encourage them to add grades on the dashboard for detailed analysis, but still help with any general academic questions."

        system = GENERAL_SYSTEM_PROMPT.format(
            student_name=student_name,
            grade_context=grade_context
        )
        history_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}" for msg in conversation_history
        ])
        full_prompt = (
            system + "\n\n"
            "CONVERSATION SO FAR:\n" + history_text + "\n\n"
            "STUDENT: " + user_message + "\n\n"
            "Reply as GradeBot. Max 4-5 sentences. No markdown headers. Natural chat tone."
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        return "Sorry, I had trouble responding. Please try again!"

# Keep old function name for compatibility
def generate_ai_feedback(student_name, subject,
    score, letter_grade, gpa_points, date_str):
    return generate_first_message(
        student_name, subject, score,
        letter_grade, gpa_points, date_str)

def generate_semester_report(student_name, grades_summary, date_str):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "<p>GEMINI_API_KEY not set.</p>"
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""You are GradeBot, an expert academic advisor.
Student Name: {student_name}
Date: {date_str}
Grades Overview:
{grades_summary}

Please write a comprehensive academic report analyzing this student's overall performance.
- Use HTML formatting tags (<h3>, <strong>, <p>, <ul>, <li>).
- Do NOT use markdown symbols (no asterisks or hash symbols).
- Keep it encouraging but honest. Highlight strengths and suggest improvements.
"""
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return "<p>Sorry, I had trouble analyzing your semester. Please try again!</p>"
