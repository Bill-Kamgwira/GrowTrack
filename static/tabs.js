alert("Javascript Loaded!");
const tabs = document.querySelectorAll('.tabs li a');
const tabContent = document.querySelectorAll('.tab-pane');

// Show the first tab content by default
tabContent[0].classList.add('active');

tabs.forEach(tab => {
  tab.addEventListener('click', (e) => {
    e.preventDefault();
    const target = e.target.getAttribute('href');

    // Remove active class from all tabs and tab content
    tabs.forEach(tab => tab.classList.remove('active'));
    tabContent.forEach(tab => tab.classList.remove('active'));

    // Add active class to the clicked tab and its corresponding content
    e.target.classList.add('active');
    document.querySelector(target).classList.add('active');
  });
});

