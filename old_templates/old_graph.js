let title = document.getElementById('chart_title').value;
let target = document.getElementById('chart_target').value;
let dstr = String(document.getElementById('chart_data').value);
let darr = dstr.split(',');
let dlabel = String(document.getElementById('chart_labels').value);
let larr = dlabel.split(',');
let ctx = document.getElementById('myChart').getContext('2d');

// 色の設定
var colorSet = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

// 色のRGB変換
var color = Chart.helpers.color;

let myRadarChart = new Chart(ctx, {
    type: 'radar',
    data: {
        labels: larr,
        datasets: [{
            data:darr,//app.pyのchart_data
            //backgroundColor: "rgba(255,0,0,0.2)", // 線の下の塗りつぶしの色
            //borderColor: "red",                   // 線の色
            //borderWidth: 2,                       // 線の幅
            //pointStyle: "circle",                 // 点の形状
            //pointRadius: 6,                       // 点形状の半径
            //pointBorderColor: "red",              // 点の境界線の色
            //pointBorderWidth: 2,                  // 点の境界線の幅
            //pointBackgroundColor: "yellow",       // 点の塗りつぶし色
            //pointLabelFontSize: 20,
            //label: target, //app.pyのchart_target
            
            backgroundColor: color(colorSet.red).alpha(0.5).rgbString(),    // 線の下の塗りつぶしの色
            borderColor: colorSet.red,                                      // 線の色
            pointBackgroundColor: colorSet.red                              // 点の塗りつぶし色

            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        
        /*
        title: {                // タイトル
            display: true,      // 表示する
            fontSize: 20,       // タイトルのフォント
            text: title         //app.pyのchart_title
        },
        */
        /*
        legend: {
            position: 'bottom', // 凡例の表示位置
            labels: {
                fontSize: 20,   // 判例のフォントサイズ
            },
        },
        */
        scale: {
            // スケールを隠す。
            display: true,      // メモリを表示する
            ticks: {            // 目盛り
                display: false,
                min: 0,         // 目盛りの最小値
                max: 3,        // 目盛りの最大値
                stepSize: 1,    // 目盛の間隔
                fontSize: 12,   // 目盛り数字の大きさ
                fontColor: colorSet.green   // 目盛り数字の色
            },
            pointLabels: {
                fontSize: 15,   // チャートラベルのフォントサイズ
                fontColor: colorSet.yello
            },
            /*
            angleLines: {        // 軸（放射軸）
                display: true,
                color: "maroon"
            },
            */
            gridLines: {         // 補助線（目盛の線）
                display: true,
                color: colorSet.yellow
            }
        },
    }
});

