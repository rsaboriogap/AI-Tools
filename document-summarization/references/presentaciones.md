# Presentaciones PowerPoint

## Descripción

El skill genera **presentaciones PowerPoint profesionales y educativas** a partir de los documentos analizados. Las presentaciones incluyen:

- Diapositivas estructuradas por capítulo
- Visualización del mapa conceptual
- Preguntas clave de estudio
- Notas del orador con contexto y ejemplos
- Tema visual configurable

## Activación

Las presentaciones se generan cuando:

```json
{
  "presentation": {
    "enabled": true
  }
}
```

## Opciones de configuración

### `presentation.enabled`
- **Tipo:** booleano
- **Valor por defecto:** `false`
- **Descripción:** Activa la generación de presentaciones PowerPoint.

### `presentation.style`
- **Tipo:** cadena
- **Valores permitidos:** `educational`, `corporate`, `minimalist`
- **Valor por defecto:** `educational`
- **Descripción:**
  - `educational`: Estilo amigable para estudiantes, con colores vibrantes y énfasis en conceptos clave.
  - `corporate`: Diseño profesional para contextos académicos o empresariales.
  - `minimalist`: Diseño limpio con tipografía clara y espacios en blanco.

### `presentation.theme`
- **Tipo:** cadena
- **Valores permitidos:** `modern`, `classic`, `colorful`, `dark`
- **Valor por defecto:** `modern`
- **Descripción:**
  - `modern`: Colores contemporáneos, líneas limpias, tipografía sans-serif.
  - `classic`: Colores tradicionales, fuentes serif, aspecto académico.
  - `colorful`: Paleta de colores vibrante, ideal para captar atención.
  - `dark`: Fondo oscuro, texto claro, cómodo para proyecciones prolongadas.

### `presentation.slides_per_chapter`
- **Tipo:** entero (1-5)
- **Valor por defecto:** `3`
- **Descripción:** Número de diapositivas dedicadas a cada capítulo:
  - `1`: Resumen compacto (título + idea principal).
  - `2`: Título + conceptos clave.
  - `3`: Título + conceptos + análisis profundo.
  - `4`: Título + conceptos + análisis + ejemplos prácticos.
  - `5`: Título + conceptos + análisis + ejemplos + reflexión.

### `presentation.include_title_slide`
- **Tipo:** booleano
- **Valor por defecto:** `true`
- **Descripción:** Incluye portada inicial con título del documento, autor, fecha y tema.

### `presentation.include_summary_slide`
- **Tipo:** booleano
- **Valor por defecto:** `true`
- **Descripción:** Incluye diapositiva de resumen general al final.

### `presentation.include_conceptual_map`
- **Tipo:** booleano
- **Valor por defecto:** `true`
- **Descripción:** Incluye el mapa conceptual (en formato visual) como diapositiva dedicada.

### `presentation.include_key_questions`
- **Tipo:** booleano
- **Valor por defecto:** `true`
- **Descripción:** Incluye diapositivas con preguntas clave y respuestas resumidas.

### `presentation.include_speaker_notes`
- **Tipo:** booleano
- **Valor por defecto:** `true`
- **Descripción:** Agrega notas del orador a cada diapositiva con:
  - Contexto ampliado
  - Ejemplos prácticos
  - Transiciones sugeridas
  - Aclaraciones adicionales

## Estructura de una presentación

### Portada (si `include_title_slide = true`)
- Título del documento
- Autor (si está disponible)
- Fecha de análisis
- Tema general
- Institución/Contexto

### Índice de contenidos
- Lista de capítulos principales
- Vista general de la estructura

### Capítulos (repetido según `slides_per_chapter`)

**Diapositiva 1: Introducción al capítulo**
- Título del capítulo
- Pregunta guía o problema principal

**Diapositiva 2: Conceptos clave**
- Terminología principal
- Definiciones operacionales
- Relaciones conceptuales

**Diapositiva 3: Análisis profundo**
- Argumento principal del capítulo
- Evidencia o ejemplos del documento
- Implicaciones prácticas

**Diapositiva 4 (opcional): Ejemplos prácticos**
- Casos de estudio
- Aplicaciones reales
- Ejercicios sugeridos

**Diapositiva 5 (opcional): Reflexión y preguntas**
- Puntos de reflexión
- Preguntas de pensamiento crítico
- Conexiones con otros capítulos

### Mapa Conceptual (si `include_conceptual_map = true`)
- Visualización en formato diagrama
- Relaciones entre conceptos principales
- Jerarquía de ideas

### Preguntas Clave (si `include_key_questions = true`)
- Preguntas seleccionadas del banco de preguntas
- Respuestas concisas
- Explicaciones breves

### Resumen General (si `include_summary_slide = true`)
- Puntos clave de todos los capítulos
- Conclusiones principales
- Llamada a la acción o reflexión final

## Modo individual vs. consolidado

### Presentación Individual
- Una presentación PPT por documento
- Estructura completa: portada + índice + capítulos + mapa + preguntas + resumen.
- Nombre: `{nombre_documento}_presentacion.pptx`

### Presentación Consolidada
- Una presentación única que integra todos los documentos
- Secciones por documento dentro de la misma presentación
- Análisis comparativo en diapositivas de integración
- Nombre: `presentacion_consolidada.pptx`

## Notas del orador

Cada diapositiva incluye notas que contienen:

```
# Notas del Orador: [Título de la Diapositiva]

**Contexto:**
[Información ampliada que no aparece en la diapositiva]

**Ejemplos prácticos:**
[Casos concretos o aplicaciones]

**Transición sugerida:**
[Cómo conectar con la siguiente diapositiva]

**Aclaraciones:**
[Puntos delicados, limitaciones, o excepciones]

**Referencia:**
[Página o sección del documento original]
```

## Ejemplo de configuración personalizada

```json
{
  "presentation": {
    "enabled": true,
    "style": "educational",
    "theme": "colorful",
    "slides_per_chapter": 4,
    "include_title_slide": true,
    "include_summary_slide": true,
    "include_conceptual_map": true,
    "include_key_questions": true,
    "include_speaker_notes": true
  }
}
```

## Limitaciones conocidas

1. **Imágenes del documento original:** Las presentaciones generadas no incluyen automáticamente imágenes del documento fuente; se recomienda agregarlas manualmente post-generación si es necesario.
2. **Animaciones:** Las presentaciones utilizan transiciones simples y consistentes; no incluyen animaciones complejas.
3. **Formato de texto:** Se preserva la estructura lógica pero el formato visual se normaliza según el tema elegido.
4. **Referencias cruzadas:** En modo consolidado, las referencias entre documentos se incluyen como notas de texto.

## Integración con otros componentes

- **Guías de estudio:** El contenido de las diapositivas se alinea con las guías de estudio generadas.
- **Mapas conceptuales:** Se visualizan en una o más diapositivas dedicadas.
- **Banco de preguntas:** Las preguntas clave se seleccionan automáticamente para incluir.
- **Podcast:** Las notas del orador pueden usarse como base para la narración del podcast.

## Recomendaciones de uso

- Usa `slides_per_chapter: 3-4` para equilibrar profundidad y claridad.
- Activa `include_speaker_notes` si vas a presentar en vivo.
- Usa tema `dark` si vas a proyectar en aulas oscuras.
- Combina con `mode: consolidated` para análisis comparativo de varios documentos.

---

**Ver también:** `referencias/configuracion.md`, `referencias/modo_individual.md`, `referencias/modo_consolidado.md`
