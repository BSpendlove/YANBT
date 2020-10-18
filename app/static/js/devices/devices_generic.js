$devices = (function() {
    var devicesTable = $('#devicesTable');

    function populateDevicesTable(){
        $.ajax({
            url: "http://localhost:5006/api/v1/devices/"
        }).done( function(data){
            var devices = data.data;
                console.log(devices);
                if (devices == undefined || devices.length == 0){
                    return;
                }

                var table_data = '';

                $.each(devices, function(index, device){
                    table_data += '<tr>';
                    table_data += '<td>'+device.id+'</td>';
                    table_data += '<td>'+device.friendly_name+'</td>';
                    table_data += '<td>'+device.ip+'</td>';
                    table_data += '<td>'+device.port+'</td>';
                    table_data += '<td>'+device.netmiko_driver+'</td>';
                    table_data += '<td>'+device.authentication_user+'</td>';
                    table_data += '<td>'+device.assigned_group+'</td>';
                    table_data += '</tr>';
                });

                devicesTable.append(table_data);
        });
    }

    populateDevicesTable();
})();