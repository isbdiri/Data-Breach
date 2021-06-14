// https://stackoverflow.com/a/44661975

// var imported_data = require('../data/plotting_file.json');
define(function (require) {
   var imported_data = require('../data/plotting_file.json');
});

var ctx = document.getElementById('myChart').getContext('2d');
var scatterChart = new Chart(ctx, {
   type: 'scatter',
   data: {
      labels: ["Label 1", "Label 2", "Label 3"],
      datasets: [{
         label: 'Legend',
         data: [{
            x: -10,
            y: 0,
         }, {
            x: 0,
            y: 10
         }, {
            x: 10,
            y: 5
         }]
      }]
   },
   options: {
      tooltips: {
         callbacks: {
            label: function(tooltipItem, data) {
               var label = data.labels[tooltipItem.index];
               return label + ': (' + tooltipItem.xLabel + ', ' + tooltipItem.yLabel + ')';
            }
         }
      }
   }
});