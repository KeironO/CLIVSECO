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


function get_opcs4(opcs4) {

    var api_url = encodeURI(window.location.origin + '/api/code/OPCS4/'  + opcs4 );

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


function get_icd10(icd10) {

        var api_url = encodeURI(window.location.origin + '/api/code/ICD10/'  + icd10 );
    
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


var icd10_audit_results = [];
var opcs49_audit_results = [];

var icd10s = [];
var opcs49s = [];

var lookup_dict = {}

function rebuild_audit_icd10_results_view() {


    

    $("#auditiedIcd10").empty();


    if (icd10_audit_results.length == 0) {
        var lgi = `<li class='list-group-item' data-id='None'>No Diagnoses Added</li>`
        $("#auditiedIcd10").append(lgi)
    }

        for (indx in icd10_audit_results) {
            var icd10 = icd10_audit_results[indx]
            var icd10_lookup = get_icd10(icd10);
            
            var lgi = `<li class='list-group-item d-flex justify-content-between align-items-start' data-id=${icd10}>`
    
            if (icd10_lookup["success"]) {
                lgi += `${icd10}: ${icd10_lookup["content"]["description"]}`
                lgi += `<div id="${icd10}_delete" class="btn btn-danger btn-sm pull-right">-</div> `
            }

            lgi += "</div></li>"
       
            $("#auditiedIcd10").append(lgi)        
            $("#"+icd10+'_delete').click(function() {
                var icd10 = this.id.split('_')[0];
                var index = icd10_audit_results.indexOf(icd10);
                icd10_audit_results.splice(index, 1);
                rebuild_audit_icd10_results_view();
            });
    
        }    
}

function rebuild_audit_opcs40_results_view() {
    $("#auditiedOpcs4").empty();


    if (opcs49_audit_results.length == 0) {
        var lgi = `<li class='list-group-item d-flex justify-content-between align-items-start' data-id='None'>No Procedures Added</li>`
        $("#auditiedOpcs4").append(lgi)
    }

    for (indx in opcs49_audit_results) {
        var opcs4 = opcs49_audit_results[indx];
        var opcs4_lookup = get_opcs4(opcs4);

        var lgi = `<li class='list-group-item d-flex justify-content-between align-items-start' data-id='${opcs4}-${indx}'>`
        if (opcs4_lookup["success"]) {
            lgi += `${opcs4}: ${opcs4_lookup["content"]["description"]}`
            lgi += `<div id="${opcs4}_${indx}_delete" class="btn btn-danger btn-sm pull-right">-</div> `

        }

        lgi += "</div></li>"
        $("#auditiedOpcs4").append(lgi)


        $(`#${opcs4}_${indx}_delete`).click(function() {
            var opcs4 = this.id.split('_')[0];
            var index = this.id.split('_')[1]
            opcs49_audit_results.splice(index, 1);
            rebuild_audit_opcs40_results_view();
        })

    }
}


function fill_autocoded_diagnosis(note) {

    
    for (i in note["auto_codes"]) {
        var ac = note["auto_codes"][i];
        if (ac["note_code"]["type"] == "DIAG") {
            icd10s.push(ac)
        }
    }


    if (icd10s.length == 0) {
        var lgi = `<li class='list-group-item' data-id='None'>No Diagnoses Found</li>`
        $("#autocodedIcd10").append(lgi)
    }

    icd10s.sort((a, b) => (a.position, b.position));

    for (i in icd10s) {
        var ac = icd10s[i];

        var lgi = `<li id='ac_${ac["note_code"]["code"]}' class='list-group-item'>`
        lgi += `${ac["note_code"]["code"]}: ${ac["note_code"]["code_information"]["description"]}`
        lgi += `</li>`

        $("#autocodedIcd10").append(lgi)

        $(`#ac_${ac["note_code"]["code"]}`).click(function() {
            var icd10 = this.id.split('_')[1];
            add_icd10_to_audit(icd10);
        });

    }
    
}

function fill_autocoded_procedures(note) {
    for (i in note["auto_codes"]) {
        var ac = note["auto_codes"][i];
        if (ac["note_code"]["type"] == "PROC") {
            opcs49s.push(ac)
        }
    }

    opcs49s.sort((a, b) => (a.position, b.position));


    if (opcs49s.length == 0) {
        var lgi = `<li class='list-group-item' data-id='None'>No Procedures Found</li>`
        $("#autocodedOpcs4").append(lgi)
    }

    for (i in opcs49s) {
        var ac = opcs49s[i];

        var lgi = `<li id='ac_proc_${ac["note_code"]["code"]}' class='list-group-item'>`
        lgi += `${ac["note_code"]["code"]}: ${ac["note_code"]["code_information"]["description"]}`
        lgi += `</li>`

        $("#autocodedOpcs4").append(lgi)

        $(`#ac_proc_${ac["note_code"]["code"]}`).click(function() {
            var opcs49 = this.id.split('_')[2];
            add_opcs4_to_audit(opcs49);
        });

    }
    
}

function add_opcs4_to_audit(opcs4) {
    // You can have multiple of the same procedures and laterality codes...
    opcs49_audit_results.push(opcs4.toUpperCase());
    rebuild_audit_opcs40_results_view();
}

function add_icd10_to_audit(icd10) {
    if (icd10.endsWith("X")) {
        icd10 = icd10.slice(0, -1);  
    }
    icd10 = icd10.replace(".", "")
    if (icd10_audit_results.includes(icd10) == false) {
        icd10_audit_results.push(icd10.toUpperCase());
        rebuild_audit_icd10_results_view();
    }
}

function submit_icd10_via_form() {
    var icd10 = $("#icd10ControlInput").val();
    if (icd10.length >= 3) {
        add_icd10_to_audit(icd10);
        $("#icd10ControlInput").val('');

    }

    else {
        alert("Probably wrong ICD10")
    }
}

function submit_opcs4_via_form() {
    var opcs4 = $("#opcs4ControlInput").val();
    if (opcs4.length >= 3) {
        add_opcs4_to_audit(opcs4);
        $("#opcs4ControlInput").val('');
    }
}

$(document).ready(function () {
    var note = get_note()["content"];

    fill_autocoded_diagnosis(note);
    fill_autocoded_procedures(note);
    
    rebuild_audit_icd10_results_view();
    rebuild_audit_opcs40_results_view();

    $('#auditiedIcd10').sortable({
        onUpdate: function() {
			var order = this.toArray();;
            icd10_audit_results = this.toArray();
            rebuild_audit_icd10_results_view();
        }
    });


    $('#auditiedOpcs4').sortable({
        onUpdate: function() {
			var order = this.toArray();
            var new_order = []
            for (i in order) {
                var t_opcs4 = order[i];
                new_order.push(t_opcs4.split("-")[0]);
            }
            opcs49_audit_results = new_order;
            rebuild_audit_opcs40_results_view();
        }
    });




    $("#icd10submit").click(function() {
        submit_icd10_via_form();
    });

    $("#icd10ControlInput").on("keyup", function (event) {
        if (event.key === 'Enter') {
            submit_icd10_via_form()
        }
    });

    $("#opcs4submit").click(function() {
        submit_opcs4_via_form()
    });

    $("#opcs4ControlInput").on("keyup", function (event) {
        if (event.key === 'Enter') {
            submit_opcs4_via_form()
        }
    });

    $("#toggleSubmitModal").click(function() {
        $("#diagnosis").val(icd10_audit_results.join('/'));
        $("#procedures").val(opcs49_audit_results.join('/'));
        $("#auditorInput").val(`AUTOCODED*${$("#nadex").html()}`);
        $("#submitModal").modal("show");
    });

    
}); 