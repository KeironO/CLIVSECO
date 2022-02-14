String.prototype.insert = function(index, string) {
    if (index > 0) {
      return this.substring(0, index) + string + this.substr(index);
    }
  
    return string + this;
};

const div_map = new Map();

div_map.set('DIA', 'discharge-diagnoses-text')
div_map.set('TRE', 'treatment-narrative-text')
div_map.set('CLI', 'clinical-finding-text')
div_map.set('PRE', 'presenting-complaint-text')

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
    $("#presenting-complaint-text").text(note["presenting_complaint"]);
    $("#clinical-finding-text").text(note["clinical_finding"]);
    $("#treatment-narrative-text").text(note["treatment_narrative"]);
    $("#allergy-text").text(note["allergy"]);
    $("#discharge-diagnoses-text").text(note["discharge_diagnoses"]);
}



function highlight_text(div, start, end) {
    var contents = $("#" + div ).html();
    contents = contents.insert(end+1, "</span>")
    contents = contents.insert(start, "<span class='highlight'>")
    $("#" + div ).html(contents);
}

function unhighlight_text(div) {
    $('#' + div ).find('span').contents().unwrap();
}

function set_auto_coder(auto_codes) {

    if (auto_codes.length > 0) {
        $("#auto-coder-none").remove();
    }

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
            "<li class='list-group-item " + bg + "' id='gi-"+ note_code["id"] + "'>" + note_code["code"] + ": " + note_code["code_information"]["description"] + "</li>"
        );

        $("#gi-"+ note_code["id"]).hover(function() {
            highlight_text(div_map.get(code["section"]), code["start"], code["end"]);
        }, function() {
            unhighlight_text(div_map.get(code["section"]))
        });

        $("#gi-"+ note_code["id"]).click(function() {
            window.open(code['_links']['feedback'], '_blank'); 
        });
    }
}

function set_clinical_coder(clinical_codes) {
    if (clinical_codes.length > 0) {
        $("#clinical-coder-none").remove();
    }

    for (i in clinical_codes) {
        let code = clinical_codes[i];
        let note_code = code["note_code"]

        if (note_code["type"] == "DIAG") {
            var bg = "bg-danger text-white"
        }

        else {
            var bg = "bg-warning"
        }

        $("#clinical-coder-list-group").append(
            "<li class='list-group-item " + bg + "' id='gi-"+ note_code["id"] + "'>" + note_code["code"] + "</li>"
        );

    }
}

$(document).ready(function () {
    var note = get_note()["content"];
    set_heading(note["dal_id"]);
    set_content(note);
    set_auto_coder(note["auto_codes"]);
    set_clinical_coder(note["clinical_coder_codes"]);
});