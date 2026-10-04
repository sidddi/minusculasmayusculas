/**
 * Mayúsculas después de punto
 * Convierte la primera letra del texto a mayúscula y capitaliza
 * la primera letra tras cada punto, cierre de interrogación o exclamación
 * (o puntos suspensivos) seguido de espacio, y tras cada salto de línea.
 * Salta los signos de apertura (¿ ¡ « " “ ' ( [) para llegar a la letra.
 */
function capitalizarDespuesDePunto(text) {
  if (!text) return text;
  return text
    .toLowerCase()
    .replace(/(^[ \t]*|[.?!…]\s+|\n[ \t]*)([¿¡«"“'(\[]*)([^\s¿¡«"“'(\[])/g, function (match, sep, open, char) {
      return sep + open + char.toUpperCase();
    });
}

/**
 * todo minúsculas
 * Convierte todo el texto a letras minúsculas.
 */
function todoMinusculas(text) {
  return text.toLowerCase();
}

/**
 * TODO MAYÚSCULAS
 * Convierte todo el texto a letras mayúsculas.
 */
function todoMayusculas(text) {
  return text.toUpperCase();
}

/**
 * Capitalizar Cada Palabra
 * Pone en mayúscula la primera letra de cada palabra, también cuando
 * la palabra empieza tras un signo de apertura («hola» → «Hola»).
 */
function capitalizarCadaPalabra(text) {
  if (!text) return text;
  return text
    .toLowerCase()
    .replace(/(^|\s)([¿¡«"“'(\[]*)(\S)/g, function (match, space, open, char) {
      return space + open + char.toUpperCase();
    });
}
