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
        columns: [
        { mData: function (data, type, row ) {
            return '<a href="'+data["note_code"]["note"]["_links"]["self"]+'"><div class="btn btn-success btn-sm">' +data["note_code"]["note"]["m_number"] +':' + data["note_code"]["note"]["linkid"] +'</div></a>'
        }},
        { mData: function (data, type, row ) {
            return "FBK:" + data["note_code"]["note_id"]
        }},
        { mData: function (data, type, row) {
            return data["note_code"]["code"]
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
        }},
        { mData: function (data, type, row) {
           return data["user_id"]
        }},
        { mData: function (data, type, row) {
           return data["created_on"]
        }},
        { mData: function (data, type, row) {
            return '<a href="'+ data["_links"]["remove"]+ '"><div class="btn btn-danger btn-sm">Delete</div></a>'
         }}
     ]
    });

    console.log(codes)
});