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
  autoplayTimeout: 6000,
  autoplayHoverPause: false,
  stagePadding: 0,
  smartSpeed: 2000,
  responsiveClass: true,
  responsive: {
    0: {
      items: 4
    },
    600: {
      items: 4
    },
    1000: {
      items: 5
    }
  }
})

$('#carousel2').owlCarousel({
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

$('#carousel3').owlCarousel({
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

$('#carousel_detalhes').owlCarousel({
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
    600: {
      items: 1
    },
    1000: {
      items: 1
    }
  }
})