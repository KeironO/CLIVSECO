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

const clinically_coded_codes = new Map();


function dateDiffYearsOnly( dateNew,dateOld) {
    function date2ymd(d){ w=new Date(d);return [w.getFullYear(),w.getMonth(),w.getDate()]}
    function ymd2N(y){return (((y[0]<<4)+y[1])<<5)+y[2]} // or 60 and 60 // or 13 and 32 // or 25 and 40 //// with ...
    function date2N(d){ return ymd2N(date2ymd(d))}
 
    return  (date2N(dateNew)-date2N(dateOld))>>9
 }

function get_note() {

    var api_url = encodeURI(window.location.origin + '/notes/get/'  + $("#note-heading").html() );

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

function set_heading(caseno, linkid) {
    document.title = caseno + ":" + linkid + " : CLIVSECO";

}

function set_dates(note) {
    $("#discharge-date").html(note["discharge_date"]);
    $("#admission-date").html(note["admission_date"]);
    $("#date-of-birth").html(note["dob"]);
    $("#spec-name").html(note["spec_name"]);

}

function if_nothing_then_none(s) {
    if (s == null) {
        return "None."
    } 
    return s
 }



function set_content(note) {
    $("#age").text(note["age"]);
    $("#m-number").text(note["m_number"]);
    $("#admission-spec").text(note["admission_spec"]);
    $("#discharge-spec").text(note["discharge_spec"]);

    var ad = new Date(note["admission_date"]);
    var dd = new Date(note["discharge_date"]);

    $("#los").text(Math.abs(ad-dd) / 86400000);
    $("#episode-count").text(note["episode_count"]);
    $("#presenting-complaint-text").text(if_nothing_then_none(note["presenting_complaint"]));
    $("#clinical-finding-text").text(if_nothing_then_none(note["clinical_finding"]));
    $("#treatment-narrative-text").text(if_nothing_then_none(note["treatment_narrative"]));
    $("#allergy-text").text(if_nothing_then_none(note["allergy"]));
    $("#discharge-diagnosis-1-text").text(if_nothing_then_none(note["discharge_diagnosis_1"]));
    $("#discharge-diagnosis-2-text").text(if_nothing_then_none(note["discharge_diagnosis_2"]));
    $("#edal-unique-id").text(if_nothing_then_none(note["dal_id"]));
}



function highlight_text(div, start, end) {
    var contents = $("#" + div ).html();
    contents = contents.insert(end+1, "</span>")
    contents = contents.insert(start, "<span class='highlight'>")
    $("#" + div ).html(contents);
}

function highlight_code(div) {
    $(`#${div}`).addClass( "codehighlight" );
}

function unhighlight_code(div) {
    $(`#${div}`).removeClass( "codehighlight" );

}

function unhighlight_text(div) {
    $('#' + div ).find('span').contents().unwrap();
}

function set_auto_coder(auto_codes) {

    if (auto_codes.length > 0) {
        $("#auto-coder-none").remove();
    }

    var pmhs = [];
    var diag = [];
    var fmhs = [];
    var com = [];
    var other = [];
    var procs = [];

    var unvalidated = 0

    for (i in auto_codes) {
        let code = auto_codes[i]
        if (code["note_code"]["confirmations"].length == 0) {
            unvalidated += 1
        };

        if (code["note_code"]["type"] == "PROC") {
            procs.push(code)
        }

        else if (code["comorbidity"]) {
            com.push(code);
        }

        else if (code["dia"]) {
            diag.push(code);
        }

        else if (code["pmh"]) {
            pmhs.push(code);
        }

        else if (code["fmh"]) {
            fmhs.push(code);
        }

        

        else {
            other.push(code);
        }

        console.log(code)
    }

    if (unvalidated) {
    }

    else {
        $("#jph").css('background-color', '#198754');
    }
    

    var final_array = [];
    final_array.push(diag);
    final_array.push(com);
    final_array.push(other);
    final_array.push(pmhs);
    final_array.push(fmhs);
    final_array.push(procs);

    for (j in final_array) {
        var yearofthesmile = final_array[j];
    
        for (i in yearofthesmile) {
            let code = yearofthesmile[i];
    
            let note_code = code["note_code"];
            
            if (note_code["type"] == "DIAG") {
                var bg = "bg-danger text-white"
            }
    
            else {
                var bg = "bg-warning"
            }
            

            lgi = "<li class='list-group-item list-group-item-action flex-column align-items-start "+ bg + "' id='gi-"+ note_code["id"] + "'>"
            lgi += '<div class="d-flex w-100 justify-content-between">'

    
            lgi += '<h5 class="mb-1">' + note_code["code"] + ": " + note_code["code_information"]["description"] 
            if (code["comorbidity"] == true) {
                lgi += ' ✨ '
            }
    
            if (code["dia"] == true) {
                lgi += ' 👨🏼‍⚕️ '
            }
    
            if (code["acr"] == true) {
                lgi += ' 🎈 '
    
            }
    
            if (code["pmh"] == true) { 
                lgi += ' 🛌🏼 '
            }
    
            if (code["fmh"]) {
                lgi += ' 👵 '
            }
    
            if (code["daa"]) {
                lgi += ' 🗡️ '
            }

            lgi += '</h5>'
            

            var confirmations = note_code["confirmations"];
            var cleared_confirmations = []
            for (i in confirmations) {
                let confirmation = confirmations[i];
                if (confirmation["marked_as_deleted"] != true) {
                    cleared_confirmations.push(confirmation)
                }
            }
            lgi += '<small>'+cleared_confirmations.length+'</small>'
            lgi += '</div><p class="mb-1">'
            lgi += '<small><div class="btn btn-light btn-sm">' + code["source_id"] + '</div></small></div>'          
            lgi += "</li>"


    
            $("#auto-coder-list-group").append(
                lgi
            );
    
 
    
            $("#gi-"+ note_code["id"]).click(function() {
                window.location = code['_links']['feedback']; 
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

    
}

function set_clinical_coder(clinical_codes) {
    if (clinical_codes.length > 0) {
        $("#clinical-coder-none").remove();
    }

    for (i in clinical_codes) {
        
        let code = clinical_codes[i];
        let ccid = code["id"];
        let note_code = code["note_code"];

        if (note_code["type"] == "DIAG") {
            var bg = "bg-danger text-white"
            var edal_code = "d"+zeroPad(code["code_number"],2)

        }

        else {
            var bg = "bg-warning"
            var edal_code = "p"+zeroPad(code["code_number"],2)

        }


        var lgi = `<li id="cc${ccid}" class='list-group-item d-flex justify-content-between align-items-center ${bg}'>`
        lgi += `${note_code["code"]}: ${note_code["code_information"]["description"]}<span class="badge badge-primary badge-pill">${edal_code}</span>
        `
        lgi += `</li>`

        clinically_coded_codes.set(note_code["code"], `cc${ccid}`);

        $("#clinical-coder-list-group").append(lgi);

        

    }
}


function set_missing_code(missing_codes) {
    if (missing_codes.length > 0) {
        $("#missing-codes-none").remove();
    }

    for (i in missing_codes) {
        let mc = missing_codes[i];
        let codes = mc["code"].split(",");

        if (mc["type"] == "DIAG") {
            var bg = "bg-danger text-white"
        }


        else {
            var bg = "bg-warning"
        }

        var lgi = `<li id='miss-${mc["id"]}' class='list-group-item ${bg}'>`
        if (mc["comorbidity"] == true) {
            lgi += '✨'
        }
        
        for (j in codes) {
            var code = codes[j];
            lgi += `<span class="badge bg-secondary" style="margin-right:0.5em">${code}</span>`
        }

        lgi += `<p class="small">Feedback User: ${mc["user_id"]}</p>`
        lgi += `<p class="small">Created On: ${mc["created_on"]}</p>`

        lgi += "</li>"

        $("#missing-codes-list-group").append(
            lgi
        );

        $(`#miss-${mc["id"]}`).hover(function() {
            highlight_text(div_map.get(mc["section"]), mc["start"], mc["end"]);
        }, function() {
            unhighlight_text(div_map.get(mc["section"]));
        });

    }
}

function fill_missing_code_information(note) {
    var text_div = div_map.get($("#section option:selected").val());
    var text = $(`#${text_div}`)[0].innerHTML;
    $( "#start" ).val(0);
    $( "#end" ).val(0);
    $("#additional-codes-text").html(text);
}


document.getElementById("additional-codes-text").addEventListener('mouseup', function () {
    if (typeof window.getSelection != 'undefined') {
        var sel = window.getSelection();
        var range = sel.getRangeAt(0);
  
        var startOffset = range.startOffset;
        var endOffset = startOffset + range.toString().length - 1;
        
        $("#start").val(startOffset);
        $("#end").val(endOffset);
        unhighlight_text("additional-codes-text")
        highlight_text("additional-codes-text", startOffset, endOffset);

    }
  }, false);


function set_letters(clinic_letters) {

    $("#dal-nav").click(function () {
        $("#nav-tab-selection").parent().find('a').removeClass("active");
        $(this).addClass("active");
        $("#cls").fadeOut(500);
        $("#edal").fadeIn(500);

    });

    const clcontents = new Map();


    for (i in clinic_letters) {
        var letter_info = clinic_letters[i];
        
        $("#nav-tab-selection").append(`<li class="nav-item">
            <a class="nav-link" id="${letter_info["letter_key"]}-nav">✉️ CL: ${letter_info["letter_key"]} </a>
        </li>`)
        
        clcontents.set(letter_info["letter_key"], letter_info["letter_contents"]);

        $(`#${letter_info["letter_key"]}-nav`).click( function() {
            $("#nav-tab-selection").parent().find('a').removeClass("active");
            $(this).addClass("active");
            var clk = this.id.split('-')[0]
            $("#clinical-letter-key").text(`${letter_info["letter_key"]}`);
            $("#letter-text").html(`${clcontents.get(clk).replace(/\n/g,'<br/>')}`);
            $("#edal").fadeOut(500);
            $("#cls").fadeIn(500);

        });
    }
}

function audit_results(audit) {
    console.log(audit.length)
    if (audit.length >= 1) {
        $("#audit-section").attr('style', 'display:block');
    }

    for (a in audit) {
        var audit_result = audit[a];
        
        console.log(audit_result);

        var lgi = `<li class="list-group-item d-flex justify-content-between align-items-start">`;

        lgi += `<div class="ms-2 me-auto">`
        lgi += `<div class="fw-bold">${audit_result['author']}</div>`
        lgi += `<p>Diagnoses: ${audit_result['diagnoses']} .. Procedures: ${audit_results['procedures']}</p>`
        if (audit_result['coders_note'].length > 1) {
            lgi += `<p>Coders Note: ${audit_result['coders_note']}</p>`

        }
        lgi += `</div>`
        lgi += `<span class="badge bg-primary rounded-pill">${audit_result['created_on']}</span>`

        lgi += `</li>`


        $("#audit-list").append(lgi);
    }
}


$(document).ready(function () {
    var note = get_note()["content"];
 
    set_heading(note["m_number"], note["linkid"]);
    set_dates(note);
    set_content(note);

    if (note["clinical_coder_codes"].length >= 1) {
        set_clinical_coder(note["clinical_coder_codes"]);
    }

    else {

        $("#clinical-code-col").remove()
        $("#note-information-col").removeClass("col-6").addClass("col-8");
        $("#auto-code-row").removeClass("col-3").addClass("col-4");
        set_auto_coder(note["auto_codes"]);

    }

    fill_missing_code_information(note);
    set_missing_code(note["missing_codes"]);
    set_letters(note["clinic_letters"]);
    audit_results(note["audit"]);

    $("#loading").fadeOut(250, function() {
        $("#content").fadeIn(250);

    });

    $("#section").change(function() {
        fill_missing_code_information(note);
    });

    if (note["audit"].length >= 1) { 
        $("#jph").css('background-color', '#198754');
    }
    else {
    }
});