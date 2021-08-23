
var cr9oOB = '保定';
var dN4HOMV3 = false;
var mYO7OUIEo = 'GETMONTHDATA';

function l91R6WCs87B() {
  ocA8cLjWVA = {};
  ocA8cLjWVA.city = cr9oOB;
  so0dfwPlMFfHCInqN(mYO7OUIEo,ocA8cLjWVA, function(oIN9Ay) {
    obj = oIN9Ay.data;
    items = obj.items;
    showTable(items);
    var data = obj.datas;
    var data_min = obj.datas_min;
    var data_max = obj.datas_max;
    var min = obj.min;
    var avg = obj.avg;
    var max = obj.max;
    showHistoryChart(data, data_min, data_max, min, avg, max);
    var datas1 = obj.datas1;
    var datas2 = obj.datas2;
    var datas3 = obj.datas3;
    var datas4 = obj.datas4;
    var datas5 = obj.datas5;
    var datas6 = obj.datas6;
    showLevel(datas1, datas2, datas3, datas4, datas5, datas6);
    var level = obj.level;
    showPieChart(level.level1, level.level2, level.level3, level.level4, level.level5, level.level6);
  }, 6);
}

var alfa = 0.8;
var valuePlotBaud = [{
  from: 0,
  to: 50,
  color: 'rgba(0, 254, 3, ' + alfa + ')',
  label: {
    text: '优',
    style: {
      color: "#606060"
    }
  }
}, {
  from: 51,
  to: 100,
  color: 'rgba(254, 245, 0, ' + alfa + ')',
  label: {
    text: '良',
    style: {
      color: '#606060'
    }
  }
}, {
  from: 101,
  to: 150,
  color: 'rgba(254, 125, 0, ' + alfa + ')',
  label: {
    text: '轻度污染',
    style: {
      color: '#606060'
    }
  }
}, {
  from: 151,
  to: 200,
  color: 'rgba(255, 3, 3, ' + alfa + ')',
  label: {
    text: '中度污染',
    style: {
      color: '#606060'
    }
  }
}, {
  from: 201,
  to: 300,
  color: 'rgba(188, 3,205 , ' + alfa + ')',
  label: {
    text: '重度污染',
    style: {
      color: '#606060'
    }
  }
}, {
  from: 301,
  to:600,
  color: 'rgba(72, 0, 78, ' + alfa + ')',
  label: {
    text: '严重污染',
    style: {
      color: '#606060'
    }
  }
}];

function showTable(items) {
  items.forEach(function(item) {
    $('.table tbody').append('\
      <tr>\
        <td align="center" class="hidden-xs hidden-sm hidden-md hidden-lg">' + Math.round(Math.random()*120)  + '</td><td align="center" class="hidden-xs hidden-lg hidden-md hidden-sm">' + Math.round(Math.random()*120)  + '</td><td align="center" class="hidden-xs hidden-md hidden-sm hidden-lg">' + Math.round(Math.random()*120)  + '</td>\
        <td align="center"><a href="daydata.php?city=' + cr9oOB + '&month=' + item.time_point + '">' + item.time_point + '</a></td>\
        <td align="center">' + item.aqi + '</td>\
        <td align="center" class="hidden-xs hidden-md hidden-lg hidden-sm">' + Math.round(Math.random()*120)  + '</td><td align="center" class="hidden-xs hidden-sm hidden-lg hidden-md">' + Math.round(Math.random()*120)  + '</td><td align="center" class="hidden">' + Math.round(Math.random()*120)  + '</td><td align="center" class="hidden">' + Math.round(Math.random()*120)  + '</td>\
        <td align="center" class="hidden-xs">' + item.min_aqi + '~' + item.max_aqi + '</td>\
        <td align="center"><span style="display:block;width:60px;text-align:center;' + getAQIStyle(item.aqi) + '">' + item.quality + '</span></td>\
        <td align="center">' + item.pm2_5 + '</td>\
        <td align="center">' + item.pm10 + '</td>\
        <td align="center" class="hidden-xs hidden-md hidden-sm hidden-lg">' + Math.round(Math.random()*120)  + '</td><td align="center" class="hidden-xs hidden-sm hidden-md hidden-lg">' + Math.round(Math.random()*120)  + '</td><td align="center" class="hidden">' + Math.round(Math.random()*120)  + '</td>\
        <td align="center" class="hidden-xs">' + item.so2 + '</td>\
        <td align="center" class="hidden-xs">' + item.co + '</td>\
        <td align="center" class="hidden-xs hidden-md hidden-lg hidden-sm">' + Math.round(Math.random()*120)  + '</td><td align="center" class="hidden-xs hidden-sm hidden-lg hidden-md">' + Math.round(Math.random()*120)  + '</td><td align="center" class="hidden">' + Math.round(Math.random()*120)  + '</td><td align="center" class="hidden">' + Math.round(Math.random()*120)  + '</td>\
        <td align="center" class="hidden-xs">' + item.no2 + '</td>\
        <td align="center" class="hidden-xs">' + item.o3 + '</td>\
      </tr>'
      );
  });
}

