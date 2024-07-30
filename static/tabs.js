const tabs = document.querySelectorAll('.tabs li a');
const tabContent = document.querySelectorAll('.tab-pane');

tabs.forEach(tab => {
  tab.addEventListener('click', (e) => {
    e.preventDefault();
    const target = e.target.getAttribute('href');
    tabs.forEach(tab => tab.classList.remove('active'));
    e.target.classList.add('active');
    tabContent.forEach(tab => tab.classList.remove('active'));
    document.querySelector(target).classList.add('active');
  });
});
