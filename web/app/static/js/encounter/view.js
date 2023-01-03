const zeroPad = (num, places) => String(num).padStart(places, '0')

$(document).ready(function () {
    $('[id^="navlink_"]').click(function() {
        
        var id = $(this).attr('id');

        var div = id.split("_")[1];
        
        var messages = document.querySelectorAll(".encounter-content");
        for (var i = 0; i < messages.length; i++) {
            $(`#${messages[i].id}`).fadeOut(0);
        }

        $(`#${div}`).fadeIn(500);
     });
});