String.prototype.insert = function(index, string) {
    if (index > 0) {
      return this.substring(0, index) + string + this.substr(index);
    }
  
    return string + this;
};

function toggle_open_dyslexia() {
  var setting = localStorage.dyslexia;
  if (setting == 'on') {
    $("body").attr('style', 'font-family:opendyslexic !important; font-size:1.5rem;');
  }
  else {
    $("body").attr('style', 'font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","Liberation Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";');
  }
}

$(document).ready(function () {

  if (localStorage.dyslexia) {
    
  } else {
    localStorage.dyslexia = 'off';
  }

  toggle_open_dyslexia();

  $("#toggledyslexic").click(function() {
      var setting = localStorage.dyslexia;
      if (setting == 'on') {
        localStorage.dyslexia = 'off'
    } else {
      localStorage.dyslexia = 'on'
  }
  toggle_open_dyslexia();
  });


});