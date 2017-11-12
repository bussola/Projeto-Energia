// Contem funções para charts do morris.js

function bindDonut(nome_chart, dados) {
    console.log('------------------------------------------------------- Donut');
    Morris.Donut({
        element: nome_chart,
        data: dados,
        backgroundColor: '#ccc',
        labelColor: '#025D8C',
        colors: [
            '#025D8C',
            '#107FC9',
            '#0A93FC',
            '#73C2FF'
        ],
        xKey: 'label',
        formatter: function (x) { return x.toFixed(2)}
    });
}

function bindLines(nome_chart, dados, xKey, yKeys, labels) {
    console.log('------------------------------------------------------- Lines');
    Morris.Line({
        element: nome_chart,
        data: dados,
        xkey: xKey,
        ykeys: yKeys,
        labels: labels,
        parseTime: false
    });
}

function bindBar(nome_chart, dados, xKey, yKeys, labels) {
    console.log('------------------------------------------------------- Bar');
    Morris.Bar({
        element: nome_chart,
        data: dados,
        xkey: xKey,
        ykeys: yKeys,
        labels: labels
    });
}