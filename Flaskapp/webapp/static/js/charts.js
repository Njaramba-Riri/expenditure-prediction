const line = document.getElementById('line').getContext('2d');
//const pleth = document.getElementById('pleth');
const sunburst = document.getElementById('sunburst');
const bar = document.getElementById('bar').getContext('2d');
const polar = document.getElementById('polar').getContext('2d');
const donught = document.getElementById('donut').getContext('2d');


// Plotly.newPlot(line, [{
//     x: [1, 2, 3, 4, 5],
//     y: [1, 2, 4, 8, 16, 32]
// }],
// {
//     margin: {t: 0 }
// });


// Plotly.newPlot(sunburst, [{
//     data: [{
//         type: "sunburst",
//         labels: ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
//         parents: ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
//         values: [10, 14, 12, 10, 2, 6, 6, 4, 4],
//         outsidetextfont: {size: 20, color: "#377eb8"},
//         leaf: {opacity: .4},
//         marker: {line: {width: 2}},
//     }],
//     layout: {
//         margin: {l:0, r:0, b:0, t:0},
//         width: 500,
//         height: 500
//     },
// }]);

var data = [
    {
      "type": "sunburst",
      "labels": ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
      "parents": ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
      "values":  [65, 14, 12, 10, 2, 6, 6, 4, 4],
      "leaf": {"opacity": 0.4},
      "marker": {"line": {"width": 2}},
      "branchvalues": 'total'
    }];
    
var layout = {
    "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
};


Plotly.newPlot('sunburst', data, layout, {showSendToCloud: true})

myPlot = document.getElementById("sunburst");


fetch('/letsgo/admin/features')
.then( response => response.json())
.then(data => {
    let counts = {};
    data.forEach(item => {
        if (counts[item.main_activity]) {
            counts[item.main_activity]++;
        } else {
            counts[item.main_activity] = 1;
        }
    });

    // Create arrays for the labels and data
    let data_labels = Object.keys(counts);
    let data_values = Object.values(counts);

    const chart = new Chart(bar, {
        type: 'bar',
        data: {
        labels: data_labels,
        datasets: [{
            label: 'Number of Tourists',
            data: data_values,
            borderWidth: 1
        }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Main Activity of the Trip.",
                    font: {
                        size: 20,
                        family: 'helvetica'
                    }
                },
                legend: {
                    display: false,
                    onHover: function (event, legendItem) {
                        chart.legend.options.display = true;
                        chart.update();
                    },
                    onLeave: function (event, legendItem) {
                        chart.legend.options.display = false;
                        chart.update();
                    }
                }
            },
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
});

fetch('/letsgo/admin/features')
.then(response => response.json())
.then(data => {
    let counts = {};
    data.forEach(item => {
        if(counts[item.predicted_category]) {
            counts[item.predicted_category]++;
        } else {
            counts[item.predicted_category] = 1;
        }
    });

    let data_labels = Object.keys(counts);
    let data_values = Object.values(counts);

    new Chart( polar, {
        type: 'polarArea',
        data: {
            datasets: [{
                label: "Predicted",
                data: data_values,
                borderWidth: 1,
                backgroundColor: [
                    'rgba(255, 0, 0, .5)',
                    'rgba(0, 255, 255, .5)',
                    'rgba(0, 255, 0, .5)',
                    'rgba(255, 0, 255, .5)',
                    'rgba(255, 255, 0, .5)',
                    'rgba(0, 0, 255, .5)',
                ]
            }],     
            labels: data_labels,
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Spending Categories",
                    font: {
                        size: 20,
                        
                        family: 'helvetica'
                    }
                }            
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    display: false
                },
                y: {
                    grid: {
                        display: false
                    },
                    display: false
                }
            }
        }
        
    });
});

fetch('/letsgo/admin/features')
.then(response => response.json())
.then(data => {
    let counts = {};
    data.forEach(item =>{
        if(counts[item.country]){
            counts[item.country]++;
        }else {
            counts[item.country] = 1;
        }
    })

    let data_labels = Object.keys(counts);
    let data_values = Object.values(counts);
    let hoveredElement = null;

    new Chart(donught, {
        type: 'doughnut',
        data: {
            labels: data_labels,
            datasets: [{
                label: "Number of Tourists",
                data: data_values,
                borderWidth: 1,
                hoverOffset: 4
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Tourist's Country of Origin",
                    font: {
                        size: 20,
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    display: false
                },
                y: {
                    grid: {
                        display: false
                    },
                    display: false
                }
            },
            onHover: (event, chartElement) => {
                if (chartElement[0] && chartElement[0].element != hoveredElement) {
                    if (hoveredElement) {
                        hoveredElement.outerRadius -= 5;
                    }
                    hoveredElement = chartElement[0].element;
                    hoveredElement.outerRadius += 5;
                }
            },
            onLeave: (event, chartElement) => {
                if (hoveredElement) {
                    hoveredElement.outerRadius -= 5;
                    hoveredElement = null;
                }
            }
        }
    });    

    donught.onmouseout =  function() {
        if (hoveredElement) {
            hoveredElement.outerRadius -= 5;
            hoveredElement = null;
            pieChart.update();
        }
    }
    Chart.defaults.doughnut.animation = {
        animateScale: true
    } 
});

fetch('/letsgo/admin/features')
.then(response => response.json())
.then(data => {
    new Chart(line, {
        type: 'line',
        data: {
            labels: data.map(item => item.purpose),
            datasets: [{
                label: "Females",
                data: data.map(item => item.total_female),
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: {
                    target: 'Origin',
                    below: 'rgba(0, 0, 255, .5)'
                },
                label: 'Males',
                data: data.map(item => item.total_male),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill:{
                    target: 'origin',
                    below: 'rgba(255, 255, 0, .5)'
                }
            }],
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            } 
        },
        options: {
            responsive: true,
            maintainAspectRatio: false            
        }
    })
});




