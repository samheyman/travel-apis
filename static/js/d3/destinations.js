// fare search history
// actual numbers
// type=fare-search
var chart1 = c3.generate({
    bindto: '#destinations_most_searched_chart',
    data: {
      x: 'x',
      columns: [
        ['x', 'SIN', 'LON', 'NYC', 'TUN', 'BCN'],
        ['searches', 12300, 11000, 5000, 2000, 500],
      ],

      types: {
        searches: 'bar'
      },
      colors: {
        searches: '#005EB8',
      }
    },
    axis : {
        x : {
            type: 'category',
            categories: ['PAR', 'LON', 'NYC', 'TUN', 'BCN'] 
        }
    }
});

// Most travelled destinations - has to be anonymised 
// Top destinations - flight scores
// type = air-traffic
var chart2 = c3.generate({
  bindto: '#destinations_most_travelled_chart',
  data: {
    x: 'x',
    columns: [
      ['x', 'SIN', 'LON', 'NYC', 'TUN', 'BCN'],
      ['bookings', 1, 0.79, 0.34, 0.22, 0.08],
    ],

    types: {
      bookings: 'bar'
    },
    colors: {
      bookings: '#9BCAEB',
    }
  },
  axis : {
      x : {
          type: 'category',
          categories: ['PAR', 'LON', 'NYC', 'TUN', 'BCN']
          
      }
  }

});


function load_charts() { 

  chart1.load({
    columns: [
      most_searched_data_xs,
      most_searched_data_values
    ]
  });

  chart2.load({
    columns: [
      most_travelled_data_xs,
      most_travelled_data_values
    ]
  });
}



// setTimeout(function () {
//     chart.load({
//         columns: [
//             ['data3', 130, -150, 200, 300, -200, 100]
//         ]
//     });
// }, 1000);

