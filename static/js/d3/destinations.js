// fare search history
// actual numbers
// type=fare-search
var chart1 = c3.generate({
    bindto: '#destinations_most_searched_chart',
    data: {
      //x: 'x',
      columns: [
        ['number of searches', 0, 0, 0, 0, 0],
      ],

      types: {
        'number of searches': 'bar'
      },
      colors: {
        'number of searches': '#005EB8',
      }
    },
    axis: {
      rotated: true,
      y: {
        show: true,
        label: 'total search numbers'
      },
      x : {
        type: 'category',
        categories: ['', '', '', '', '']
      }     
    },
    legend: {
      hide: true
    }
});

// Most travelled destinations - has to be anonymised 
// Top destinations - flight scores
// type = air-traffic
var chart2 = c3.generate({
  bindto: '#destinations_most_travelled_chart',
  data: {
    //x: 'x',
    columns: [
      ['number of travels', 0, 0, 0, 0, 0],
    ],

    types: {
      'number of travels': 'bar'
    },
    colors: {
      'number of travels': '#9BCAEB',
    }
  },
  axis : {
    rotated: true,
    y: {
      show: true,
      label: 'total number of check-ins (normalized to a range 0-1)'
    },
    
    x : {
        type: 'category',
        categories: ['', '', '', '', '']
    }
  },
  legend: {
    hide: true
  }
});

// Most booked destinations - has to be anonymised 
// Top destinations - flight scores
// type = air-traffic
var chart3 = c3.generate({
  bindto: '#destinations_most_booked_chart',
  data: {
    //x: 'x',
    columns: [
      ['number of bookings', 0, 0, 0, 0, 0],
    ],

    types: {
      'number of bookings': 'bar'
    },
    colors: {
      'number of bookings': '#9BCAEB',
    }
  },
  axis : {
    rotated: true,
    y: {
      show: true,
      label: 'total number of check-ins (normalized to a range 0-1)'
    },
    
    x : {
        type: 'category',
        categories: ['', '', '', '', '']
    }
  },
  legend: {
    hide: true
  }
});

var chart4 = c3.generate({
  bindto: '#busiest_period_chart',
  data: {
    //x: 'x',
    columns: [
      ['number of travelers', 0, 0, 0, 0, 0],
    ],

    types: {
      'number of travelers': 'bar'
    },
    colors: {
      'number of travelers': '#9BCAEB',
    }
  },
  axis : {
    rotated: true,
    y: {
      show: true,
      label: 'total number of travelers (normalized to a range 0-1)'
    },
    
    x : {
        type: 'category',
        categories: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    }
  },
  legend: {
    hide: true
  }
});


function load_charts() { 
  most_searched_data_xs.shift();
  most_travelled_data_xs.shift();
  most_booked_data_xs.shift();
  busiest_period_months.shift();

  chart1 = c3.generate({
    bindto: '#destinations_most_searched_chart',
    data: {
      columns: [
        most_searched_data_values,
      ],
      types: {
        'number of searches': 'bar'
      },
      colors: {
        'number of searches': '#005EB8',
      }

        //most_searched_data_xs,
      // ["x", "RAK", "OPO", "DXB", "UIO", "SDQ"],
        //["number of searches", 498, 328, 282, 237, 185]
    },
    axis: {
      rotated: true,
      y: {
        show: true,
        label: 'total number of searches'
      },    
      x : {
          type: 'category',
          categories: most_searched_data_xs
      }
    },
    legend: {
      hide: true
    }
  });

  chart2 = c3.generate({
    bindto: '#destinations_most_travelled_chart',
    data: {
      columns: [
        most_travelled_data_values
      ],
      types: {
        'number of travels': 'bar'
      },
      colors: {
        'number of travels': '#9BCAEB',
      }
    },
    axis: {
      rotated: true,
      y: {
        show: true,
        label: 'number of travelers (normalized to a range 0-100)'
      },    
      x : {
          type: 'category',
          categories: most_travelled_data_xs
      }
    },
    legend: {
      hide: true
    }
  });

  chart3 = c3.generate({
    bindto: '#destinations_most_booked_chart',
    data: {
      columns: [
        most_booked_data_values
      ],
      types: {
        'number of bookings': 'bar'
      },
      colors: {
        'number of bookings': '#9BCAEB',
      }
    },
    axis: {
      rotated: true,
      y: {
        show: true,
        label: 'number of travelers (normalized to a range 0-100)'
      },    
      x : {
          type: 'category',
          categories: most_booked_data_xs
      }
    },
    legend: {
      hide: true
    }
  });

  chart4 = c3.generate({
    bindto: '#busiest_period_chart',
    data: {
      columns: [
        busiest_period_travelers
      ],
      types: {
        'number of travelers': 'bar'
      },
      colors: {
        'number of travelers': '#9BCAEB',
      }
    },
    axis: {
      rotated: false,
      y: {
        show: true,
        label: 'number of travelers (normalized to a range 0-100)'
      },    
      x : {
          type: 'category',
          categories: busiest_period_months
      }
    },
    legend: {
      hide: true
    }
  });
}



// setTimeout(function () {
//     chart.load({
//         columns: [
//             ['data3', 130, -150, 200, 300, -200, 100]
//         ]
//     });
// }, 1000);

