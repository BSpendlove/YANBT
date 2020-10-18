$settings = (function() {
    var backupRootDir = $('#backupRootDir');
    var additionalSettingsDiv = $('#additionalSettings');
    var editSettingsBtn = $('#editSettingsBtn');
    var saveSettingsBtn = $('#saveSettingsBtn');

    var lock_config = true;

    function toggleControls(){
        console.log(lock_config);
        if (lock_config){
            backupRootDir.attr("disabled", true);
            editSettingsBtn.html('<i class="fas fa-lock p-1"></i>Edit');
            saveSettingsBtn.attr("disabled", false);
            return;
        }
        
        backupRootDir.attr("disabled", false);
        saveSettingsBtn.attr("disabled", true);
        editSettingsBtn.html('<i class="fas fa-lock-open p-1"></i></i>Editing');
    }

    function getAppConfig(){
        $.ajax({
            url: "http://localhost:5006/api/v1/config/"
        }).done(function (data){
            console.log(data);
            backupRootDir.val(data.data.backup_directory);
            additionalSettingsDiv.html('<p>App Version: ' + data.data.version + '</p>');
        });
    }

    function updateAppConfig(){
        var backup_dir = backupRootDir.val();
        if (backup_dir == null || backup_dir == "")
        {
            alert("Backup Directory field must not be empty...");
            return;
        }
        $.ajax({
            url: "http://localhost:5006/api/v1/config/",
            type: "PATCH",
            contentType: "application/json",
            data: JSON.stringify({
                "backup_directory": backup_dir
            })
        }).done(function (data){
            console.log(data);
            alert("Backup Directory has been updated...");
        });
    }

    editSettingsBtn.on("click", function(e){
        e.preventDefault();
        if (lock_config){
            lock_config = false;
        }
        else {
            lock_config = true;
        }
        toggleControls();
    });

    saveSettingsBtn.on("click", function(e){
        e.preventDefault();
        updateAppConfig();
    });

    getAppConfig();
    toggleControls();
})();