$users = (function() {
    var usersTable = $('#usersTable');
    var usernameBox = $('#username');
    var passwordBox = $('#password');
    var addUserBtn = $('#addUserBtn');

    function addUser(){
        var btnDefaultVal = addUserBtn.val();

        addUserBtn.prop('value', 'Please wait...');
        addUserBtn.prop('disabled', true);
        $.ajax({
            url: "http://localhost:5006/api/v1/users/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "username": usernameBox.val(),
                "password": passwordBox.val()
            })
        }).done(function(data){
            updateUsersTable(data);
            addUserBtn.prop('value', btnDefaultVal);
            addUserBtn.prop('disabled', false);
        });
        addUserBtn.prop('value', btnDefaultVal);
        addUserBtn.prop('disabled', false);
    }

    function populateUsersTable(){
        $.ajax({
            url: "http://localhost:5006/api/v1/users/"
        }).done( function(data){
            var users = data.data;
                console.log(users);
                if (users == undefined || users.length == 0){
                    return;
                }

                var table_data = '';

                $.each(users, function(index, user){
                    table_data += '<tr>';
                    table_data += '<td>'+user.id+'</td>';
                    table_data += '<td>'+user.username+'</td>';
                    table_data += '<td>'+user.password+'</td>';
                    table_data += '<td>'+user.devices.length+'</td>';
                    table_data += '</tr>';
                });

                usersTable.append(table_data);
        });
    }

    function updateUsersTable(user){
        var table_data = '';
        table_data += '<tr>';
        table_data += '<td>'+user.id+'</td>';
        table_data += '<td>'+user.username+'</td>';
        table_data += '<td>'+user.password+'</td>';
        table_data += '<td>'+user.devices.length+'</td>';
        table_data += '</tr>';

        usersTable.append(table_data);
    }

    function clearUsersTable(){
        $("#usersTable tr").remove();
    }

    addUserBtn.on("click", function(e){
        e.preventDefault();
        addUser();
    });

    populateUsersTable();
})();