
// Line Chart
const ctxLine = document.getElementById('line-chart').getContext('2d');
new Chart(ctxLine, {
  type: 'line',
  data: {
    labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    datasets: [
      {
        label: 'Page Views',
        data: [120, 200, 150, 80, 70, 110, 130],
        borderColor: 'blue',
        borderWidth: 2,
      }
    ]
  }
});

// Bar Chart
const ctxBar = document.getElementById('bar-chart').getContext('2d');
new Chart(ctxBar, {
  type: 'bar',
  data: {
    labels: ['Free', 'Basic', 'Premium'],
    datasets: [
      {
        label: 'Subscriptions',
        data: [300, 450, 200],
        backgroundColor: ['green', 'orange', 'blue']
      }
    ]
  }
});
