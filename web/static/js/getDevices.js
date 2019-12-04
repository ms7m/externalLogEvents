
function checkBackup(metaData, switchName) {
    if (metaData.devicesBackup.devicesCompleted.includes(switchName)) {
        var stage_1 = document.createElement('a')
        stage_1.innerHTML = '<a class="button is-success is-pulled-right is-active">Success</a>'
        return stage_1
    } else if (metaData.devicesBackup.devicesFailed.includes(switchName)) {
        var stage_1 = document.createElement('a')
        stage_1.innerHTML = '<a class="button is-danger is-pulled-right is-active">Failed</a>'
        return stage_1
    } else {
        var stage_1 = document.createElement('a')
        stage_1.innerHTML = '<a class="button is-warning is-pulled-right is-active">API Error</a>'
        return stage_1
    }
}


function create_html(dict, metaData, switchName){
    var stage_1 = document.createElement('tr');
    stage_1.innerHTML = '<td width="5%"><i class="fas fa-server"></i></td>';
    var stage_2 = document.createElement('td');
    stage_2.textContent = dict.name;
    stage_1.append(stage_2);
    stage_3 = document.createElement('td');
    stage_4 = document.createElement('a');
    stage_4.classList.add('button', 'is-link', 'is-rounded', 'is-small');
    stage_4.textContent = dict.device;
    stage_3.append(stage_4);
    stage_3.append(checkBackup(metaData, switchName))
    stage_1.append(stage_3);
    return stage_1
};



function getDevices(){
    //var request = $.getJSON('http://127.0.0.1:8000/devices').request.responseJSON.backups;

    $.when( $.getJSON('http://localhost:8000/devices').then(function( responseJSON ) {
        var result_bin = document.getElementById('deviceList');
        document.getElementById('deviceLoading').remove()
        var loading_button = document.getElementById('deviceLoading')
        responseJSON.backups.forEach(item => {
            result_bin.append(create_html(item, responseJSON.metaData, item.name))
        });

        var deviceCount = document.getElementById('deviceCount');
        deviceCount.textContent = responseJSON.backups.length

        var exceptionCount = document.getElementById('exceptionCount')
        exceptionCount.textContent = responseJSON.metaData.devicesBackup.devicesFailed.length

        var totalCount = document.getElementById('totalDeviceCount')
        totalCount.textContent = responseJSON.metaData.devicesBackup.devicesCompleted.length
    }));
    //console.log(request)
    //var i;
    var result_bin = document.getElementById('devicesList');
    //let requestJSON = request.responseJSON
    //console.log(requestJSON)
    //var backupsList = requestJSON.backups
    //backupsList.forEach(function(obj) { 
    //    console.log(obj)
    //});
    }
    