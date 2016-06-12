$(function () {

    /* data stolen from http://howmanyleft.co.uk/vehicle/jaguar_'e'_type */
    var day_data = [
        {"period": "2012-10-01", "licensed": 807, "sorned": 660},
        {"period": "2012-09-30", "licensed": 1251, "sorned": 729},
        {"period": "2012-09-29", "licensed": 1769, "sorned": 1018},
        {"period": "2012-09-20", "licensed": 2246, "sorned": 1461},
        {"period": "2012-09-19", "licensed": 2657, "sorned": 1967},
        {"period": "2012-09-18", "licensed": 3148, "sorned": 2627},
        {"period": "2012-09-17", "licensed": 3471, "sorned": 3740},
        {"period": "2012-09-16", "licensed": 2871, "sorned": 2216},
        {"period": "2012-09-15", "licensed": 2401, "sorned": 1656},
        {"period": "2012-09-10", "licensed": 2115, "sorned": 1022}
    ];

    Morris.Bar({
        element: 'graph_bar',
        data: [
            {device: 'Dal', Quantity: 136},
            {device: 'Rice', Quantity: 137},
        ],
        xkey: 'device',
        ykeys: ['Quantity'],
        labels: ['QUantity'],
        barRatio: 0.4,
        barColors: ['#26B99A', '#34495E', '#ACADAC', '#3498DB'],
        xLabelAngle: 35,
        hideHover: 'auto'
    });
    Morris.Bar({
        element: 'graph_bar1',
        data: [
            {device: 'Jaundice', Quantity: 20},
            {device: 'Stomach Upset', Quantity: 137},
        ],
        xkey: 'device',
        ykeys: ['Quantity'],
        labels: ['Quantity'],
        barRatio: 0.4,
        barColors: ['#26B99A', '#34495E', '#ACADAC', '#3498DB'],
        xLabelAngle: 35,
        hideHover: 'auto'
    });
Morris.Bar({
        element: 'graph_bar2',
        data: [
            {device: 'Dead', Quantity: 75},
            {device: 'Orphans', Quantity: 25},
        ],
        xkey: 'device',
        ykeys: ['Quantity'],
        labels: ['Quantity'],
        barRatio: 0.4,
        barColors: ['#26B99A', '#34495E', '#ACADAC', '#3498DB'],
        xLabelAngle: 35,
        hideHover: 'auto'
    });

    


    Morris.Donut({
        element: 'graph_donut',
        data: [
            {label: 'Bardhamman', value: 25},
            {label: 'Bankura', value: 40},
            {label: 'Hooghly', value: 25},
            {label: 'Midnapore', value: 10}
        ],
        colors: ['#26B99A', '#34495E', '#ACADAC', '#3498DB'],
        formatter: function (y) {
            return y + "%"
        }
    });



    Morris.Donut({
        element: 'graph_donut2',
        data: [
            {label: 'AUD', value: 9.4},
            {label: 'IMG', value: 12.5},
            {label: 'SMS', value: 40.6},
            {label: 'TXT', value: 28.4},
            {label: 'VID', value: 9.4}
        ],
        colors: ['#26B99A', '#34495E', '#ACADAC', '#3498DB'],
        formatter: function (y) {
            return y + "%"
        }
    });

    Morris.Donut({
        element: 'graph_donut1',
        data: [
            {label: 'Dead', value: 75},
            {label: 'Orphans', value: 25}
        ],
        colors: ['#26B99A', '#34495E', '#ACADAC', '#3498DB'],
        formatter: function (y) {
            return y + "%"
        }
    });

    new Morris.Line({
        element: 'graph_line',
        xkey: 'year',
        ykeys: ['value'],
        labels: ['Value'],
        hideHover: 'auto',
        lineColors: ['#26B99A', '#34495E', '#ACADAC', '#3498DB'],
        data: [
            {year: '2008', value: 20},
            {year: '2009', value: 10},
            {year: '2010', value: 5},
            {year: '2011', value: 5},
            {year: '2012', value: 20}
        ]
    });

    new Morris.Line({
        element: 'graph_line1',
        xkey: 'year',
        ykeys: ['value'],
        labels: ['Value'],
        hideHover: 'auto',
        lineColors: ['#26B99A', '#34495E', '#ACADAC', '#3498DB'],
        data: [
            {year: '2008', value: 20},
            {year: '2009', value: 10},
            {year: '2010', value: 5},
            {year: '2011', value: 5},
            {year: '2012', value: 20}
        ]
    });

});