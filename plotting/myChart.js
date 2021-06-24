

var ctx = document.getElementById("myChart").getContext('2d');
var ctx2 = document.getElementById("myChart_mean").getContext('2d');

var imported_data = $.getJSON("../data/plotting_file2.json", function(){
    console.log("imported")
})
    .done(function( data ) {
        console.log(data)
        onJSONLoad(data)
    });


function onJSONLoad(jsonData){
    var options = {
      type: 'bubble',
      data: {
        // datasets: [
          // {
          //   label: 'John',
          //   data: [
          //     {
          //       x: 3,
          //       y: 7,
          //       r: 10
          //     }
          //   ],
          //   backgroundColor:"#ff6384",
          //   hoverBackgroundColor: "#ff6384"
          // },
          // {
          //   label: 'Paul',
          //     data: [
          //       {
          //         x: 6,
          //         y: 2,
          //         r: 10
          //       }
          //     ],
          //     backgroundColor:"#ff6384",
          //     hoverBackgroundColor: "#ff6384"
          // },
          // {
          //   label: 'George',
          //     data: [
          //       {
          //         x: 2,
          //         y: 6,
          //         r: 10
          //       }
          //     ],
          //     backgroundColor:"#ff6384",
          //     hoverBackgroundColor: "#ff6384"
          // },
          // {
          //   label: 'Ringo',
          //     data: [
          //       {
          //         x: 5,
          //         y: 3,
          //         r: 10
          //       }
          //     ],
          //     backgroundColor:"#ff6384",
          //     hoverBackgroundColor: "#ff6384"
          // },
          // {
          //   label: 'John',
          //     data: [
          //       {
          //         x: 2,
          //         y: 1,
          //         r: 10
          //       }
          //     ],
          //     backgroundColor:"#ff6384",
          // //     hoverBackgroundColor: "#ff6384"
          // },
          // {
          //   label: 'George',
          //     data: [
          //       {
          //         x: 1,
          //         y: 3,
          //         r: 10
          //       }
          //     ],
          //     backgroundColor:"#ff6384",
          //     hoverBackgroundColor: "#ff6384"
          // },
          // {
          //   label: 'Ringo',
          //     data: [
          //       {
          //         x: 1,
          //         y: 1,
          //         r: 10
          //       }
          //     ],
          //     backgroundColor:"#ff6384",
          //     hoverBackgroundColor: "#ff6384"
          // },
          // {
          //   label: 'George',
          //     data: [
          //       {
          //         x: 1,
          //         y: 2,
          //         r: 10
          //       }
          //     ],
          //     backgroundColor:"#ff6384",
          //     hoverBackgroundColor: "#ff6384"
          // }
          // ]
		 datasets:  jsonData.dataset1
      }
    }
    new Chart(ctx, options);
    var options = {
      type: 'bubble',
      data: {
        datasets:  jsonData.dataset2
      }
    }
    new Chart(ctx2, options);
}

// var ctx = document.getElementById('chartJSContainer').getContext('2d');