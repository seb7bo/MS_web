# MARASE Supply — nueva página de inicio

## Contenido del paquete

- `index.html` — la nueva home, en un solo archivo (HTML + CSS + JS, sin dependencias).

## Cómo instalarla

1. Haz respaldo de tu `index.html` actual (renómbralo a `index-anterior.html`).
2. Sube `index.html` a la raíz de tu sitio, al mismo nivel que `aboutus.html`,
   `industrialproducts.html`, `services.html`, `contacto.html` y `privacy.html`.
3. Asegúrate de que la carpeta `image/` siga en la raíz. La página usa estas imágenes
   que ya tienes publicadas:

   - `image/motor.jpg`
   - `image/bomba.png`
   - `image/Soplador.jpg`
   - `image/ttrmegger.jpg`
   - `image/pqm.jpg`
   - `image/Cable.jpg`
   - `image/logogold.svg` (tu logo, usado en el header, el footer, el favicon y
     como marca de agua al 5% de opacidad detrás del hero)

   Si alguna falta, la tarjeta muestra automáticamente un respaldo gráfico (gradiente
   con ícono) en lugar de una imagen rota.
4. Listo. No hay build, ni npm, ni framework.

## Qué puedes editar sin tocar código

- **Colores**: al inicio del `<style>`, en el bloque `:root`.
  `--gold` (dorado de marca), `--ink` (fondo oscuro), `--paper` (fondo claro).
- **Cifras de la banda oscura**: busca `<section class="band stats">`.
  Hoy dicen 7 líneas, 4 servicios, 6 días y cobertura nacional.
  Cámbialas por años de operación, clientes atendidos o proyectos entregados
  cuando tengas el dato real.
- **Datos de contacto**: busca `id="contacto"` y el `<footer>`.
  Teléfono, correo y dirección aparecen en ambos lugares.

## Sobre el logo

Se usa `image/logogold.svg` en cuatro lugares, de forma discreta:

1. Header, a 38 px de alto.
2. Footer, a 46 px.
3. Favicon de la pestaña.
4. Marca de agua detrás del hero, al 5% de opacidad.

Si el archivo no se encuentra, la página cambia automáticamente a un logotipo
tipográfico (MARASE / SUPPLY) para que nunca se vea una imagen rota.
Para ajustar el tamaño busca `.brand .logo` en el `<style>`; para la marca de
agua, `.hero .watermark` (la opacidad es la propiedad `opacity:.05`).

## Sobre el botón ES / EN

Funciona en vivo: cada texto traducible lleva un atributo `data-en` con su versión
en inglés. Para cambiar una traducción, edita el `data-en` del elemento.
Para agregar un texto nuevo traducible, basta con darle su propio `data-en`.

## Tipografías

Se cargan desde Google Fonts (Fraunces para titulares, Archivo para texto).
Si prefieres alojarlas en tu propio servidor para no depender de un tercero,
descarga ambas familias y reemplaza el `<link>` del `<head>` por un `@font-face`.

## Accesibilidad y responsive

- Menú hamburguesa en móvil, navegación por teclado con foco visible.
- Respeta `prefers-reduced-motion`: si el usuario desactiva animaciones, la página
  se muestra estática.
- Probado desde 360 px hasta pantallas anchas.

## Siguiente paso sugerido

Aplicar el mismo sistema visual a las páginas internas, empezando por `services.html`,
que hoy muestra un GIF de "en construcción".
