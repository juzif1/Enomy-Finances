
% rebase('base.tpl', title='Investment Results', include_js=False)

<h2>Investment Projection</h2>

<table style="width:100%; border-collapse:collapse; margin-top:20px;">
    <thead>
        <tr>
            <th>Years</th>
            <th>Min Value (£)</th>
            <th>Max Value (£)</th>
            <th>Min Profit (£)</th>
            <th>Max Profit (£)</th>
            <th>Fees (£)</th>
            <th>Min Tax (£)</th>
            <th>Max Tax (£)</th>
        </tr>
    </thead>
    <tbody>
        % for years, r in results.items():
        <tr>
            <td>{{years}}</td>
            <td>{{r["min"]}}</td>
            <td>{{r["max"]}}</td>
            <td>{{r["profit_min"]}}</td>
            <td>{{r["profit_max"]}}</td>
            <td>{{r["fees"]}}</td>
            <td>{{r["tax_min"]}}</td>
            <td>{{r["tax_max"]}}</td>
        </tr>
        % end
    </tbody>
</table>

<hr style="margin:40px 0;">

<h3>Projected Maximum Value</h3>

<canvas id="investmentChart" height="120"></canvas>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const data = {
    labels: ['1 Year', '5 Years', '10 Years'],
    datasets: [{
        label: 'Max Investment Value (£)',
        data: [
            {{results[1]["max"]}},
            {{results[5]["max"]}},
            {{results[10]["max"]}}
        ]
    }]
};

new Chart(document.getElementById('investmentChart'), {
    type: 'bar',
    data: data,
    options: {
        responsive: true,
        plugins: {
            legend: { display: false }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
</script>

<div style="text-align:center; margin-top:30px;">
    <a href="/investment">New Calculation</a> |
    <a href="/">Home</a>
</div>
