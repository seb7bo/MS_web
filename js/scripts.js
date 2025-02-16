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
const text1 = "Nos especializamos en el suministro de materiales y equipos de alta calidad para proyectos industriales eléctricos y petroquímicos. Ofrecemos una amplia gama de productos, desde cables eléctricos y transformadores hasta válvulas y tuberías, todo cumpliendo con los más altos estándares de calidad y seguridad.";
const text2 = "En nuestra empresa, también ofrecemos una amplia gama de insumos médicos y de salud, desde equipos de diagnóstico hasta suministros de primeros auxilios. Trabajamos con los principales fabricantes del mercado y nos aseguramos de que nuestros productos cumplan con altos estándares de calidad y seguridad.";
const text3 = "Nuestro equipo de expertos altamente capacitados cuenta con amplia experiencia en el ámbito contable, fiscal y laboral, y se asegura de mantenerse actualizado sobre las leyes y regulaciones aplicables en cada área. Ofrecemos una amplia gama de servicios contactanos para mas información.";

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