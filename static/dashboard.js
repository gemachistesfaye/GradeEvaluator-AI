document.addEventListener('DOMContentLoaded', () => {
    // Show Loading Overlay on form submit
    const evaluateForm = document.getElementById('evaluateForm');
    if (evaluateForm) {
        evaluateForm.addEventListener('submit', function() {
            document.getElementById('loadingOverlay').classList.add('active');
        });
    }

    // Initialize Chatbot if grades exist
    const gradesDataEl = document.getElementById('grades-data');
    let gradesData = [];
    let currentGradeId = null;

    if (gradesDataEl) {
        try {
            gradesData = JSON.parse(gradesDataEl.textContent);
            if (gradesData && gradesData.length > 0) {
                currentGradeId = gradesData[0].id;
            }
        } catch (e) {
            console.error("Failed to parse grades data", e);
        }
    }

    let conversation = [];
    let chatOpen = false;

    if (currentGradeId !== null) {
        conversation.push({
            role: 'assistant',
            content: "Hi there! I'm GradeBot. What would you like to know about this grade?"
        });
    } else {
        conversation.push({
            role: 'assistant',
            content: "Hi there! I'm GradeBot. Add some grades so we can analyze them together!"
        });
        const initialMsg = document.querySelector('.chat-msg-bot');
        if (initialMsg) {
            initialMsg.textContent = "Hi there! I'm GradeBot. Add some grades so we can analyze them together!";
        }
    }

    const chatWindow = document.getElementById('advisorPanel');
    const chatFab = document.getElementById('advisorBtn');
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    
    // Elements for dynamic updates
    const botGradeInfo = document.getElementById('botGradeInfo');

    window.toggleChat = function() {
        if (!chatWindow || !chatFab) return;
        chatOpen = !chatOpen;
        chatWindow.classList.toggle('open', chatOpen);
        chatFab.innerHTML = chatOpen 
            ? '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>' 
            : '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2z"/></svg>';
        if (chatOpen) scrollToBottom();
    };

    function scrollToBottom() {
        if (chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addMessage(content, role) {
        const div = document.createElement('div');
        div.className = 'chat-msg ' + (role === 'user' ? 'chat-msg-user' : 'chat-msg-bot');
        if (role === 'user') {
            div.textContent = content;
        } else {
            // Markdown: **bold**, *italic*, ~small~
            let formatted = content
                .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.+?)\*/g, '<em>$1</em>')
                .replace(/~(.+?)~/g, '<small>$1</small>');
            div.innerHTML = formatted;
        }
        chatMessages.appendChild(div);
        scrollToBottom();
    }

    function addTyping() {
        const div = document.createElement('div');
        div.className = 'chat-msg chat-msg-bot';
        div.id = 'typingIndicator';
        div.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
        chatMessages.appendChild(div);
        scrollToBottom();
    }

    function removeTyping() {
        const t = document.getElementById('typingIndicator');
        if (t) t.remove();
    }

    window.sendChat = async function() {
        const msg = chatInput.value.trim();
        if (!msg) return;

        chatInput.value = '';
        sendBtn.disabled = true;

        addMessage(msg, 'user');
        conversation.push({ role: 'user', content: msg });
        addTyping();

        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: msg,
                    grade_id: currentGradeId || null,
                    conversation: conversation
                })
            });
            const data = await res.json();
            removeTyping();
            
            const reply = data.reply || "Sorry, I couldn't process that.";
            addMessage(reply, 'assistant');
            conversation.push({ role: 'assistant', content: reply });
        } catch(e) {
            removeTyping();
            addMessage('Sorry, something went wrong. Try again!', 'assistant');
        }

        sendBtn.disabled = false;
        chatInput.focus();
    };

    window.quickSend = function(msg) {
        if (!chatOpen) toggleChat();
        setTimeout(() => {
            chatInput.value = msg;
            sendChat();
        }, 300);
    };

    window.switchGrade = function(gradeId) {
        currentGradeId = parseInt(gradeId);
        conversation = [];
        chatMessages.innerHTML = '';
        
        // Find new grade to update header
        const newGrade = gradesData.find(g => g.id === currentGradeId);
        if (newGrade) {
            botGradeInfo.textContent = `${newGrade.subject} · ${newGrade.score}/100 · ${newGrade.letter_grade}`;
        }

        addMessage('Switched! Ask me anything about this grade.', 'assistant');
        conversation.push({ role: 'assistant', content: 'Switched grade context!' });
    };
    
    // Handle Enter key
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendChat();
    });
});
