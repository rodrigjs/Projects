
const pollData = [
  {
    option: "Spider-Man",
    votes: 11,
    color: "rgba(255, 99, 132)"
  },
  {
    option: "Superman",
    votes: 8,
    color: "rgba(54, 162, 235)"
  },
  {
    option: "Batman",
    votes: 11,
    color: "rgba(36, 36, 36)"
  },
  {
    option: "Son Goku",
    votes: 5,
    color: "rgba(255, 159, 64)"
  },
  {
    option: "Hulk",
    votes: 3,
    color: "rgba(75, 192, 192)"
  },
  {
    option: "Wolverine",
    votes: 8,
    color: "rgba(255, 206, 86)"
  },
  {
    option: "Other",
    votes: 10,
    color: "rgba(153, 102, 255)"
  }
];

Chart.defaults.global.defaultFontFamily = '"Comic Sans MS", cursive sans-serif';

const ctx = document.getElementById('chart').getContext('2d');
const pollChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: pollData.map(pollOption => pollOption.option),
        datasets: [{
            label: '# of Votes',
            data: pollData.map(pollOption => pollOption.votes),
            backgroundColor: pollData.map(pollOption => pollOption.color),
            borderWidth: 3
        }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      },
      title: {
        display: true,
        text: 'Favorite Superheroes',
        fontColor: "#333",
        fontSize: 20,
        padding: 20
      }

    }
});
