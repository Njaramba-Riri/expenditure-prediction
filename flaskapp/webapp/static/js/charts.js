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

    // Extract labels and parents from data
    data.forEach(item => {
        // Add main activity to labels and its parent to parents
        labels.push(item.tour_arrangement);
        parents.push(item.info_source);

        // Add arrangement to labels and an empty string to parents if not already present
        if (!labels.includes(item.info_source)) {
            labels.push(item.info_source);
            parents.push('');
        }
    });
    
    // Calculate data values
    let data_values = labels.map(label => {
        let count = data.filter(item => item.info_source === label).length;
        return count;
    });

    // Construct chart data
    var chartData = [{
        type: "sunburst",
        labels: labels,
        parents: parents,
        values: data_values,
        leaf: { opacity: .7 },
        insidetextfont: { size: 10, color: 'white' },
        outsidetextfont: { size: 10, color: 'black' }
    }];

    // Define layout
    var layout = {
        title: {
            text: "Effect of Information Source in Planning Tour",
            font: {
                family: "Courier New, monospace",
                size: 20,
            },
            xref: 'paper',
            x: 0.05
        },
        margin: { l: 0, r: 0, b: 0, t: 0 },
    };

    // Define configuration
    var config = {
        displayModeBar: true
    };

    // Render sunburst chart
    Plotly.newPlot('sunburst', chartData, layout, config);
})
.catch(error => {
    console.error('Error fetching or processing data:', error);
});


// Main activities.
fetch('/letsgo/admin/features')
.then( response => response.json())
.then(data => {
    let categoryData = {}; // Object to store data for each predicted category

    // Count occurrences of each predicted category and regions within them
    data.forEach(item => {
        if (!(item.main_activity in categoryData)) {
            categoryData[item.main_activity] = {};
        }

        if (item.predicted_category in categoryData[item.main_activity]) {
            categoryData[item.main_activity][item.predicted_category]++;
        } else {
            categoryData[item.main_activity][item.predicted_category] = 1;
        }
    });

    let data_labels = Object.keys(categoryData);
    let datasets = [];

    // Process main_avtivity data for each predicted category to create datasets
    data_labels.forEach(category => {
        let activities = Object.keys(categoryData[category]);
        let counts = Object.values(categoryData[category]);

        let backgroundColors = generateUniqueColors(activities.length);

        datasets.push({
            label: category,
            data: counts,
            backgroundColor: backgroundColors,
        });
    });

    // Get all unique regions from all categories
    let allActivi = Object.keys(categoryData).reduce((acc, key) => {
        return [...acc, ...Object.keys(categoryData[key])];
    }, []);

    // Remove duplicate regions
    let uniqueActivi = Array.from(new Set(allActivi));

    new Chart(bar, {
        type: 'bar',
        data: {
            labels: uniqueActivi,
            datasets: datasets
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Main activity in Predicted category",
                    font: {
                        size: 20,
                        family: 'Calibri'
                    }
                }
            },
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    suggestedMax: getMaxValue(categoryData) * 1.1, // Add 10% padding
                    grid: {
                        display: false,
                    }
            }
        }
    }
});

});

// Polar chart
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
                    'rgba(31, 0, 255, .4)',
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
                        family: 'helvetica',
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

