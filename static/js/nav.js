$('.hamburger').click(() => {
    $('.hamburger').toggleClass('is-active');
    $('nav div').toggleClass('show');
});

if ((window.location.href).indexOf('localhost') !== 7) {
    let loc = window.location.href + '';
    if (loc.indexOf('http://') === 0) {
        window.location.href = loc.replace('http://', 'https://');
    }
}

// hides navbar on scroll
var prevScrollpos = 0;
$("nav").css("top", "0");

$(window).scroll(() => {
  var currentScrollPos = window.scrollY;

  if (prevScrollpos > currentScrollPos) {
    $("nav").css("top", "0");
  } else {
    $("nav").css("top", "-100px");
  }
  
  prevScrollpos = currentScrollPos;
});