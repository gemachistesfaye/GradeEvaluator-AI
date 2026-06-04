
document.addEventListener("DOMContentLoaded", () => {
    if (typeof gradesData === 'undefined' || gradesData.length === 0) return;
    
    // Process data
    gradesData.reverse(); // oldest first for line chart
    const subjects = gradesData.map(g => g.subject);
    const scores = gradesData.map(g => g.score);
    const dates = gradesData.map(g => g.date);
    
    const dist = {A:0, B:0, C:0, D:0, F:0};
    gradesData.forEach(g => {
        const letter = g.letter_grade[0].toUpperCase();
        if(dist[letter] !== undefined) dist[letter]++;
    });

Chart.defaults.color = '#64748b'; // Slate-500
    Chart.defaults.font.family = "'Outfit', sans-serif";
    
    const gridConfig = { color: '#e2e8f0' }; // Slate-200

    // Group subjects and average their scores
    const subjectMap = {};
    gradesData.forEach(g => {
        if (!subjectMap[g.subject]) {
            subjectMap[g.subject] = { total: 0, count: 0 };
        }
        subjectMap[g.subject].total += g.score;
        subjectMap[g.subject].count += 1;
    });
    const groupedSubjects = Object.keys(subjectMap);
    const groupedScores = groupedSubjects.map(s => 
        parseFloat(
          (subjectMap[s].total / subjectMap[s].count).toFixed(1)
        )
    );

    // Bar Chart - Grades by subject
    new Chart(document.getElementById('barChart'), {
        type: 'bar',
        data: {
            labels: groupedSubjects,
            datasets: [{ 
                label: 'Score', 
                data: groupedScores, 
                backgroundColor: '#4f46e5', // Indigo 600
                borderRadius: 4
            }]
        },
        options: { scales: { y: { grid: gridConfig }, x: { grid: { display: false } } }, plugins: { legend: { display: false }, title: { display: true, text: 'Scores by Subject', color: '#0f172a', font: {size: 16, weight: 'bold'} } } }
    });

    // Pie Chart - Distribution
    new Chart(document.getElementById('pieChart'), {
        type: 'doughnut',
        data: {
            labels: Object.keys(dist),
            datasets: [{ 
                data: Object.values(dist), 
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#f97316', '#ef4444'],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: { plugins: { title: { display: true, text: 'Grade Distribution', color: '#0f172a', font: {size: 16, weight: 'bold'} } }, cutout: '75%' }
    });

    // Line Chart - Progress
    new Chart(document.getElementById('lineChart'), {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{ 
                label: 'Score Over Time', 
                data: scores, 
                borderColor: '#4f46e5', 
                backgroundColor: 'rgba(79, 70, 229, 0.1)',
                fill: true,
                tension: 0.3,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: '#4f46e5',
                pointBorderWidth: 2
            }]
        },
        options: { scales: { y: { grid: gridConfig }, x: { grid: { display: false } } }, plugins: { legend: { display: false }, title: { display: true, text: 'Progress Over Time', color: '#0f172a', font: {size: 16, weight: 'bold'} } } }
    });
});