//Donought chart
fetch('/letsgo/admin/features')
.then(response => response.json())
.then(data => {
    let counts = {};
    data.forEach(item =>{
        if(counts[item.region]){
            counts[item.region]++;
        }else {
            counts[item.region] = 1;
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
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, data) {
                        var dataset = data.datasets[tooltipItem.datasetIndex];
                        var total = dataset.data.reduce(function(previousValue, currentValue) {
                            return previousValue + currentValue;
                        });
                        var currentValue = dataset.data[tooltipItem.index];
                        var percentage = Math.floor(((currentValue/total) * 100)+0.5);         
                        return percentage + "%";
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: "Know Your Tourists",
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
                        hoveredElement.outerRadius -= 0;
                    }
                    hoveredElement = chartElement[0].element;
                    hoveredElement.outerRadius += 0;
                }
            },
            onLeave: (event, chartElement) => {
                if (hoveredElement) {
                    hoveredElement.outerRadius -= 0;
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

// Regions vs Cost Category
fetch('/letsgo/admin/features')
.then(response => response.json())
.then(data => {
    let categoryData = {}; // Object to store data for each predicted category

    // Count occurrences of each predicted category and regions within them
    data.forEach(item => {
        if (!(item.predicted_category in categoryData)) {
            categoryData[item.predicted_category] = {};
        }

        if (item.region in categoryData[item.predicted_category]) {
            categoryData[item.predicted_category][item.region]++;
        } else {
            categoryData[item.predicted_category][item.region] = 1;
        }
    });

    let data_labels = Object.keys(categoryData);
    let datasets = [];

        // Process region data for each predicted category to create datasets
        data_labels.forEach(category => {
            let regions = Object.keys(categoryData[category]);
            let counts = Object.values(categoryData[category]);

            let backgroundColors = generateUniqueColors(regions.length);

            datasets.push({
                label: category,
                data: counts,
                backgroundColor: backgroundColors,
            });
        });

        // Get all unique regions from all categories
        let allRegions = Object.keys(categoryData).reduce((acc, key) => {
            return [...acc, ...Object.keys(categoryData[key])];
        }, []);

        // Remove duplicate regions
        let uniqueRegions = Array.from(new Set(allRegions));

        // Plot the data using Chart.js
        new Chart('line', {
            type: 'bar',
            data: {
                labels: uniqueRegions,
                datasets: datasets
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: "Regions by Predicted Categories",
                        font: {
                            size: 20
                        }
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMax: getMaxValue(categoryData) * 1.1 // Add 10% padding
                }
            }
        }
    });
});

// Function to generate unique colors
function generateUniqueColors(count) {
    let colors = [];
    for (let i = 0; i < count; i++) {
        colors.push(`rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.8)`);
    }
    return colors;
}

// Function to get the maximum value in the categoryData object
function getMaxValue(categoryData) {
    let max = 0;
    Object.values(categoryData).forEach(category => {
        let categoryMax = Math.max(...Object.values(category));
        if (categoryMax > max) {
            max = categoryMax;
        }
    });
    return max;
}


// Feature importance
function drawImportance(imps) {
    var featureImportanceData = imps;
    
    // Get the canvas element and context
    var canvas = document.getElementById('imps');
    var ctx = canvas.getContext('2d');
    
    // Define canvas dimensions and padding
    var canvasWidth = canvas.width;
    var canvasHeight = canvas.height;
    var padding = 80;
    var barOffset = 20;
    
    // Calculate maximum importance for dynamic scaling
    var maxImportance = Math.max(...featureImportanceData.map(item => item.Importance));
    
    // Bar settings
    var barWidth = 20;
    var barPadding = 10;
    
    // Scale the canvas height based on maximum importance
    var scaledHeight = canvasHeight - padding * 2;
    var scaleY = scaledHeight / maxImportance;
    
    // Draw the plot
    for (var i = 0; i < featureImportanceData.length; i++) {
        var importance = featureImportanceData[i].Importance;
        var barHeight = importance * scaleY;
        var xPos = padding + (barWidth + barPadding) * i;
        
        // Draw bar with unique color
        var barColor = getRandomColor();
        ctx.fillStyle = barColor;
        ctx.fillRect(xPos, canvasHeight - padding - barHeight, barWidth, barHeight);
        
        // Draw label
        ctx.fillStyle = '#000'; 
        ctx.textAlign = 'right';
        ctx.font = "italic 10px Times New Roman";
        ctx.save();
        ctx.translate(xPos + barWidth / 2, canvasHeight - padding + barOffset);
        ctx.rotate(-Math.PI / 4);
        ctx.fillText(featureImportanceData[i].Feature, 0, 0);
        ctx.restore();
        ctx.fillText(formatNumber(importance), xPos + barWidth, canvasHeight - padding - barHeight - 5);
    }
    
    // Draw x-axis
    ctx.beginPath();
    ctx.moveTo(padding, canvasHeight - padding);
    ctx.lineTo(canvasWidth - padding, canvasHeight - padding);
    ctx.font = 'bold 15px monospace'
    ctx.stroke();
    
    // Draw x-axis label
    ctx.textAlign = 'left';
    ctx.fillText('Variable', canvasWidth / 2, canvasHeight / 2 );
    
    // Draw y-axis label
    ctx.save();
    ctx.translate(30, canvasHeight / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.textAlign = 'center';
    ctx.fillText('Importance', 20, 30);
    ctx.restore();
    
    // Draw chart title
    ctx.font = 'bold 20px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('What will influence a tourist spending?.', canvasWidth / 2, padding / 2);
}

// Function to generate a random color
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Function to format numbers or percentages
function formatNumber(num) {
    return Math.round(num * 100) / 100 + '%';
}
