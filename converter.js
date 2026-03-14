/**
 * Mayúsculas después de punto
 * Convierte la primera letra del texto a mayúscula y capitaliza
 * la primera letra tras cada punto seguido de espacio o tras salto de línea.
 */
function capitalizarDespuesDePunto(text) {
  if (!text) return text;
  return text
    .toLowerCase()
    .replace(/(^[ \t]*|\.\s+|\n[ \t]*)([^\s])/g, function (match, sep, char) {
      return sep + char.toUpperCase();
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
 * Pone en mayúscula la primera letra de cada palabra.
 */
function capitalizarCadaPalabra(text) {
  if (!text) return text;
  return text
    .toLowerCase()
    .replace(/(^|\s)(\S)/g, function (match, space, char) {
      return space + char.toUpperCase();
    });
}
