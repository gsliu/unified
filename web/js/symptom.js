/**
 * Created by gliu on 6/21/16.
 */
function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};


var oPerfChart;
function refreshChart() {
    $('#div_kb_info').empty()
    //异步请求数据
    kbnumber = getUrlParameter('id');
    $.ajax({
        type: "GET",
        url: 'http://unified.eng.vmware.com:8000/symptom',// hard code kb number for debugging
        data: {kbnumber: kbnumber},
        success: function (data) {
            //定义一个数组
            var series_data = [];
            var res = JSON.parse(data);

            //display kb


            kbhtml = '<div><h3><a href="' + res["url"] + '">' + res["title"] + '</a></h3><p>' + res["text"] +
                '</p> <p>Total <b>' + res['total']+ '</b> Hits </p> ' +
                ' <hr></div>'

            $("#div_kb_info").append(kbhtml);




            var hits = eval(res['hits']);
            var mydate;

            //迭代，把异步获取的数据放到数组中
            $.each(hits, function (i, elem) {


                series_data.push([Date.parse(elem['time']), parseInt(elem['hits'])]);
                console.log("aaaa");
            });
            //设置数据
            oPerfChart.series[0].setData(series_data);


        },
        error: function (e) {
            console.log("Cannot get symptom data, check database\n");
        }

    });

}


$(function () {
    oPerfChart = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'divHitsChart'

        },

        title: {
            text: 'Hits Htatistics'
        },
        /*
        subtitle: {
            text: 'hits data for each symptom'
        },
        */
        xAxis: {
            type: 'datetime',

            formatter: function () {
                return Highcharts.dateFormat('%a %d %b', this.value);
            },
            title: {
                text: 'Date'
            }
        },
        yAxis: {
            title: {
                text: 'Hits'
            },
            min: 0
        },


        plotOptions: {
            spline: {
                marker: {
                    enabled: true
                }
            }
        },

        series: [{
            name: 'Hits/Day',
            yAxis: 0


        }]
    });


});

refreshChart()
