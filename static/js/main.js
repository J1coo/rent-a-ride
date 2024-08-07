/**
* Template Name: Append
* Updated: Aug 30 2023 with Bootstrap v5.3.1
* Template URL: https://bootstrapmade.com/append-bootstrap-website-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
const confirmLogout=()=>{
  let status = window.confirm('Do you want to logout ?')
  if(status){
    location.assign('/logout/')
  }

}
let waitDialog=document.querySelector('[data-waitDialog]')
document.addEventListener('DOMContentLoaded', () => {
  "use strict";

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  const selectBody = document.querySelector('body');
  const selectHeader = document.querySelector('#header');

  function toggleScrolled() {
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Scroll up sticky header to headers with .scroll-up-sticky class
   */
  let lastScrollTop = 0;
  window.addEventListener('scroll', function () {
    if (!selectHeader.classList.contains('scroll-up-sticky')) return;

    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop && scrollTop > selectHeader.offsetHeight) {
      selectHeader.style.setProperty('position', 'sticky', 'important');
      selectHeader.style.top = `-${header.offsetHeight + 50}px`;
    } else if (scrollTop > selectHeader.offsetHeight) {
      selectHeader.style.setProperty('position', 'sticky', 'important');
      selectHeader.style.top = "0";
    } else {
      selectHeader.style.removeProperty('top');
      selectHeader.style.removeProperty('position');
    }
    lastScrollTop = scrollTop;
  });

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  mobileNavToggleBtn.addEventListener('click', mobileNavToogle);

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .has-dropdown i').forEach(navmenu => {
    navmenu.addEventListener('click', function (e) {
      if (document.querySelector('.mobile-nav-active')) {
        e.preventDefault();
        this.parentNode.classList.toggle('active');
        this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
        e.stopImmediatePropagation();
      }
    });
  });

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener('load', function (e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init isotope layout and filters
   */
  function initIsotopeLayout() {
    document.querySelectorAll('.isotope-layout').forEach(function (isotopeItem) {
      let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
      let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
      let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

      let initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
        itemSelector: '.isotope-item',
        layoutMode: layout,
        filter: filter,
        sortBy: sort
      });

      isotopeItem.querySelectorAll('.isotope-filters li').forEach(function (filters) {
        filters.addEventListener('click', function () {
          isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
          this.classList.add('filter-active');
          initIsotope.arrange({
            filter: this.getAttribute('data-filter')
          });
          if (typeof aosInit === 'function') {
            aosInit();
          }
        }, false);
      });

    });
  }
  window.addEventListener('load', initIsotopeLayout);

  /**
   * Frequently Asked Questions Toggle
   */
  document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
    faqItem.addEventListener('click', () => {
      faqItem.parentNode.classList.toggle('faq-active');
    });
  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll('.swiper').forEach(function (swiper) {
      let config = JSON.parse(swiper.querySelector('.swiper-config').innerHTML.trim());
      new Swiper(swiper, config);
    });
  }
  window.addEventListener('load', initSwiper);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

});


const searchPlace = async () => {
  let userLocation = document.getElementById('userLocation').value.trim()
  let addressDropDownModal = document.getElementById('addressDropDownModal')

  let locationSeggestionDiv = document.getElementById('locationSeggestionDiv')
  locationSeggestionDiv.innerHTML = ''
  let firstOptoin = document.createElement('option')
  firstOptoin.value=''
  firstOptoin.innerHTML='Select location'
  locationSeggestionDiv.appendChild(firstOptoin)

  fetch(`https://api.geoapify.com/v1/geocode/autocomplete?text=${userLocation}&format=json&apiKey=94ec647943634731b43f21d4f34265f9`)
    .then(response => response.json())
    .then(result => {
      let predictedLocations = Array.from(result['results'])
      if (predictedLocations.length != 0) {
        predictedLocations.forEach((eachLocation) => {
          let eachLocationInput = document.createElement('option')

          let locationValue={}
          locationValue['formattedName']=eachLocation['formatted']
          locationValue['lat']= eachLocation['lat'].toString()
          locationValue['lon']=eachLocation['lon'].toString()
          locationValue['place_id']=eachLocation['place_id']
          locationValue['state']=eachLocation['state']
          locationValue['state_code']=eachLocation['state_code']
          locationValue['country']=eachLocation['country']
          locationValue['country_code']=eachLocation['country_code']

          eachLocationInput.value = `${JSON.stringify(locationValue)}`
          eachLocationInput.innerHTML = `${eachLocation['formatted']}`
          eachLocationInput.classList.add('suggestedAdress')
          locationSeggestionDiv.appendChild(eachLocationInput)
        })
      }
      else{
      }
    })
    .catch(error => console.log('error', error));

}

const searchDestinationPlace = async () => {
  let userLocation = document.getElementById('destinationLocationId').value.trim()
  let addressDropDownModal = document.getElementById('destinationAddressDropDown')

  let locationSeggestionDiv = document.getElementById('destinationAddressSelectTag')
  locationSeggestionDiv.innerHTML = ''
  let firstOptoin = document.createElement('option')
  firstOptoin.value=''
  firstOptoin.innerHTML='Select location'
  locationSeggestionDiv.appendChild(firstOptoin)

  fetch(`https://api.geoapify.com/v1/geocode/autocomplete?text=${userLocation}&format=json&apiKey=94ec647943634731b43f21d4f34265f9`)
    .then(response => response.json())
    .then(result => {
      let predictedLocations = Array.from(result['results'])
      if (predictedLocations.length != 0) {
        predictedLocations.forEach((eachLocation) => {
          let eachLocationInput = document.createElement('option')

          let locationValue={}
          locationValue['formattedName']=eachLocation['formatted']
          locationValue['lat']=eachLocation['lat'].toString()
          locationValue['lon']=eachLocation['lon'].toString()
          locationValue['place_id']=eachLocation['place_id']
          locationValue['state']=eachLocation['state']
          locationValue['state_code']=eachLocation['state_code']
          locationValue['country']=eachLocation['country']
          locationValue['country_code']=eachLocation['country_code']

          eachLocationInput.value = `${JSON.stringify(locationValue)}`
          eachLocationInput.innerHTML = `${eachLocation['formatted']}`
          eachLocationInput.classList.add('suggestedAdress')
          locationSeggestionDiv.appendChild(eachLocationInput)
        })
      }
      else{
      }
    })
    .catch(error => console.log('error', error));

}



const putAddressToInput=(e)=>{
  let currentValue=e.currentTarget.value
  console.log(currentValue)
}