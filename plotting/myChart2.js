// https://stackoverflow.com/a/44661975

// var imported_data = require('../data/plotting_file.json');
// define(function (require) {
//    var imported_data = require('../data/plotting_file.json');
// });

var imported_data = $.getJSON("../data/plotting_file.json", function(){
	console.log("imported")
})
	.done(function( data ) {
		console.log(data)
		onJSONLoad(data)
	});

function onJSONLoad(jsonData){
    var ctx = document.getElementById('myChart').getContext('2d');
    var scatterChart = new Chart(ctx, {
       type: 'scatter',
       data: {
          labels: jsonData.labels,
          datasets: jsonData.datasets
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

}
