$dashboard = (function() {
    var directory_tree = $('#tree');
    var configViewer = $('#configViewer');

    directory_tree.treeview({data: null});

    function getTree(){
        $.ajax({
            url: "http://localhost:5006/api/v1/tools/directory_tree"
        }).done(function (data) {
            directory_tree.treeview({
                data: data.data,
                levels: 5,
                onNodeSelected: function(event, data){
                    if (data.type == "file"){
                        getConfigFile(data.path);
                    }
                }
            });
        });
    }

    function getConfigFile(path){
        $.ajax({
            url: "http://localhost:5006/api/v1/tools/get_config_file",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"path": path})
        }).done(function (data) {
            console.log(data);
            configViewer.text(data.data);
        });
    }

    getTree();
})();