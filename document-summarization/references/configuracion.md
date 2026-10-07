# Guía de Configuración Completa

## Estructura de Carga (Prioridad)

1. **JSON en mensaje del usuario** (máxima prioridad)
2. **`.claude/document-summarization.json`** (proyecto)
3. **Valores por defecto del skill** (fallback)

## Esquema Completo (Valores por Defecto del Skill)

```json
{
  "save_locations": {
    "input": "c:\\IA-Inventory\\document-summarization\\input",
    "output": "c:\\IA-Inventory\\document-summarization\\output"
  },
  "processing": {
    "mode": "individual",
    "analysis_depth": "detailed",
    "preserve_original_structure": true,
    "include_page_references": true,
    "cross_document_analysis": true,
    "include_practical_examples": true
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
    "detail_level": "comprehensive"
  },
  "chapter_analysis": {
    "enabled": true,
    "key_concepts_per_chapter": 5
  },
  "conceptual_map": {
    "enabled": true,
    "format": "mermaid",
    "max_depth": 4
  },
  "podcast": {
    "enabled": true,
    "style": "educational",
    "tone": "natural_conversational",
    "target_duration_minutes": 12,
    "speakers": 2
  },
  "questions": {
    "enabled": true,
    "count": 10,
    "difficulty": "mixed"
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
  "consolidated": {
    "include_common_topics": true,
    "include_document_contributions": true,
    "include_similarities": true,
    "include_differences": true,
    "include_integrated_conclusions": true
  }
}
```

## Referencia Detallada de Propiedades

### `save_locations` (REQUERIDO)
```json
"save_locations": {
  "input": "ruta/a/documentos",
  "output": "ruta/para/guardar"
}
```
- **`input`**: Directorio con documentos fuente (PDF, DOCX, MD, TXT)
- **`output`**: Directorio para guardar resultados

### `processing` (Análisis)
```json
"processing": {
  "mode": "individual | consolidated | both",
  "analysis_depth": "basic | detailed | exhaustive",
  "preserve_original_structure": true/false,
  "include_page_references": true/false,
  "cross_document_analysis": true/false,
  "include_practical_examples": true/false
}
```

| Propiedad | Valores | Efecto |
|-----------|---------|--------|
| `mode` | individual, consolidated, both | individual: por documento. consolidated: comparativo. both: ambos |
| `analysis_depth` | basic, detailed, exhaustive | Profundidad del análisis |
| `preserve_original_structure` | true, false | true: respeta orden del documento |
| `include_page_references` | true, false | true: incluye números de página |
| `cross_document_analysis` | true, false | true: análisis comparativo (modo consolidated) |
| `include_practical_examples` | true, false | true: agrega ejemplos derivados |

### `output` (Formato y Salida)
```json
"output": {
  "format": "md | docx",
  "language": "es | en | fr",
  "generate_zip": true/false,
  "zip_name": "nombre.zip",
  "include_manifest": true/false
}
```

### `summary` (Resumen General)
```json
"summary": {
  "style": "academic_natural | formal | conversational",
  "detail_level": "basic | comprehensive | exhaustive"
}
```

### `chapter_analysis` (Análisis por Capítulo)
```json
"chapter_analysis": {
  "enabled": true/false,
  "key_concepts_per_chapter": número
}
```
⚠️ **Si enabled=false**: NO generar análisis de capítulos

### `conceptual_map` (Mapa Conceptual)
```json
"conceptual_map": {
  "enabled": true/false,
  "format": "mermaid",
  "max_depth": número
}
```
⚠️ **Si enabled=false**: NO generar mapa conceptual

### `podcast` (Podcast Educativo)
```json
"podcast": {
  "enabled": true/false,
  "style": "educational | narrative | discussion",
  "tone": "natural_conversational | formal | academic",
  "target_duration_minutes": número,
  "speakers": número
}
```
🚨 **Si enabled=false**: NO generar podcast bajo ninguna circunstancia

### `presentation` (Presentación PowerPoint)
```json
"presentation": {
  "enabled": true/false,
  "style": "educational | corporate | minimal",
  "theme": "modern | classic | academic",
  "slides_per_chapter": número,
  "include_title_slide": true/false,
  "include_summary_slide": true/false,
  "include_conceptual_map": true/false,
  "include_key_questions": true/false,
  "include_speaker_notes": true/false
}
```
🚨 **Si enabled=false**: NO generar presentación bajo ninguna circunstancia

### `questions` (Preguntas de Estudio)
```json
"questions": {
  "enabled": true/false,
  "count": número,
  "difficulty": "easy | medium | hard | mixed"
}
```
🚨 **Si enabled=false**: NO generar preguntas bajo ninguna circunstancia

### `consolidated` (Análisis Consolidado - solo si mode="consolidated")
```json
"consolidated": {
  "include_common_topics": true/false,
  "include_document_contributions": true/false,
  "include_similarities": true/false,
  "include_differences": true/false,
  "include_integrated_conclusions": true/false
}
```

## Reglas CRÍTICAS de Validación

### Prioridades Absolutas

1. ✋ **Las propiedades explícitas del usuario SIEMPRE tienen prioridad**
2. ✋ **JSON en mensaje > archivo `.claude/` > defaults del skill**
3. ✋ **Fusionar JSON parcial recursivamente con defaults**

### Flags `enabled` - REGLA DE ORO

| Flag | Valor false | Acción |
|------|-------------|--------|
| `chapter_analysis.enabled` | false | OMITIR completamente análisis de capítulos |
| `conceptual_map.enabled` | false | OMITIR completamente mapa conceptual |
| `podcast.enabled` | false | **OMITIR completamente podcast - NO generar bajo ninguna circunstancia** |
| `presentation.enabled` | false | **OMITIR completamente presentación - NO generar bajo ninguna circunstancia** |
| `questions.enabled` | false | **OMITIR completamente preguntas - NO generar bajo ninguna circunstancia** |
| `output.generate_zip` | false | NO empaquetar en ZIP, entregar archivos individuales |

### Validaciones Numéricas

- `questions.count` → generar EXACTAMENTE ese número (no flexibilizar)
- `chapter_analysis.key_concepts_per_chapter` → EXACTAMENTE ese número por capítulo
- `conceptual_map.max_depth` → NO exceder esa profundidad
- `presentation.slides_per_chapter` → EXACTAMENTE ese número por capítulo
- `podcast.target_duration_minutes` → aproximado (120-150 palabras/min)
- `podcast.speakers` → número de participantes (1=monólogo, 2+=diálogo)

### Valores de Cadena

- `output.zip_name` → usar EXACTAMENTE ese nombre (ej: "test.zip")
- `processing.mode` → "individual", "consolidated" o "both"
- `output.language` → respetar idioma configurado
- `output.format` → "md" o "docx"

### Reglas de Modo

- **`mode = "individual"`**: generar análisis por documento
- **`mode = "consolidated"`**: generar análisis comparativo + propiedades `consolidated.*`
- **`mode = "both"`**: generar ambos tipos de análisis
- `cross_document_analysis` → solo aplica si mode="consolidated"

### Reglas de Calidad

1. Validar tipos de datos
2. No generar archivos vacíos para funcionalidades desactivadas
3. Registrar configuración efectiva en `manifest.json`
4. Informar limitaciones técnicas sin afirmar falsos éxitos
5. No inventer información faltante