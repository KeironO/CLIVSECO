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

$(document).ready(function () {
    var code = get_code()["content"];

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

    fill_code_information(code);
});