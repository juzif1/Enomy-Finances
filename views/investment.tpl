
% rebase('base.tpl', title='Investment Calculator', include_js=True)

<form method="post">
    <label>Investment Type</label>
    <select name="investment_type">
        <option>Basic Savings Plan</option>
        <option>Savings Plan Plus</option>
        <option>Managed Stock Investments</option>
    </select>

    <label>Lump Sum (£)</label>
    <input type="number" name="lump_sum">

    <label>Monthly (£)</label>
    <input type="number" name="monthly_investment">

    <label>Years</label>
    <input type="number" name="years">

    <button type="submit">Calculate</button>
</form>
