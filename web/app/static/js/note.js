function get_note() {
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

function set_heading(dal_id) {
    document.title = dal_id + " : CLIVSECO";
    $("#note-heading").html(dal_id);
}


function set_content(note) {
    $("#presenting-complaint-text").append(note["presenting_complaint"]);
    $("#clinical-finding-text").append(note["clinical_finding"]);
    $("#treatment-narrative-text").append(note["treatment_narrative"]);
    $("#allergy-text").append(note["allergy"]);
    $("#discharge-diagnoses-text").append(note["discharge_diagnoses"]);
}

function set_auto_coder(auto_codes) {
    for (i in auto_codes) {
        let code = auto_codes[i];
        let note_code = code["note_code"];
        
        if (note_code["type"] == "DIAG") {
            var bg = "bg-danger text-white"
        }

        else {
            var bg = "bg-warning"
        }

        $("#auto-coder-list-group").append(
            "<li class='list-group-item " + bg + "'>" + note_code["code"] + "</li>"
        );
    }
}

$(document).ready(function () {
    var note = get_note()["content"];

    set_heading(note["dal_id"]);
    set_content(note);
    set_auto_coder(note["auto_codes"]);
});