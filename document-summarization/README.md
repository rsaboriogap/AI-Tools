# 📚 document-study-material-generator

Skill de Claude que transforma uno o varios documentos académicos (PDF, DOCX, MD, TXT) en **materiales de estudio estructurados, precisos y listos para usar**.

---

## 🎯 ¿Qué hace este skill?

A partir de una o varias lecturas, el skill genera automáticamente:

| Producto | Descripción |
|---|---|
| 📖 **Guías de estudio** | Resumen general + análisis capítulo por capítulo + conceptos clave + referencias. |
| 🗺️ **Mapas conceptuales** | Diagramas Mermaid (o jerárquicos) con relaciones etiquetadas. |
| 🎙️ **Guiones de podcast educativo** | Diálogos naturales entre presentador y experto, con duración ajustable. |
| 📊 **Presentaciones PowerPoint** | Diapositivas por capítulo con mapa conceptual, preguntas clave y notas del orador. |
| ❓ **Preguntas de estudio** | Banco con respuestas, explicaciones y referencias; cinco tipos de pregunta. |
| 🔗 **Análisis consolidado** | Integración de varias lecturas: similitudes, diferencias y aportes específicos. |
| 📦 **Paquete ZIP** | Todos los archivos organizados por modalidad + `manifest.json` reproducible. |

### Modos de análisis

- **`individual`** → genera dos archivos por documento (guía + podcast).
- **`consolidated`** → genera dos archivos que integran todas las lecturas.
- **`both`** → ejecuta ambos y organiza los resultados en carpetas independientes.

### Profundidades de análisis

- **`basic`** → síntesis breve centrada en lo esencial.
- **`detailed`** → explicación completa de conceptos y argumentos principales.
- **`exhaustive`** → análisis profundo de todos los capítulos, relaciones y matices.

---

## 🚀 ¿Cuándo se activa?

El skill se dispara automáticamente cuando el usuario:

- Adjunta documentos y pide "material de estudio", "guía de estudio", "resumen académico".
- Solicita "mapa conceptual", "podcast educativo", "preguntas de estudio" o "presentación".
- Pide "PowerPoint", "diapositivas", "PPT" o "presentación educativa".
- Pide analizar, sintetizar, consolidar o transformar lecturas universitarias.
- Menciona análisis "individual", "consolidado" o "both".

### Ejemplos de invocación

```
"Analiza estas 3 lecturas y genera material de estudio completo."
"Hazme una guía de estudio y un podcast educativo de este PDF."
"Genera un resumen consolidado con mapa conceptual, 15 preguntas y una presentación."
"Convierte estas lecturas en material de estudio con modo both y formato docx."
"Crea una presentación PowerPoint educativa con 3 diapositivas por capítulo."
"Genera material de estudio individual con presentación y notas del orador."
```

---

## ⚙️ Configuración: JSON completo con todas las opciones

El skill acepta un objeto JSON de configuración. **Todas las propiedades son opcionales**; si se omite alguna, se usa el valor por defecto. Las propiedades explícitas del usuario siempre tienen prioridad.

### Ejemplo completo (con valores por defecto)

```json
{
  "input": {
    "documents": "attached",
    "supported_formats": ["pdf", "docx", "md", "txt"]
  },

  "processing": {
    "mode": "individual",
    "analysis_depth": "detailed",
    "preserve_original_structure": true,
    "include_page_references": true,
    "cross_document_analysis": true,
    "include_practical_examples": true,
    "include_conclusions": true
  },

  "output": {
    "format": "md",
    "language": "es",
    "generate_zip": true,
    "zip_name": "material_estudio.zip",
    "include_manifest": true
  },

  "summary": {
    "style": "academic_natural",
    "detail_level": "comprehensive",
    "include_context": true,
    "include_key_concepts": true,
    "include_conclusions": true
  },

  "chapter_analysis": {
    "enabled": true,
    "include_main_topic": true,
    "include_key_concepts": true,
    "include_main_ideas": true,
    "include_relevant_arguments": true,
    "include_examples": true,
    "include_chapter_conclusions": true,
    "key_concepts_per_chapter": 5
  },

  "conceptual_map": {
    "enabled": true,
    "format": "mermaid",
    "max_depth": 4,
    "include_relationship_labels": true,
    "include_explanation": true
  },

  "podcast": {
    "enabled": true,
    "style": "educational",
    "tone": "natural_conversational",
    "target_duration_minutes": 12,
    "speakers": 2,
    "include_introduction": true,
    "include_examples": true,
    "include_reflection": true,
    "include_recap": true,
    "include_closing": true
  },

  "presentation": {
    "enabled": false,
    "style": "educational",
    "theme": "modern",
    "slides_per_chapter": 3,
    "include_title_slide": true,
    "include_summary_slide": true,
    "include_conceptual_map": true,
    "include_key_questions": true,
    "include_speaker_notes": true
  },

  "questions": {
    "enabled": true,
    "count": 10,
    "difficulty": "mixed",
    "include_answers": true,
    "include_explanations": true,
    "include_references": true,
    "question_types": [
      "conceptual",
      "comprehension",
      "analytical",
      "relational",
      "application"
    ]
  },

  "consolidated": {
    "include_common_topics": true,
    "include_document_contributions": true,
    "include_similarities": true,
    "include_differences": true,
    "include_integrated_conclusions": true
  },

  "quality_control": {
    "verify_document_coverage": true,
    "verify_factual_consistency": true,
    "verify_question_answers": true,
    "verify_conceptual_map": true,
    "verify_generated_files": true
  }
}
```

