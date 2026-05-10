document.addEventListener('DOMContentLoaded', function () {
    // 1. PIE CHART - Bug Priority Distribution
    fetch('/api/analytics/priority')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('priorityChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(data),
                    datasets: [{
                        data: Object.values(data),
                        backgroundColor: [
                            '#ef4444', // High (Red)
                            '#f59e0b', // Medium (Amber)
                            '#10b981'  // Low (Emerald)
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
        });

    // 2. BAR CHART - Bug Status Overview
    fetch('/api/analytics/status')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('statusChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(data),
                    datasets: [{
                        label: 'Status Count',
                        data: Object.values(data),
                        backgroundColor: '#6366f1', // Indigo
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, grid: { display: false } },
                        x: { grid: { display: false } }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        });

    // 3. LINE CHART - Bugs Reported Over Time
    fetch('/api/analytics/trends')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('trendsChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Bugs Reported',
                        data: data.data,
                        borderColor: '#8b5cf6', // Violet
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointBackgroundColor: '#8b5cf6'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, stepSize: 1 },
                        x: { grid: { display: false } }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        });

    // 4. LINE CHART - Resolution Time Trend
    fetch('/api/analytics/resolution-trend')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('resolutionChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Avg Resolution Hours',
                        data: data.data,
                        borderColor: '#fbbf24', // Amber
                        backgroundColor: 'rgba(251, 191, 36, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointBackgroundColor: '#fbbf24'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Hours' } },
                        x: { grid: { display: false } }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        });

});
