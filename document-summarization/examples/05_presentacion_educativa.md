# Ejemplo 5: Presentación PowerPoint Educativa

## Caso de uso

El usuario adjunta un documento sobre "Psicología Educacional" y solicita:
- Material de estudio completo en **modo individual**
- Incluir **presentación PowerPoint educativa**
- Estilo visual moderno con **3 diapositivas por capítulo**
- Incluir **notas del orador** para presentación en vivo

## Configuración JSON

```json
{
  "processing": {
    "mode": "individual",
    "analysis_depth": "detailed"
  },
  "output": {
    "format": "md",
    "language": "es",
    "generate_zip": true
  },
  "presentation": {
    "enabled": true,
    "style": "educational",
    "theme": "modern",
    "slides_per_chapter": 3,
    "include_title_slide": true,
    "include_summary_slide": true,
    "include_conceptual_map": true,
    "include_key_questions": true,
    "include_speaker_notes": true
  },
  "podcast": {
    "enabled": true,
    "target_duration_minutes": 12
  },
  "questions": {
    "enabled": true,
    "count": 15
  }
}
```

## Entrada del usuario

```
Analiza este documento sobre Psicología Educacional. Quiero:
- Material de estudio con modo individual
- Presentación PowerPoint moderna con 3 diapositivas por capítulo
- Notas del orador para presentar en clase
- Podcast educativo de 12 minutos
- 15 preguntas de estudio

{
  "presentation": {
    "enabled": true,
    "style": "educational",
    "theme": "modern",
    "slides_per_chapter": 3,
    "include_speaker_notes": true
  }
}
```

## Salida esperada

```
material_estudio.zip
│
└── individual/
    └── Psicologia_Educacional/
        ├── 01_Guia_Estudio.md
        ├── 02_Mapa_Conceptual.md
        ├── 03_Podcast_Script.md
        ├── 04_Banco_Preguntas.md
        └── 05_Psicologia_Educacional_presentacion.pptx
            ├── Portada
            ├── Índice
            ├── Capítulo 1: Fundamentos Teóricos (3 diapositivas)
            ├── Capítulo 2: Desarrollo Cognitivo (3 diapositivas)
            ├── Capítulo 3: Estrategias de Aprendizaje (3 diapositivas)
            ├── Capítulo 4: Evaluación Educativa (3 diapositivas)
            ├── Mapa Conceptual
            ├── Preguntas Clave
            └── Resumen General
```

## Estructura de la presentación PowerPoint

### Diapositiva 1: Portada
- **Título:** Psicología Educacional
- **Subtítulo:** Principios y aplicaciones en el aula
- **Autor:** [Si está disponible]
- **Fecha:** 2026-10-06
- **Notas del orador:** Contexto general del documento y objetivo de la presentación.

### Diapositiva 2: Índice
- Capítulo 1: Fundamentos Teóricos
- Capítulo 2: Desarrollo Cognitivo
- Capítulo 3: Estrategias de Aprendizaje
- Capítulo 4: Evaluación Educativa

### Diapositivas 3-5: Capítulo 1 - Fundamentos Teóricos

**Diapositiva 3: Introducción**
- Título: "¿Qué es la Psicología Educacional?"
- Pregunta guía: ¿Cómo la psicología mejora la enseñanza?
- Notas: Definición operativa, contexto histórico.

**Diapositiva 4: Conceptos Clave**
- Aprendizaje significativo
- Constructivismo
- Metacognición
- Motivación intrínseca
- Notas: Explicaciones ampliadas con ejemplos de aula.

**Diapositiva 5: Aplicaciones Prácticas**
- Diseño de lecciones basado en teoría
- Adaptación a estilos de aprendizaje
- Mejora del clima educativo
- Notas: Casos de estudio e implementación real.

### Diapositiva N: Mapa Conceptual
- Visualización jerárquica de conceptos principales
- Relaciones etiquetadas entre ideas
- Notas: Explicación de la estructura conceptual.

### Diapositiva N+1: Preguntas Clave
- Pregunta 1 + respuesta breve
- Pregunta 2 + respuesta breve
- Pregunta 3 + respuesta breve
- Notas: Desarrollo de respuestas completas.

### Diapositiva Final: Resumen General
- Puntos clave de cada capítulo
- Conexiones principales
- Reflexión final
- Notas: Sugerencias de actividades de consolidación.

## Configuración alternativa: Tema "colorful"

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

**Resultado:** Presentación con paleta vibrante, ideal para captar atención de estudiantes.

## Configuración alternativa: Tema "dark" para proyección

```json
{
  "presentation": {
    "enabled": true,
    "style": "corporate",
    "theme": "dark",
    "slides_per_chapter": 3,
    "include_speaker_notes": true
  }
}
```

**Resultado:** Presentación profesional con fondo oscuro, cómoda para proyecciones prolongadas.

## Notas del orador - Ejemplo completo

### Diapositiva: "Aprendizaje Significativo"

```
# Notas del Orador: Aprendizaje Significativo

**Contexto:**
El aprendizaje significativo ocurre cuando el estudiante vincula nueva información
con sus conocimientos previos. Este concepto, desarrollado por David Ausubel,
es fundamental en la psicología educacional moderna.

**Ejemplos prácticos:**
- Al enseñar fotosíntesis, comenzar con preguntas sobre plantas que los estudiantes
  conocen (flores del jardín, árboles del parque).
- Conectar fracciones con situaciones reales (dividir una pizza, compartir dinero).
- Usar analogías: "Una célula es como una fábrica" (mitocondrias = plantas de energía).

**Transición sugerida:**
"Ahora que entendemos cómo ocurre el aprendizaje significativo,
veamos cómo el constructivismo complementa este concepto..."

**Aclaraciones:**
- No confundir con "aprendizaje memorístico" (repetición sin sentido).
- Aunque más lento, el aprendizaje significativo es más duradero.
- Requiere actividad cognitiva del estudiante, no transmisión pasiva.

**Referencia:**
Página 45-47, "Teorías Cognitivistas del Aprendizaje"
```

## Recomendaciones de presentación

1. **Duración:** Aproximadamente 45-50 minutos (incluyendo pausas).
2. **Público:** Estudiantes de postgrado, educadores, diseñadores instruccionales.
3. **Interactividad:** Usar las preguntas clave como puntos de discusión grupal.
4. **Actividad práctica:** Pausar después del Capítulo 2 para ejercicio de análisis.
5. **Cierre:** Invitar reflexión sobre aplicación personal.

## Checklist de revisión post-generación

- [ ] Todas las diapositivas están presentes
- [ ] Las imágenes del mapa conceptual son legibles
- [ ] Las notas del orador aparecen correctamente
- [ ] Los colores se ven bien en el tema elegido
- [ ] Las transiciones funcionan correctamente
- [ ] El archivo PowerPoint se abre sin errores
- [ ] Los datos coinciden con la guía de estudio

---

**Ver también:** `references/presentaciones.md`, `references/modo_individual.md`
