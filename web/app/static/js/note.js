String.prototype.insert = function(index, string) {
    if (index > 0) {
      return this.substring(0, index) + string + this.substr(index);
    }
  
    return string + this;
};

const zeroPad = (num, places) => String(num).padStart(places, '0')


const div_map = new Map();
div_map.set('DIA', 'discharge-diagnoses-text');
div_map.set('TRE', 'treatment-narrative-text');
div_map.set('ALL', 'allergy-text');
div_map.set('CLI', 'clinical-finding-text');
div_map.set('PRE', 'presenting-complaint-text');

const filter_map = new Map();
filter_map.set('DIA', 'discharge-diagnosis-checkbox');
filter_map.set('TRE', 'treatment-narrative-checkbox');
filter_map.set('CLI', 'clinical-finding-checkbox');
filter_map.set('ALL', 'allergy-checkbox');
filter_map.set('PRE', 'presenting-complaint-checkbox');

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

function set_dates(note) {
    $("#discharge-date").html(note["discharge_date"]);
    $("#admission-date").html(note["admission_date"]);
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

    // TODO: Need to remove duplicates in the view and have them displayed as different entities.

    if (auto_codes.length > 0) {
        $("#auto-coder-none").remove();
    }

    for (i in auto_codes) {
        let code = auto_codes[i];
        let note_code = code["note_code"];
        
        console.log(code);

        if (note_code["type"] == "DIAG") {
            var bg = "bg-danger text-white"
        }

        else {
            var bg = "bg-warning"
        }

        var lgi = "<li class='list-group-item d-flex justify-content-between align-items-center "+ bg + "' id='gi-"+ note_code["id"] + "'>"
        lgi += note_code["code"] + ": " + note_code["code_information"]["description"]
        if (code["comorbidity"] == true) {
            lgi += '<span class="badge badge-primary badge-pill">COMORB</span>'
        }
        lgi += "</li>"

        $("#auto-coder-list-group").append(
            lgi
        );

        $("#gi-"+ note_code["id"]).hover(function() {
            highlight_text(div_map.get(code["section"]), code["start"], code["end"]);
        }, function() {
            unhighlight_text(div_map.get(code["section"]))
        });

        $("#gi-"+ note_code["id"]).click(function() {
            window.open(code['_links']['feedback'], '_blank'); 
        });

        $("#"+filter_map.get(code["section"])).click(function() {
            var checked = this.checked
            if (checked) {
                $("#gi-"+ note_code["id"]).fadeIn(500);
            }
            
            else {
                $("#gi-"+ note_code["id"]).fadeOut(500);
            }
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
            var edal_code = "d"+zeroPad(code["code_number"],2)

        }

        else {
            var bg = "bg-warning"
            var edal_code = "p"+zeroPad(code["code_number"],2)

        }


        var lgi = `<li class='list-group-item d-flex justify-content-between align-items-center ${bg}'>`
        lgi += `${note_code["code"]}: ${note_code["code_information"]["description"]}<span class="badge badge-primary badge-pill">${edal_code}</span>
        `
        lgi += `</li>`

        $("#clinical-coder-list-group").append(lgi);

    }
}

$(document).ready(function () {
    var note = get_note()["content"];
    set_heading(note["dal_id"]);
    set_dates(note);
    set_content(note);
    set_auto_coder(note["auto_codes"]);
    set_clinical_coder(note["clinical_coder_codes"]);
});