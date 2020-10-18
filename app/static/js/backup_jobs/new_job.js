$devices_add = (function() {
    var groups = $('#groups');
    var start_date_time = $('#start_date_time');
    var end_date_time = $('#end_date_time');
    var weekdays = $('#weekdays');

    function populateGroupSelection(){
        $.ajax({
            url: "http://localhost:5006/api/v1/groups/"
        }).done(function (data){
            var groups_data = data.data;
            $.each(groups_data, function(index, item){
                groups.append($("<option />").val(item.id).text(item.folder_path));
            });
        });
    }

    populateGroupSelection();
    start_date_time.datepicker();
    end_date_time.datepicker();
})();