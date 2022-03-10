const type_map = new Map();
type_map.set('DIAG', 'discharge_diagnoses');
type_map.set('TRE', 'treatment_narrative');
type_map.set('ALL', 'allergy');
type_map.set('CLI', 'clinical_finding');
type_map.set('PRE', 'presenting_complaint');

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

String.prototype.insert = function(index, string) {
    if (index > 0) {
      return this.substring(0, index) + string + this.substr(index);
    }
  
    return string + this;
};


function fill_context(code) {
    const type = code["note_code"]["type"];
    const text = type_map.get(type);

    var context = code["note_code"]["note"][text]
    
    const start = code["start"];
    const end = code["end"];

    context = context.insert(end+1, "</span>")
    context = context.insert(start, "<span class='highlight'>")
    $("#context").html(context);
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
});