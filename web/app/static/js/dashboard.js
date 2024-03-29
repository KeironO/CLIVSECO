


function get_data() {

    var api_url = encodeURI(window.location.origin + '/api/notes/chartjs' );

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

function render_graph(data, divid, type) {

    const ctx = document.getElementById(divid).getContext('2d');
    const myChart = new Chart(ctx, {
        type: type,
        data: data
    });

}


$(document).ready(function () {
    var dashboard_data = get_data()["content"];

    $("#dal-count").html(dashboard_data['counts']['letters']);
    $("#auto-code-count").html(dashboard_data['counts']['autocodes']);

    var pdoc = dashboard_data['counts']['autocodes']/ dashboard_data['counts']['letters'];
    var pdoc = parseFloat(pdoc.toFixed(2))

    $("#avg-number").html(pdoc);

    render_graph(dashboard_data['notes']['admitting_spec'], 'admission-spec-chart', 'pie')
    render_graph(dashboard_data['notes']['discharge_spec'], 'discharge-spec-chart', 'pie')
    render_graph(dashboard_data['autocodes']['source_text'], 'auto-code-section-chart', 'bar')

});
        
