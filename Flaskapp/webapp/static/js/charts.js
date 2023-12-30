const line = document.getElementById('line');
const pleth = document.getElementById('pleth')
const sunburst = document.getElementById('sunburst')
const bar = document.getElementById('bar');
const polar = document.getElementById('polar');
const donught = document.getElementById('donut');


Plotly.newPlot(line, [{
    x: [1, 2, 3, 4, 5],
    y: [1, 2, 4, 8, 16, 32]
}],
{
    margin: {t: 0 }
});

Plotly.d3.csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv', function(err, rows){
    function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
    }

    var data = [{
        type: 'choropleth',
        locations: unpack(rows, 'CODE'),
        z: unpack(rows, 'GDP (BILLIONS)'),
        text: unpack(rows, 'COUNTRY'),
        colorscale: [
            [0,'rgb(5, 10, 172)'],[0.35,'rgb(40, 60, 190)'],
            [0.5,'rgb(70, 100, 245)'], [0.6,'rgb(90, 120, 245)'],
            [0.7,'rgb(106, 137, 247)'],[1,'rgb(220, 220, 220)']
        ],
        autocolorscale: false,
        reversescale: true,
        marker: {
            line: {
                color: 'rgb(180,180,180)',
                width: 0.5
            }
        },
        tick0: 0,
        zmin: 0,
        dtick: 1000,
        colorbar: {
            autotic: false,
            tickprefix: '$',
            title: 'GDP<br>Billions US$'
        }
    }];

    var layout = {
        title: '2014 Global GDP<br>Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">CIA World Factbook</a>',
        geo:{
            showframe: false,
            showcoastlines: false,
            projection:{
                type: 'mercator'
            }
        }
    };

    Plotly.newPlot(pleth, data, layout, {showLink: false});
});

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
      "labels": ["Tour Arrangement", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
      "parents": ["", "Tour Arrangement", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
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

const chart = new Chart(bar, {
    type: 'bar',
    data: {
    labels: ['Wildlife', 'Beach', 'Cultural', 'Medical', 'Business', 'Volunteering'],
    datasets: [{
        label: 'Number of Tourists',
        data: [12392, 8738, 3482, 72, 2387, 978],
        borderWidth: 1
    }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: "Purpose of the Trip.",
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

const polarChart = new Chart( polar, {
    type: 'polarArea',
    data: {
        datasets: [{
            label: "Number of Tourists",
            data: [2500, 1564, 437, 5490, 11883, 6308],
            borderWidth: 1,
            backgroundColor: [
                'rgba(255, 0, 0, .5)',
                'rgba(0, 255, 255, .5)',
                'rgba(0, 255, 0, .5)',
                'rgba(255, 0, 255, .5)',
                'rgba(255, 255, 0, .5)',
                'rgba(0, 0, 255, .5)'
            ]
        }],     
        labels: ['High Cost', 'Higher Cost', 'Highest Cost', 'Low Cost', 'Normal Cost', 'Lower Cost'],
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

let hoveredElement = null;

const pieChart = new Chart(donught, {
    type: 'doughnut',
    data: {
        labels: ['Kenya', 'United Kingdom', 'United States', 'South Africa', 'Uganda'],
        datasets: [{
            label: "Number of Tourists",
            data: [8956, 5342, 6839, 4983, 7389],
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
                    hoveredElement.outerRadius -= 10;
                }
                hoveredElement = chartElement[0].element;
                hoveredElement.outerRadius += 10;
            }
        },
        onLeave: (event, chartElement) => {
            if (hoveredElement) {
                hoveredElement.outerRadius -= 10;
                hoveredElement = null;
            }
        }
    }
});

donught.onmouseout =  function() {
    if (hoveredElement) {
        hoveredElement.outerRadius -= 10;
        hoveredElement = null;
        pieChart.update();
    }
}
Chart.defaults.doughnut.animation = {
    animateScale: true
} 