$settings = (function() {
    var backupRootDir = $('#backupRootDir');
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
    });

    getAppConfig();
    toggleControls();
})();