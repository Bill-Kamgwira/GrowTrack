document.addEventListener('DOMContentLoaded', () => {
    const managementTypeSelect = document.getElementById('management_type');
    const managementDetailsContainer = document.getElementById('management-details');
                                                                
    console.log('DOMContentLoaded: Elements accessed:', managementTypeSelect, managementDetailsContainer);

    managementTypeSelect.addEventListener('change', () => {
        console.log('Select box changed');
        const selectedType = managementTypeSelect.value;
        console.log('Selected type:', selectedType);

        managementDetailsContainer.innerHTML = ''; // Clear previous content 

    // Dynamically create form fields based on selected type
    if (selectedType === 'fertilization') {
        const fertilizerTypeLabel = document.createElement('label');
        fertilizerTypeLabel.textContent = 'Fertilizer Type:';

        const fertilizerTypeInput = document.createElement('input');
        fertilizerTypeInput.type = 'text';
        fertilizerTypeInput.name = 'fertilizer_type';
        fertilizerTypeInput.id = 'fertilizer_type';

        const fertilizerAmountLabel = document.createElement('label');
        fertilizerAmountLabel.textContent = 'Amount applied:';

        const fertilizerAmountInput = document.createElement('input');
        fertilizerAmountInput.type = 'number';
        fertilizerAmountInput.name = 'fertilizer_amount';
        fertilizerAmountInput.id = 'fertilizer_amount';

        const fertilizerDateLabel = document.createElement('label');
        fertilizerDateLabel.textContent = 'Date Applied:';

        const fertilizerDateInput = document.createElement('input');
        fertilizerDateInput.type = 'date';
        fertilizerDateInput.name = 'fertilizer_date';
        fertilizerDateInput.id = 'fertilizer_date';

        managementDetailsContainer.appendChild(fertilizerTypeLabel);
        managementDetailsContainer.appendChild(fertilizerTypeInput);

        managementDetailsContainer.appendChild(fertilizerAmountLabel);
        managementDetailsContainer.appendChild(fertilizerAmountInput);

        managementDetailsContainer.appendChild(fertilizerDateLabel);
        managementDetailsContainer.appendChild(fertilizerDateInput);
        
    } else if (selectedType === 'irrigation') {

        const irrigationTypeLabel = document.createElement('label');
        irrigationTypeLabel.textContent = 'Irrigation Type:';

        const irrigationTypeInput = document.createElement('input');
        irrigationTypeInput.type = 'text';
        irrigationTypeInput.name = 'irrigation_type';
        irrigationTypeInput.id = 'irrigation_type';

        const irrigationAmountLabel = document.createElement('label');
        irrigationAmountLabel.textContent = 'Amount applied:';

        const irrigationAmountInput = document.createElement('input');
        irrigationAmountInput.type = 'number';
        irrigationAmountInput.name = 'irrigation_amount';
        irrigationAmountInput.id = 'irrigation_amount';

        const irrigationDateLabel = document.createElement('label');
        irrigationDateLabel.textContent = 'Date Applied:';

        const irrigationDateInput = document.createElement('input');
        irrigationDateInput.type = 'date';
        irrigationDateInput.name = 'irrigation_date';
        irrigationDateInput.id = 'irrigation_date';

        managementDetailsContainer.appendChild(irrigationTypeLabel);
        managementDetailsContainer.appendChild(irrigationTypeInput);

        managementDetailsContainer.appendChild(irrigationAmountLabel);
        managementDetailsContainer.appendChild(irrigationAmountInput);

        managementDetailsContainer.appendChild(irrigationDateLabel);
        managementDetailsContainer.appendChild(irrigationDateInput);

    } else if (selectedType === 'pest_control') {

        const controlTypeLabel = document.createElement('label');
        controlTypeLabel.textContent = 'Control Type:';

        const controlTypeInput = document.createElement('input');
        controlTypeInput.type = 'text';
        controlTypeInput.name = 'control_type';
        controlTypeInput.id = 'control_type';

        const controlAmountLabel = document.createElement('label');
        controlAmountLabel.textContent = 'Amount applied:';

        const controlAmountInput = document.createElement('input');
        controlAmountInput.type = 'number';
        controlAmountInput.name = 'control_amount';
        controlAmountInput.id = 'control_amount';

        const controlDateLabel = document.createElement('label');
        controlDateLabel.textContent = 'Date Applied:';

        const controlDateInput = document.createElement('input');
        controlDateInput.type = 'date';
        controlDateInput.name = 'control_date';
        controlDateInput.id = 'control_date';

        managementDetailsContainer.appendChild(controlTypeLabel);
        managementDetailsContainer.appendChild(controlTypeInput);

        managementDetailsContainer.appendChild(controlAmountLabel);
        managementDetailsContainer.appendChild(controlAmountInput);

        managementDetailsContainer.appendChild(controlDateLabel);
        managementDetailsContainer.appendChild(controlDateInput);

    } else if (selectedType === 'weeding') {

       const weedingTypeLabel = document.createElement('label');
       weedingTypeLabel.textContent = 'Weeding Method:';

        const weedingTypeInput = document.createElement('input');
        weedingTypeInput.type = 'text';
        weedingTypeInput.name = 'weeding_method';
        weedingTypeInput.id = 'weeding_method';

        const weedingDateLabel = document.createElement('label');
        weedingDateLabel.textContent = 'Date Weeded:';

        const weedingDateInput = document.createElement('input');
        weedingDateInput.type = 'date';
        weedingDateInput.name = 'weeding_date';
        weedingDateInput.id = 'weeding_date';

        managementDetailsContainer.appendChild(weedingTypeLabel);
        managementDetailsContainer.appendChild(weedingTypeInput);

        managementDetailsContainer.appendChild(weedingDateLabel);
        managementDetailsContainer.appendChild(weedingDateInput);

    } else if (selectedType === 'labor') {
        const taskCompleteLabel = document.createElement('label');
        taskCompleteLabel.textContent = 'Task Completed:';

        const taskCompletedInput = document.createElement('input');
        taskCompletedInput.type = 'text';
        taskCompletedInput.name = 'tasks_completed';
        taskCompletedInput.id = 'tasks_completed';

        const hoursAccruedLabel = document.createElement('label');
        hoursAccruedLabel.textContent = 'Hours taken:';

        const hoursAccruedInput = document.createElement('input');
        hoursAccruedInput.type = 'number';
        hoursAccruedInput.name = 'hours_accrued';
        hoursAccruedInput.id = 'hours_accrued';

        const taskDateLabel = document.createElement('label');
        taskDateLabel.textContent = 'Date:';

        const taskDateInput = document.createElement('input');
        taskDateInput.type = 'date';
        taskDateInput.name = 'labour_date';
        taskDateInput.id = 'labour_date';

        managementDetailsContainer.appendChild(taskCompleteLabel);
        managementDetailsContainer.appendChild(taskCompletedInput);

        managementDetailsContainer.appendChild(hoursAccruedLabel);
        managementDetailsContainer.appendChild(hoursAccruedInput);

        managementDetailsContainer.appendChild(taskDateLabel);
        managementDetailsContainer.appendChild(taskDateInput);

    }});
    
    function validateForm() {
        let isValid = true;
      
        const selectedType = document.getElementById('management_type').value;
      
    
      
        if (selectedType === 'fertilization') {
          const fertilizerAmountInput = document.getElementById('fertilizer_amount');
          const fertilizerAmount = parseFloat(fertilizerAmountInput.value);
          if (isNaN(fertilizerAmount) || fertilizerAmount <= 0) {
            alert('Please enter a valid fertilizer amount (positive number).');
            isValid = false;
            fertilizerAmountInput.focus(); // Set focus on the invalid input
          }
        } else if (selectedType === 'irrigation') {
          const irrigationAmountInput = document.getElementById('irrigation_amount');
          const irrigationAmount = parseFloat(irrigationAmountInput.value);
          if (isNaN(irrigationAmount) || irrigationAmount <= 0) {
            alert('Please enter a valid irrigation amount (positive number).');
            isValid = false;
            irrigationAmountInput.focus();
          }
        } else if (selectedType === 'pest_control') {
          const controlAmountInput = document.getElementById('control_amount');
          const controlAmount = parseFloat(controlAmountInput.value);
          if (isNaN(controlAmount) || controlAmount <= 0) {
            alert('Please enter a valid control amount (positive number).');
            isValid = false;
            controlAmountInput.focus();
          }
        } else if (selectedType === 'labor') {
          const hoursAccruedInput = document.getElementById('hours_accrued');
          const hoursAccrued = parseFloat(hoursAccruedInput.value);
          if (isNaN(hoursAccrued) || hoursAccrued <= 0) {
            alert('Please enter valid hours accrued (positive number).');
            isValid = false;
            hoursAccruedInput.focus();
          }
        }
      
        return isValid;
      }

    const form = document.querySelector('form');
    form.addEventListener('submit', (event) => {
        if (!validateForm()) {
      event.preventDefault(); // Prevent form submission if validation fails
        }
    });
      
    });
