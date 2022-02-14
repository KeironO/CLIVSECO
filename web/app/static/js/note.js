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
    console.log(dal_id);
    document.title = dal_id + " : CLIVSECO";
    $("#note-heading").html(dal_id);
}


function set_content(note) {
    console.log(note["discharge_diagnoses"]);
    $("#presenting-complaint-text").append(note["presenting_complaint"]);
    $("#clinical-finding-text").append(note["clinical_finding"]);
    $("#treatment-narrative-text").append(note["treatment_narrative"]);
    $("#allergy-text").append(note["allergy"]);
    $("#discharge-diagnoses-text").append(note["discharge_diagnoses"]);
}

$(document).ready(function () {
    var note = get_note()["content"];

    set_heading(note["dal_id"]);
    set_content(note);
});