---

## 🔧 Opciones permitidas por parámetro

| Parámetro | Valores válidos | Descripción |
|---|---|---|
| `processing.mode` | `individual` \| `consolidated` \| `both` | Modalidad de análisis. |
| `processing.analysis_depth` | `basic` \| `detailed` \| `exhaustive` | Nivel de profundidad. |
| `output.format` | `md` \| `docx` | Formato de salida. |
| `output.language` | código ISO (ej. `es`, `en`) | Idioma de los materiales. |
| `summary.style` | `academic_natural` \| `academic_formal` | Tono del resumen. |
| `summary.detail_level` | `brief` \| `comprehensive` \| `exhaustive` | Extensión del resumen. |
| `conceptual_map.format` | `mermaid` \| `hierarchical` | Tipo de representación. |
| `podcast.style` | `educational` \| `interview` \| `narrative` | Estilo del guion. |
| `podcast.tone` | `natural_conversational` \| `formal_academic` | Tono del diálogo. |
| `podcast.speakers` | `1` \| `2` | Narrador único o presentador + experto. |
| `presentation.style` | `educational` \| `corporate` \| `minimalist` | Estilo de la presentación. |
| `presentation.theme` | `modern` \| `classic` \| `colorful` \| `dark` | Tema visual de las diapositivas. |
| `presentation.slides_per_chapter` | `1` - `5` | Diapositivas por capítulo. |
| `questions.difficulty` | `basic` \| `intermediate` \| `advanced` \| `mixed` | Dificultad de las preguntas. |
| `questions.question_types` | `conceptual`, `comprehension`, `analytical`, `relational`, `application` | Tipos a incluir. |

---

## 📦 Estructura de salida

```
material_estudio.zip
│
├── individual/
│   ├── documento_01/
│   │   ├── documento_01_guia_estudio.md
│   │   ├── documento_01_podcast.md
│   │   └── documento_01_presentacion.pptx
│   ├── documento_02/
│   │   ├── documento_02_guia_estudio.md
│   │   ├── documento_02_podcast.md
│   │   └── documento_02_presentacion.pptx
│   └── documento_N/
│       ├── documento_N_guia_estudio.md
│       ├── documento_N_podcast.md
│       └── documento_N_presentacion.pptx
│
├── consolidado/
│   ├── resumen_general_consolidado.md
│   ├── podcast_consolidado.md
│   └── presentacion_consolidada.pptx
│
└── manifest.json
```

Solo se crean las carpetas y archivos correspondientes a las **modalidades ejecutadas** y a las **funcionalidades habilitadas**.

---

## 🎙️ Duración del podcast

Ajusta la extensión del guion al valor de `podcast.target_duration_minutes`. Referencia aproximada (120–150 palabras habladas por minuto):

| Duración | Palabras aproximadas |
|---|---|
| 10 min | 1 200 – 1 500 |
| 12 min | 1 440 – 1 800 |
| 15 min | 1 800 – 2 250 |
| 20 min | 2 400 – 3 000 |
| 25 min | 3 000 – 3 750 |
| 30 min | 3 600 – 4 500 |

---

## 🛡️ Principios de calidad

1. **Fidelidad al contenido** → nunca se inventa información ni metadatos.
2. **Trazabilidad** → se distingue contenido del autor, síntesis, interpretación y ejemplo propio.
3. **Cobertura** → no se omiten capítulos sustantivos sin justificación.
4. **Verificación** → no se declara éxito sin comprobar los archivos generados.
5. **Transparencia** → toda limitación se registra en el manifiesto.

---

## 📂 Estructura del skill

```
document-study-material-generator/
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
├── SKILL.md
├── examples/
│   ├── README.md
│   ├── 01_individual_basico.md
│   ├── 02_consolidado_docx.md
│   ├── 03_both_exhaustivo.md
│   └── 04_podcast_extendido.md
├── references/
│   ├── configuracion.md
│   ├── modo_individual.md
│   ├── modo_consolidado.md
│   ├── formatos_salida.md
│   └── control_calidad.md
└── scripts/
    └── empaquetar_zip.py
```

---

## 🧪 Ejemplo rápido de uso

**Entrada del usuario:**

> "Analiza estas 3 lecturas. Quiero modo `both`, formato Markdown, podcast de 15 minutos y 20 preguntas."

**Configuración parcial que Claude debe fusionar con los valores por defecto:**

```json
{
  "processing": { "mode": "both" },
  "output": { "format": "md" },
  "podcast": { "target_duration_minutes": 15 },
  "questions": { "count": 20 }
}
```

**Salida esperada:** ZIP `material_estudio.zip` con:

- `individual/documento_0X/documento_0X_guia_estudio.md` (×3)
- `individual/documento_0X/documento_0X_podcast.md` (×3)
- `consolidado/resumen_general_consolidado.md`
- `consolidado/podcast_consolidado.md`
- `manifest.json`

---

## 🛠️ Instalación

1. Clona o copia esta carpeta en el directorio de Skills de tu entorno Claude (por ejemplo `.claude/skills/`).
2. Verifica que la estructura de carpetas sea idéntica a la mostrada arriba.
3. El skill se activará automáticamente cuando el usuario lo requiera.

---

## 📄 Licencia

MIT — ver `LICENSE`.