function showHistoryChart(data, data_min, data_max, min, avg, max) {
  $('#container').highcharts({
  chart: {
            zoomType: '',
            spacingRight: 0
        },
        title: {
            text: '保定空气质量指数（AQI）月变化趋势'
        },
        subtitle: {
            text: '最小值：' + min + ' 平均值：' + avg + ' 最大值：' + max
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats:{
            millisecond: '%H:%M:%S.%L',
            second: '%H:%M:%S',
            minute: '%H:%M',
            hour: '%H:%M',
            day: '%m-%d',
            week: '%m-%d',
            month: '%Y-%m',
            year: '%Y'
            }
        },
        yAxis: {
            title: {
                text: '空气质量指数(AQI)'
            },
            min:0,
            plotBands:valuePlotBaud
        },
        tooltip: {
          shared: true,
            enabled: true,
            useHTML: true,
          formatter: function() {
            tip = '' + Highcharts.dateFormat('%Y年%m月', this.x) +'<br/>'
                 + "<table width='160px' class='table-condensed table-bordered table-striped' style='margin:0px'>"
                  for (i=this.points.length-1;i>=0;i--)
                  {
                    color = this.points[i].series.color;
                  name = this.points[i].series.name;
                  y = this.points[i].y;
                  level = this.points[i].point.level;
                  tip = tip +  "<tr><td width='80px' style='color:" + color + "'>" + name +"</td><td align='right'><b>"+ y + "</b></td><td align='center' style='" + getAQIStyle(y) + "'>"+ level + "</td></tr>";
                  }
                  tip = tip + "</table>";
                  return tip;

            }
        },
        plotOptions:{
          series:{
            marker: {
                  enabled: true
              },
            turboThreshold: 0
          }
        },
        legend: {
            enabled: true
        },
        credits : {
            enabled:false
        },
        series: [{
            name: '最大值',
            type:'spline',
            color: '#a94442',
            data: data_max
        },{
            name: '平均值',
            type:'spline',
      color: '#31708f',
            data: data
        },{
            name: '最小值',
            type:'spline',
            color: '#3c763d',
            data: data_min
        }]
    });
}

function showLevel(datas1, datas2, datas3, datas4, datas5, datas6){
  $('#containerlevel').highcharts({
      chart: {
      type: 'area',
            zoomType: '',
            spacingRight: 0
        },
        title: {
            text: '保定空气质量指数（AQI）等级月变化趋势'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats:{
            millisecond: '%H:%M:%S.%L',
            second: '%H:%M:%S',
            minute: '%H:%M',
            hour: '%H:%M',
            day: '%m-%d',
            week: '%m-%d',
            month: '%Y-%m',
            year: '%Y'
            }
        },
        yAxis: {
            title: {
                text: '空气质量等级'
            }
        },
        tooltip: {
          //pointFormat: '<div class="width:100px"><div class="float:left"><span style="color:{series.color}">{series.name}</span>:</div><div class="float:left;text-align:right;"> <b>{point.y:,.0f}</b>天 ({point.percentage:.1f}%)<br/></div></div>',
            shared: true,
            useHTML:true,
          formatter: function() {

                tip = '' + Highcharts.dateFormat('%Y年%m月', this.x) +'<br/>'
                    + "<table width='160px' class='table-condensed table-bordered table-striped' style='margin:5px 0 0 0'>";
                    for (i=this.points.length-1;i>=0;i--)
                    {
                      color = this.points[i].series.color;

                    name = this.points[i].series.name;
                    style = getAQIStyleByLevel(name);
                    y = this.points[i].y;
                    percentage =(this.points[i].percentage).toFixed(1);
                    tip = tip +  "<tr><td width='80px' style='text-align:center;" + style + "'>" + name +"</td><td align='right'><b>"+ y + "</b>天</td><td align='right'>" + percentage + "%</td></tr>";
                    }
                    tip = tip + "</table>";
                    return tip;

            }
        },
        plotOptions:{
          series:{
            marker: {
                  enabled: false
              },
            turboThreshold: 0
          },
          area: {
                stacking: 'percent',
                lineColor: '#ffffff',
                lineWidth: 1,
                marker: {
                    lineWidth: 1,
                    lineColor: '#ffffff'
                }
            }
        },
        legend: {
            enabled: true
        },
        credits : {
            enabled:false
        },
        series: [{
            name: '严重污染',
            color: '#9c0a4e',
            data: datas6
        },{
            name: '重度污染',
            color: '#d20040',
            data: datas5
        },{
            name: '中度污染',
            color: '#ff401a',
            data: datas4
        },{
            name: '轻度污染',
            color: '#fa0',
            data: datas3
        },{
            name: '良',
            color: '#efdc31',
            data: datas2
        },{
            name: '优',
            color: '#43ce17',
            data: datas1
        }]
    });
}

