% rebase('base.tpl', title='Currency Conversion', include_js=True)

<form method="post">
    <label>Amount (£)</label>
    <input type="number" name="amount" required>

    <label>From</label>
    <select name="source_currency">
        <option>GBP</option>
        <option>USD</option>
        <option>EUR</option>
        <option>BRL</option>
        <option>JPY</option>
        <option>TRY</option>
    </select>

    <label>To</label>
    <select name="target_currency">
        <option>GBP</option>
        <option>USD</option>
        <option>EUR</option>
        <option>BRL</option>
        <option>JPY</option>
        <option>TRY</option>
    </select>

    <button type="submit">Convert</button>
</form>
