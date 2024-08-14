const tabs = document.querySelectorAll('.tabs li a');
const tabContent = document.querySelectorAll('.tab-pane');



tabs.forEach(tab => {
  tab.addEventListener('click', (e) => {
    e.preventDefault();
    const target = e.target.getAttribute('href');

    // Reset all tabs and content to inactive state
    tabs.forEach(tab => tab.classList.remove('active'));
    tabContent.forEach(content => content.classList.remove('active'));

    // Activate the clicked tab and its corresponding content
    e.target.classList.add('active');
    document.querySelector(target).classList.add('active');
  });
});

