
function getDevices() {
    //var request = $.getJSON('http://127.0.0.1:8000/devices').request.responseJSON.backups;
    $.when($.getJSON('http://localhost:8000/devices').then(function (responseJSON) {
        var result_bin = document.getElementById('deviceList');
        var loading_button = document.getElementById('deviceLoading')
        responseJSON.backups.forEach(item => {
            result_bin.append(create_html(item, responseJSON.metaData, item.name))
        });
    }));

};

function getAllLogs() {
    $("#allLogs").load("/load/logs");
}
function getLatestLog() {
    $("#latestLogOutput").load("/load/latest/log");
}

function both() {
    getAllLogs();
    getLatestLog();
}

function start() {
    function refreshData() {
        x = 10;  

        both();
        setTimeout(refreshData, x * 1000);
    };


    refreshData()};