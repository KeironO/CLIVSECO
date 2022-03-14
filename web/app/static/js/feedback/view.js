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

    context = context.insert(end+1, "</span>")
    context = context.insert(start, "<span class='highlight'>")
    $("#context").html(context);
}

function fill_history(confirmations) {
    
    if (confirmations.length > 0) {
        $("#auto-coder-confirmation-none").remove();
    }

    for (i in confirmations) {
        let confirmation = confirmations[i];

        let email = confirmation["user"]["email"]
        if (confirmation["is_correct"]) {
            var is_correct = '✔️'
        }
        else {
            var is_correct = '❌'
        }

        var lgi = `<li class='list-group-item d-flex'>`

        var created_on = new Date(confirmation["created_on"]);

        lgi += `<p>Feedback Email: ${email}<br><span class='small'>Created On: ${created_on.toDateString()}</small></p>`
        lgi += `<span class="badge badge-primary badge-pill">${is_correct}</span>`

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
});