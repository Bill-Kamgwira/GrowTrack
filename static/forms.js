document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');

  // Validate the form submission
  form.addEventListener('submit', (event) => {
      const selectedType = document.getElementById('management_type').value;
      const amountInput = document.getElementById('amount');
      const amount = parseFloat(amountInput.value);
      
      if (isNaN(amount) || amount <= 0) {
          alert('Please enter a valid amount (positive number).');
          event.preventDefault();
          amountInput.focus();
      }
  });
});
