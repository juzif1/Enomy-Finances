
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const amountInput = form.querySelector('input[name="amount"]');
            const lumpInput = form.querySelector('input[name="lump_sum"]');
            const monthlyInput = form.querySelector('input[name="monthly_investment"]');

            // Currency validation
            if (amountInput) {
                const value = parseFloat(amountInput.value);
                if (value < 300 || value > 5000) {
                    alert("Amount must be between £300 and £5000");
                    e.preventDefault();
                    return;
                }
            }

            // Investment validation
            if (monthlyInput && parseFloat(monthlyInput.value) < 0) {
                alert("Monthly investment cannot be negative");
                e.preventDefault();
                return;
            }

            if (lumpInput && parseFloat(lumpInput.value) < 0) {
                alert("Lump sum cannot be negative");
                e.preventDefault();
                return;
            }
        });
    });
});
