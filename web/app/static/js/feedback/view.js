const type_map = new Map();
type_map.set('DIA', 'discharge_diagnoses');
type_map.set('TRE', 'treatment_narrative');
type_map.set('ALL', 'allergy');
type_map.set('CLI', 'clinical_finding');
type_map.set('PRE', 'presenting_complaint');

const trans_map = new Map();
trans_map.set('DIAG', 'Discharge Diagnoses')


function get_code() {
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


function fill_code_information(code) {
    var code = code["note_code"];
    $("#code-header").html(code["code"] + ": " + code["code_information"]["description"]);
    $("#fid").html(code["code"]);
}

function show_hide_replace_element(value) {
    if (value == 1) {
        $("#remove-div").fadeOut(500);
    }
    else {
        $("#remove-div").fadeIn(500);
    }
}


function fill_context(code) {
    const type = code["section"];
    const text = type_map.get(type);

    var context = code["note_code"]["note"][text]
    
    const start = code["start"];
    const end = code["end"];

    $("#extracted").html("<span class='highlight'>" + code["source"] + "</span>");

    $("#context").html(context);
}

function fill_history(confirmations) {
    
    var cleared_confirmations = [];

    for (i in confirmations) {
        let confirmation = confirmations[i];
        if (confirmation["marked_as_deleted"] != true) {
            cleared_confirmations.push(confirmation)
        }
    }


    var confirmations = cleared_confirmations

    if (confirmations.length > 0) {
        $("#auto-coder-confirmation-none").remove();
    }

    for (i in confirmations) {
        let confirmation = confirmations[i];

        let email = confirmation["user_id"]
        if (confirmation["is_correct"]) {
            var is_correct = '✔️'
        }
        else {
            var is_correct = '❌'
        }

        var lgi = `<li class='list-group-item d-flex'>`

        var created_on = new Date(confirmation["created_on"]);
        var comments = confirmation["comments"]
        console.log(confirmation)

        lgi += '<div class="media">'
        lgi += '<div class="media-body">'
        lgi += '<div class="mr-3">' + is_correct + '</div>'
        lgi += '<div class="media-body">'
        lgi += `<h5 class="mt-0 mb-1">${email}:</h5>`
        lgi += `<p>Comments: ${comments}</p>`
        lgi += `<p>Additional Codes: ${confirmation['additional_codes']}</p>`
        lgi += `<p>Replace With: ${confirmation['replace_with']}</p>`
        lgi += `<small><p>Created On: ${created_on.toDateString()}</p></small>`

        lgi += '</div>'
        lgi += '</div>'
        lgi += '</div>'


        lgi += `</li>`

        $("#auto-coder-confirmation-list-group").append(lgi);
    }
}

function view_info_button(code) {
    $("#view-code-info").click( function() {
        if (code["note_code"]["type"] == "DIAG") {
            var icd10 = code["note_code"]["code"];
            window.open(`https://icdcodelookup.com/icd-10/codes/${icd10}`, '_blank'); 
        };
    })
}

$(document).ready(function () {
    var code = get_code()["content"];

    fill_context(code);

    $("#remove_or_replace").change(function() {
        show_hide_replace_element($(this).val());
    });

    $("#is_correct").change(function() {
        if ($(this).prop("checked")) {
            $("#wrong-div").fadeOut(500);
        }
        else {
            $("#wrong-div").fadeIn(500);
        }
    });

    $("#requires_additional_code").change(function() {
        if ($(this).prop("checked")) {
            $("#additional-code-div").fadeIn(500);
        }

        else {
            $("#additional-code-div").fadeOut(500);
        }
    })

    fill_code_information(code);
    fill_history(code["note_code"]["confirmations"]);
    view_info_button(code);

    $("#go-back").click(function() {
        window.location.href = code["note_code"]["note"]["_links"]["self"];
    });
});