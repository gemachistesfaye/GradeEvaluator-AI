
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

    // Bar Chart - Grades by subject
    new Chart(document.getElementById('barChart'), {
        type: 'bar',
        data: {
            labels: subjects,
            datasets: [{ label: 'Score', data: scores, backgroundColor: '#3498db' }]
        }
    });

    // Pie Chart - Distribution
    new Chart(document.getElementById('pieChart'), {
        type: 'pie',
        data: {
            labels: Object.keys(dist),
            datasets: [{ data: Object.values(dist), backgroundColor: ['#2ecc71', '#f1c40f', 'orange', '#e74c3c', 'darkred'] }]
        }
    });

    // Line Chart - Progress
    new Chart(document.getElementById('lineChart'), {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{ label: 'Score Over Time', data: scores, borderColor: '#e74c3c', fill: false }]
        }
    });
});
