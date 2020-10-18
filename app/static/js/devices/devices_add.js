$devices_add = (function() {
    var netmikodriver = $('#netmikodriver');
    var users = $('#users');
    var groups = $('#groups');

    var addDeviceBtn = $('#addDeviceBtn');

    function populateNetmikoDriversSelection(){
        $.ajax({
            url: "http://localhost:5006/api/v1/tools/netmiko_drivers"
        }).done(function (data){
            var netmiko_drivers = data.data;
            $.each(netmiko_drivers, function(item, val){
                netmikodriver.append($("<option />").val(val).text(val));
            });
        });
    }

    function populateUserSelection(){
        $.ajax({
            url: "http://localhost:5006/api/v1/users/"
        }).done(function (data){
            var users_data = data.data;
            $.each(users_data, function(index, item){
                users.append($("<option />").val(item.id).text(item.username));
            });
        });
    }

    function populateGroupSelection(){
        $.ajax({
            url: "http://localhost:5006/api/v1/groups/"
        }).done(function (data){
            var groups_data = data.data;
            $.each(groups_data, function(index, item){
                groups.append($("<option />").val(item.folder_path).text(item.folder_path));
            });
        });
    }

    function addDevice(){
        var btnDefaultVal = addDeviceBtn.val();
        var post_data = generate_device_json();
        addDeviceBtn.prop("disabled", true);
        addDeviceBtn.prop("value", "Please wait...")
        $.ajax({
            url: "http://localhost:5006/api/v1/devices/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(post_data)
        }).done(function (data){
            $('#debugOutput').html(JSON.stringify(data, undefined, 4));
            console.log(data);
        });
        addDeviceBtn.prop("disabled", false);
        addDeviceBtn.prop("value", btnDefaultVal)
    }

    function generate_device_json(){
        var json_data = {
            "friendly_name": $('#friendlyname').val(),
            "ip": $('#ipaddress').val(),
            "port": +$('#port').val(),
            "netmiko_driver": $('#netmikodriver').val(),
            "authentication_user": +$('#users').val(),
            "config_command": $('#configcommand').val(),
            "pre_commands": $('#precommands').val(),
            "assigned_group": $('#groups').val(),
            "description": null,
            "notes": null
        }

        var cleaned_json = clean_json(json_data);
        console.log(cleaned_json);
        return cleaned_json
    }

    function clean_json(obj){
        for (var propName in obj) { 
            if (obj[propName] === null || obj[propName] === undefined || obj[propName] == "") {
              delete obj[propName];
            }
        }

        return obj;
    }

    populateNetmikoDriversSelection();
    populateUserSelection();
    populateGroupSelection();

    addDeviceBtn.on("click", function(e){
        e.preventDefault();
        addDevice();
    });
})();