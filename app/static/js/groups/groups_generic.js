$dashboard = (function() {
    var groups_tree = $('#groups_tree');
    var folder_parent = $('#folder_parent');
    var folder_name = $('#folder_name');
    var addFolderBtn = $('#addFolderBtn');
    var deleteFolderBtn = $('#deleteFolderBtn');
    var groupMemberTable = $('#groupMemberTable');

    var root_dir = "";

    function getTree(){
      $.ajax({
          url: "http://localhost:5006/api/v1/tools/database_group_tree"
      }).done(function (data) {
          groups_tree.treeview({
              data: data.data,
              levels: 5,
              onNodeSelected: function(event, data){
                folder_parent.val(data.path);
                checkFolderAllowedInput();
                getGroupMembers();
            }
          });
      });
  }

  function createNewFolder(){
    if(folder_name.val() == null || folder_name.val() == ""){
      alert("Folder name must not be empty...");
      return;
    }
    $.ajax({
      url: "http://localhost:5006/api/v1/groups/",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        "name": folder_name.val(),
        "folder_path": folder_parent.val() + ";" + folder_name.val().toLowerCase()
      })
    }).done(function (data) {
      console.log(data);
      getTree();
    });
  }

  function deleteFolder(){
    $.ajax({
      url: "http://localhost:5006/api/v1/groups/",
      type: "DELETE",
      contentType: "application/json",
      data: JSON.stringify({
        "folder_path": folder_parent.val()
      })
    }).done(function (data) {
      console.log(data);
      getTree();
    });
  }

  function checkFolderAllowedInput(){
      if(folder_parent.val() != null || folder_parent.val() != ""){
          folder_name.removeAttr("disabled");
          addFolderBtn.removeAttr("disabled");
          deleteFolderBtn.removeAttr("disabled");
          return;
      }
      folder_name.attr("disabled", true);
      addFolderBtn.attr("disabled", true);
      deleteFolderBtn.attr("disabled", true);
  }

  function getGroupMembers(){
    $('#groupMemberTable tbody').empty();
    $.ajax({
      url: "http://localhost:5006/api/v1/groups/get_members",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        "folder_path": folder_parent.val()
      })
    }).done(function (data) {
        var devices = data.data[0].devices;
        if (devices == undefined || devices.length == 0){
          return;
        }

        var table_data = '';
        $.each(devices, function(index, device){
          console.log(device.friendly_name);
          table_data += '<tr>';
          table_data += '<td>'+device.friendly_name+'</td>';
          table_data += '</tr>';
        });

        groupMemberTable.append(table_data);
    });
  }

  addFolderBtn.on("click", function(e){
    e.preventDefault();
    createNewFolder();
  });

  deleteFolderBtn.on("click", function(e){
    e.preventDefault();
    deleteFolder();
  });

  getTree();
})();