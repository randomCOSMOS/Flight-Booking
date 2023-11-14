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