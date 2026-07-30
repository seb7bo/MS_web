// JavaScript function to toggle the menu visibility
function toggleMenu() {
  var menu = document.getElementById("menu");
  var menuDescription = document.getElementById("menu-description");
  if (menu.style.display === "block") {
    menu.style.display = "none";
    menuDescription.style.display = "none"; // Hide the description when menu is closed
  } else {
    menu.style.display = "block";
    menuDescription.style.display = "block"; // Show the description when menu is opened
  }
}

// Start the typewriter animations when the page loads
window.onload = function() {
  // Initialize language from localStorage (default 'es')
  var savedLang = localStorage.getItem('site-lang') || 'es';
  currentLang = savedLang;
  applyLanguage(savedLang);
  var langToggle = document.getElementById('lang-toggle');
  if (langToggle) langToggle.innerText = (savedLang === 'en') ? 'ES' : 'EN';

  startTypewriter();
};

function resetTypewriter() {
  ['typewriter-text', 'typewriter-text2', 'typewriter-text3'].forEach(function(id) {
    var el = document.getElementById(id);
    if (el) {
      el.innerHTML = '';
    }
  });
  index1 = 0;
  index2 = 0;
  index3 = 0;
}

function startTypewriter() {
  resetTypewriter();
  if (document.getElementById("typewriter-text")) {
    typeWriter();
    setTimeout(typeWriter2, 700); // Start the second typewriter animation sooner
    setTimeout(typeWriter3, 1400); // Start the third typewriter animation sooner
  }
}

// JavaScript function for the typewriter animation
const text1 = {
  es: "Somos proveedores líderes en equipamiento industrial de alto rendimiento para los sectores eléctrico y petroquímico. Nuestra especialización abarca el diseño, suministro e implementación de motores eléctricos asincrónicos y sincrónicos, disponibles en tensiones media y baja, adaptados a las exigencias técnicas de proyectos complejos.",
  en: "We are leading suppliers of high-performance industrial equipment for the electrical and petrochemical sectors. Our expertise covers the design, supply, and implementation of asynchronous and synchronous electric motors, available in medium and low voltages, adapted to the technical demands of complex projects."
};
const text2 = {
  es: "Cada producto y solución que ofrecemos cumple rigurosamente con los más altos estándares internacionales de calidad, eficiencia energética y seguridad industrial, garantizando durabilidad y óptimo funcionamiento en entornos críticos.",
  en: "Every product and solution we offer rigorously meets the highest international standards for quality, energy efficiency, and industrial safety, ensuring durability and optimal performance in critical environments."
};
const text3 = {
  es: "Trabajamos con un enfoque integral, respaldado por certificaciones globales y un equipo técnico especializado, para brindar soporte desde la fase de planificación hasta la puesta en marcha. Confíe en nosotros para impulsar sus proyectos con tecnología confiable, innovación estratégica y compromiso con la excelencia.",
  en: "We work with an integrated approach, backed by global certifications and a specialized technical team, to provide support from planning through commissioning. Trust us to drive your projects with reliable technology, strategic innovation, and a commitment to excellence."
};
let currentLang = 'es';
let index1 = 0;
let index2 = 0;
let index3 = 0;

function typeWriter() {
  const currentText = text1[currentLang];
  if (index1 < currentText.length) {
    document.getElementById("typewriter-text").innerHTML += currentText.charAt(index1);
    index1++;
    setTimeout(typeWriter, 12); // Faster typing speed (milliseconds)
  }
}

function typeWriter2() {
  const currentText = text2[currentLang];
  if (index2 < currentText.length) {
    document.getElementById("typewriter-text2").innerHTML += currentText.charAt(index2);
    index2++;
    setTimeout(typeWriter2, 12); // Faster typing speed (milliseconds)
  }
}

function typeWriter3() {
  const currentText = text3[currentLang];
  if (index3 < currentText.length) {
    document.getElementById("typewriter-text3").innerHTML += currentText.charAt(index3);
    index3++;
    setTimeout(typeWriter3, 12); // Faster typing speed (milliseconds)
  }
}

function updateTypewriterText() {
  var el1 = document.getElementById("typewriter-text");
  var el2 = document.getElementById("typewriter-text2");
  var el3 = document.getElementById("typewriter-text3");
  if (el1 && el2 && el3) {
    el1.innerText = text1[currentLang];
    el2.innerText = text2[currentLang];
    el3.innerText = text3[currentLang];
    index1 = text1[currentLang].length;
    index2 = text2[currentLang].length;
    index3 = text3[currentLang].length;
  }
}

// Language toggle utilities
function applyLanguage(lang) {
  document.querySelectorAll('[data-en]').forEach(function(el) {
    if (!el.getAttribute('data-es')) {
      el.setAttribute('data-es', el.innerText);
    }
    var text = (lang === 'en') ? el.getAttribute('data-en') : el.getAttribute('data-es');
    el.innerText = text;
    if (el.hasAttribute('data-text')) {
      el.setAttribute('data-text', text);
    }
  });
  document.documentElement.setAttribute('lang', lang);
  localStorage.setItem('site-lang', lang);
}

function toggleLanguage() {
  var current = document.documentElement.getAttribute('lang') || 'es';
  var next = (current === 'es') ? 'en' : 'es';
  currentLang = next;
  applyLanguage(next);
  startTypewriter();
  var langToggle = document.getElementById('lang-toggle');
  if (langToggle) langToggle.innerText = (next === 'en') ? 'ES' : 'EN';
}