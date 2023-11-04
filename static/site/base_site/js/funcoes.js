$(document).ready(function () {
  setInterval(function () {
    var e = "wa__btn_popup_txt";
    var o = document.getElementsByClassName(e);
    o[0].style.display = 'none';
  }, 10000);

  setInterval(function () {
    var e = "wa__btn_popup_txt";
    var o = document.getElementsByClassName(e);
    o[0].style.display = 'block';
  }, 30000);
});

$('#carousel1').owlCarousel({
  loop: true,
  margin: 10,
  nav: false,
  dots: false,
  autoplay: true,
  autoplayTimeout: 9000,
  autoplayHoverPause: false,
  stagePadding: 0,
  smartSpeed: 4000,
  responsiveClass: true,
  responsive: {
    0: {
      items: 2
    },
    600: {
      items: 3
    },
    1000: {
      items: 4
    }
  }
})

$('#carousel2').owlCarousel({
  loop: true,
  margin: 10,
  nav: false,
  dots: true,
  autoplay: true,
  autoplayTimeout: 9000,
  autoplayHoverPause: false,
  stagePadding: 0,
  smartSpeed: 6000,
  responsiveClass: true,
  responsive: {
    0: {
      items: 1
    },
    368: {
      items: 1.3
    },
    600: {
      items: 2
    },
    800: {
      items: 2.5
    },
    1000: {
      items: 4
    }
  }
})

$('#carousel3').owlCarousel({
  loop: true,
  margin: 10,
  nav: false,
  dots: true,
  autoplay: true,
  autoplayTimeout: 9000,
  autoplayHoverPause: false,
  stagePadding: 0,
  smartSpeed: 6000,
  responsiveClass: true,
  responsive: {
    0: {
      items: 1
    },
    368: {
      items: 1.3
    },
    600: {
      items: 2
    },
    800: {
      items: 2.5
    },
    1000: {
      items: 4
    }
  }
})


$('#products_relacionados').owlCarousel({
  loop: true,
  margin: 10,
  nav: false,
  dots: true,
  autoplay: true,
  autoplayTimeout: 6000,
  autoplayHoverPause: false,
  stagePadding: 0,
  smartSpeed: 2000,
  responsiveClass: true,
  responsive: {
    0: {
      items: 1
    },
    368: {
      items: 1.3
    },
    600: {
      items: 2
    },
    800: {
      items: 2.5
    },
    1000: {
      items: 4
    }
  }
})

$(document).on('click', '.display-count button', function () {
  var btn = $(this),
      oldValue = btn.closest('.display-count').find('input').val().trim(),
      newVal = 0;
  if (btn.attr('data-dir') == 'up') {
      newVal = parseInt(oldValue) + 1;
  } else {
      if (oldValue > 1) {
          newVal = parseInt(oldValue) - 1;
      } else {
          newVal = 0;
      }
  }
  btn.closest('.display-count').find('input').val(newVal);
});