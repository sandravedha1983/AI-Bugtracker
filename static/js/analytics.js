document.addEventListener('DOMContentLoaded', function () {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const chartTheme = isDark ? 'dark' : 'light';

    fetch('/api/analytics/summary')
        .then(response => response.json())
        .then(data => {
            // Update Stats
            const totalBugs = Object.values(data.status).reduce((a, b) => a + b, 0);
            document.getElementById('totalBugs').innerText = totalBugs;
            
            const resolvedBugs = data.status['Resolved'] || 0;
            const resRate = totalBugs > 0 ? Math.round((resolvedBugs / totalBugs) * 100) : 0;
            document.getElementById('resRate').innerText = resRate + '%';
            document.getElementById('resRateBar').style.width = resRate + '%';
            
            const avgRes = data.resolution.data.filter(v => v > 0);
            const avgResVal = avgRes.length > 0 ? (avgRes.reduce((a, b) => a + b, 0) / avgRes.length).toFixed(1) : 0;
            document.getElementById('avgResTime').innerText = avgResVal + 'h';
            
            document.getElementById('aiPrecision').innerText = data.ai_stats.accuracy + '%';

            // 1. Trends Chart (Line)
            new ApexCharts(document.querySelector("#trendsChart"), {
                series: [{ name: 'Bugs Reported', data: data.trends.data }],
                chart: { type: 'area', height: 320, toolbar: { show: false }, theme: { mode: chartTheme } },
                colors: ['#6366f1'],
                fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.4, opacityTo: 0.1 } },
                dataLabels: { enabled: false },
                stroke: { curve: 'smooth', width: 3 },
                xaxis: { categories: data.trends.labels },
                yaxis: { labels: { formatter: (v) => Math.floor(v) } }
            }).render();

            // 2. Severity Chart (Donut)
            new ApexCharts(document.querySelector("#severityChart"), {
                series: Object.values(data.severity),
                chart: { type: 'donut', height: 320, theme: { mode: chartTheme } },
                labels: Object.keys(data.severity),
                colors: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981'],
                plotOptions: { pie: { donut: { size: '75%' } } },
                legend: { position: 'bottom' }
            }).render();

            // 3. Module Chart (Bar)
            new ApexCharts(document.querySelector("#moduleChart"), {
                series: [{ name: 'Bugs', data: Object.values(data.module) }],
                chart: { type: 'bar', height: 320, toolbar: { show: false }, theme: { mode: chartTheme } },
                colors: ['#8b5cf6'],
                plotOptions: { bar: { borderRadius: 6, columnWidth: '45%' } },
                xaxis: { categories: Object.keys(data.module) },
                dataLabels: { enabled: false }
            }).render();

            // 4. Developer Load (Radar or Horizontal Bar)
            new ApexCharts(document.querySelector("#devLoadChart"), {
                series: [{ name: 'Assigned Bugs', data: data.dev_load.data }],
                chart: { type: 'bar', height: 320, toolbar: { show: false }, theme: { mode: chartTheme } },
                colors: ['#10b981'],
                plotOptions: { bar: { borderRadius: 4, horizontal: true } },
                xaxis: { categories: data.dev_load.labels }
            }).render();
        });
});
