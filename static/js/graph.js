//let title = document.getElementById('chart_title').value;
//let target = document.getElementById('chart_target').value;
let darr = []
let larr = []
for (let i = 0; i < 6; i++) {
    var str = 'chart_data' + i.toString();
    let dstr = String(document.getElementById(str).value);
    darr.push(dstr.split(','));

    var str = 'chart_labels' + i.toString();
    let dlabel = String(document.getElementById(str).value);
    larr.push(dlabel.split(','));
}

let ctx = []
for (let i = 0; i < 6; i++) {
    var str = 'siteChart' + i.toString();
    ctx.push(document.getElementById(str).getContext('2d'));
}

//ctx.push(document.getElementById("testChart").getContext('2d'));

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

for (let i = 0; i <6; i++) {
let myRadarChart = new Chart(ctx[i], {
    type: 'radar',
    data: {
        labels: larr[i],
        datasets: [{
            data:darr[i],//app.pyのchart_data
            
            backgroundColor: color(colorSet.red).alpha(0.5).rgbString(),    // 線の下の塗りつぶしの色
            borderColor: colorSet.red,                                      // 線の色
            pointBackgroundColor: colorSet.red                              // 点の塗りつぶし色

            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        
        legend: {
            display: false,     // 凡例を表示しない
            //position: 'bottom', // 凡例の表示位置
            labels: {
                //fontSize: 20,   // 判例のフォントサイズ
            },
        },
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
            gridLines: {         // 補助線（目盛の線）
                display: true,
                color: colorSet.yellow
            }
        },
    }
});
}