function showPieChart(level1, level2, level3, level4, level5, level6) {
    var ratioArray = [];
    if(level1>0)
      {
        ratioArray.push({
          name:'优',
          color:'#43ce17',
          y:level1
        });
      }
      if(level2>0)
      {
        ratioArray.push({
          name:'良',
          color:'#efdc31',
          y:level2
        });
      }
      if(level3>0)
      {
        ratioArray.push({
          name:'轻度污染',
          color:'#fa0',
          y:level3
        });
      }
      if(level4>0)
      {
        ratioArray.push({
          name:'中度污染',
          color:'#ff401a',
          y:level4
        });
      }
      if(level5>0)
      {
        ratioArray.push({
          name:'重度污染',
          color:'#d20040',
          y:level5
        });
      }
      if(level6>0)
      {
        ratioArray.push({
          name:'严重污染',
          color:'#9c0a4e',
          y:level6
        });
      }

    $('#piecontainer').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: ''
        },
        tooltip: {
          pointFormat: '{series.name}: <b>{point.y}</b>月({point.percentage:.1f}%)'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    format: '<b>{point.name}</b>'
                },
                events: {
                click: function(e) {

                }
            }
            }
        },
        legend: {
                enabled: true
            },
        credits: {
                enabled:false
         },
        series: [{
            type: 'pie',
            name: '月数',
            data: ratioArray
        }]
      });
}


function getAQIStyle(aqi)
{
   if(aqi<=0)
   {
     style = "background-color:#6E6E6E;color:black;";
   }
   else if(aqi<=50)
   {
     style = "background-color:#43ce17;color:black;";
   }
   else if(aqi<=100)
   {
    style = "background-color:#efdc31;color:black;";
   }
   else if(aqi<=150)
   {
    style = "background-color:#fa0;color:black;";
   }
   else if(aqi<=200)
   {
    style = "background-color:#ff401a;color:white;";
   }
   else if(aqi<=300)
   {
    style = "background-color:#d20040;color:white;";
   }
   else
   {
    style = "background-color:#9c0a4e;color:white;";
   }
   return style;
}

function getAQIStyleByLevel(level)
{
   if(level=="无")
   {
     style = 'background-color:#6E6E6E;color:black;';
   }
   else if(level=="优")
   {
     style = 'background-color:#43ce17;color:black;';
   }
   else if(level=="良")
   {
    style = 'background-color:#efdc31;color:black;';
   }
   else if(level=="轻度污染")
   {
    style = 'background-color:#fa0;color:black;';
   }
   else if(level=="中度污染")
   {
    style = 'background-color:#ff401a;color:white;';
   }
   else if(level=="重度污染")
   {
    style = 'background-color:#d20040;color:white;';
   }
   else
   {
    style = 'background-color:#9c0a4e;color:white;';
   }
   return style;
}

function checkwebdriver() {
  let items = ['webdriver', '__driver_evaluate', '__webdriver_evaluate', '__selenium_evaluate', '__fxdriver_evaluate', '__driver_unwrapped', '__webdriver_unwrapped', '__selenium_unwrapped', '__fxdriver_unwrapped', '_Selenium_IDE_Recorder', '_selenium', 'calledSelenium', '_WEBDRIVER_ELEM_CACHE', 'ChromeDriverw', 'driver-evaluate', 'webdriver-evaluate', 'selenium-evaluate', 'webdriverCommand', 'webdriver-evaluate-response', '__webdriverFunc', '__webdriver_script_fn',  '__lastWatirAlert', '__lastWatirConfirm', '__lastWatirPrompt']
  for (i =0 ; i<items.length;i++) {
    item = items[i];
    // console.log(item, window.navigator[item])
    if (window.navigator[item]) {
      return true;
    }
  }
  return false;
}

$(function () {
  if (!dN4HOMV3 && !checkwebdriver()) {
    l91R6WCs87B();
  }
  Highcharts.setOptions({
    global: {
        useUTC: false
} });});