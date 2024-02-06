const line = document.getElementById('line').getContext('2d');
// const pleth = document.getElementById('pleth');
const sunburst = document.getElementById('sunburst');
const bar = document.getElementById('bar').getContext('2d');
const polar = document.getElementById('polar').getContext('2d');
const donught = document.getElementById('donut').getContext('2d');


fetch('/letsgo/admin/features')
.then(response => response.json())
.then(data => {
    let labels = [];
    let parents = [];

    data.forEach(item => {
        // Add main activity to labels and its parent to parents
        labels.push(item.tour_arrangement);
        parents.push(item.info_source);

        // Add arrangement to labels and an empty string to parents
        if (!labels.includes(item.info_source)) {
            labels.push(item.info_source);
            parents.push('');
        }
    });

    let data_values = labels.map(label => {
        let count = data.filter(item => item.info_source === label).length;
        return count;
    });

    var chartData = [{
        "type": "sunburst",
        "labels": labels,
        "parents": parents,
        "values": data_values,
        "leaf": {"opacity": .7},
       "insidetextfont": {"size": 10, "color": 'white'},
        "outsidetextfont": {"size": 10, "color": 'black'}
    }];

    var layout = {
        "title": {
            "text": "Effect of Information Source in Planning Tour",
            "font": {
                "family": "Courier New, monospace",
                "size": 20,
                
            },
            "xref": 'paper',
            "X": 0.05
        },
        "margin": {"l":0, "r":0, "b":0, "t":0},
        //"sunburstcolorway": ["#636efa","#ef553b","#00cc96"]
    };

    var config = {
        'displayModeBar': true
    }

    Plotly.newPlot(sunburst, chartData, layout, config);
});

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
            responsive: true,
            maintainAspectRatio: false,
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

    let doughnut = new Chart(donught, {
        type: 'doughnut',
        data: {
            labels: data_labels,
            datasets: [{
                label: "Submissions",
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
            responsive: true,
            maintainAspectRatio: false,
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

    doughnut.onmouseout =  function() {
        if (hoveredElement) {
            hoveredElement.outerRadius -= 5;
            hoveredElement = null;
            pieChart.update();
        }
    }
});

fetch('/letsgo/admin/features')
.then(response => response.json())
.then(data => {
    let counts = {};
    data.forEach(item => {
        if(counts[item.predicted_category]){
            counts[item.predicted_category]++;
        }else {
            counts[item.predicted_category]=1;
        }
    })

    let data_labels = Object.keys(counts)
    new Chart(line, {
        type: 'line',
        data: {
            labels: data_labels,
            datasets: [{
                label: "Females",
                data: data.map(item => item.total_female),
                tension: .4,
                fill: {
                    target: 'origin',
                    below: 'rgba(0, 0, 255, .8)'
                }
            }, {
                label: 'Males',
                data: data.map(item => item.total_male),
                borderWidth: 1,
                tension: .4,
                fill:{
                    target: 'origin',
                    below: 'rgba(255, 255, 0, .8)'
                }                   
            }
            ],
            scales: {
                y: {
                    beginAtZero: false
                },
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            } 
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Gender Influence on Spending.",
                    font: {
                        size: 20
                    }
                }  
            },
            responsive: true,
            maintainAspectRatio: false            
        }
    })
});