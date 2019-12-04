function exportCSVFile(headers, items, fileTitle) {
    if (headers) {
        items.unshift(headers);
    }

    // Convert Object to JSON
    var jsonObject = JSON.stringify(items);

    var csv = this.convertToCSV(jsonObject);

    var exportedFilenmae = fileTitle + '.csv' || 'export.csv';

    var blob = new Blob([csv], {
        type: 'text/csv;charset=utf-8;'
    });
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, exportedFilenmae);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", exportedFilenmae);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
};

function convertToCSV(objArray) {
    var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    var str = '';

    for (var i = 0; i < array.length; i++) {
        var line = '';
        for (var index in array[i]) {
            if (line != '') line += ','

            line += array[i][index];
        }

        str += line + '\r\n';
    }

    return str;
};

function genCSV(responseJSON) {
    var headers = {
        name: 'Hostname',
        ip: 'IP',
        pass: 'AuthType',
        device: 'DeviceType'
    }

    var results = []
    let fileTitle = "exported"

    var getButton = document.getElementById('exportButtonAvailablity')
    var retryButton = document.getElementById('retryExportButton')

    getButton.text = "Preparing.."
    retryButton.classList.add('is-loading')
    try {
        responseJSON.backups.forEach(element => {
            results.push({
                name: element.name,
                ip: element.ip,
                pass: element.pass,
                device: element.device
            })
        })
    } catch (error) {
        getButton.classList.remove('is-dark')
        getButton.classList.add('is-danger')
        getButton.textContent = error
    }

try {
    exportCSVFile(headers, results, fileTitle);
    getButton.removeAttribute('disabled');
    getButton.classList.remove('is-dark');
    retryButton.classList.add('is-hidden');
    getButton.classList.add('is-success');
    getButton.textContent = "Completed..";
} catch (error) {
    getButton.classList.remove('is-dark');
    getButton.classList.add('is-danger');
    getButton.textContent = error
}}


function badError(message) {
    var getButton = document.getElementById('exportButtonAvailablity')
    var retryButton = document.getElementById('retryExportButton')
    getButton.removeAttribute('disabled')
    getButton.classList.remove('is-dark')
    getButton.classList.add('is-danger')
    retryButton.classList.add('is-hidden')
    getButton.textContent = message
};

function buttonExport() {
    var getButton = document.getElementById('exportButtonAvailablity')
    var retryButton = document.getElementById('retryExportButton')

    getButton.text = "Contacting API.."
    retryButton.classList.add('is-loading')
    $.ajax({
        url: 'http://127.0.0.1:8000/devices',
        dataType: 'json',
        success: function (data) {
            genCSV(data);
        },
        error: function (data) {
            badError("Could not connect to API.");
        }
    })
}