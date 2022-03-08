function get_codes() {
    var api_url = encodeURI(window.location + '/endpoint');

    var json = (function () {
        var json = null;
        $.ajax({
            'async': false,
            'global': false,
            'url': api_url,
            'dataType': "json",
            'success': function (data) {
                json = data;
            },
            'failure': function (data) {
                json = data;
            }
            
        });
        return json;
    })();
    return json;
}


$(document).ready(function () {
    var codes = get_codes()["content"];
    $('#feedback-table').DataTable({
        data: codes,
        columns: [{
            data: 'id'
        },
        { mData: function (data, type, row ) {
            return data["note_code"]["code"] + ": " + data["note_code"]["code_information"]["description"]
        }},
        { mData: function (data, type, row) {
            if (data["is_correct"]) {
                return "✅"
            }
            else {
                return "❌"
            }
        }},
        { mData : function (data, type, row) {
            if (data["replace_with"] != "") {
                return "✅"
            }
            else {
                return "❌"
            }
        }} ]
    });

    console.log(codes)
});