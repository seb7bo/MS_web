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
  typeWriter();
  setTimeout(typeWriter2, 2000); // Start the second typewriter animation after 2 seconds
  setTimeout(typeWriter3, 4000); // Start the third typewriter animation after 4 seconds
};

// JavaScript function for the typewriter animation
const text1 = "Somos proveedores líderes en equipamiento industrial de alto rendimiento para los sectores eléctrico y petroquímico. Nuestra especialización abarca el diseño, suministro e implementación de motores eléctricos asincrónicos y sincrónicos, disponibles en tensiones media y baja, adaptados a las exigencias técnicas de proyectos complejos.";
const text2 = "Cada producto y solución que ofrecemos cumple rigurosamente con los más altos estándares internacionales de calidad, eficiencia energética y seguridad industrial, garantizando durabilidad y óptimo funcionamiento en entornos críticos. ";
const text3 = "Trabajamos con un enfoque integral, respaldado por certificaciones globales y un equipo técnico especializado, para brindar soporte desde la fase de planificación hasta la puesta en marcha. Confíe en nosotros para impulsar sus proyectos con tecnología confiable, innovación estratégica y compromiso con la excelencia.";
let index1 = 0;
let index2 = 0;
let index3 = 0;

function typeWriter() {
  if (index1 < text1.length) {
    document.getElementById("typewriter-text").innerHTML += text1.charAt(index1);
    index1++;
    setTimeout(typeWriter, 50); // Adjust typing speed (milliseconds)
  }
}

function typeWriter2() {
  if (index2 < text2.length) {
    document.getElementById("typewriter-text2").innerHTML += text2.charAt(index2);
    index2++;
    setTimeout(typeWriter2, 50); // Adjust typing speed (milliseconds)
  }
}

function typeWriter3() {
  if (index3 < text3.length) {
    document.getElementById("typewriter-text3").innerHTML += text3.charAt(index3);
    index3++;
    setTimeout(typeWriter3, 50); // Adjust typing speed (milliseconds)
  }
}