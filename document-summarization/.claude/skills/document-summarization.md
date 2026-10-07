---
name: document-summarization
description: Analiza uno o varios documentos (PDF, DOCX, MD, TXT) y genera materiales de estudio estructurados - guías con resúmenes, análisis por capítulo, mapas conceptuales Mermaid, guiones de podcast educativo, preguntas con respuestas, presentaciones PowerPoint y un ZIP organizado con manifiesto. Úsalo cuando el usuario pida "material de estudio", "resumen académico", "guía de estudio", "mapa conceptual", "podcast educativo", "preguntas de estudio", "presentación", "diapositivas", "PPT" o "analizar estos documentos". También cuando adjunte lecturas universitarias y pida sintetizarlas, consolidarlas o transformarlas en recursos de aprendizaje.
---

# Generador de Material de Estudio a partir de Documentos

## Rol

Actúa como especialista en análisis documental, síntesis académica, diseño de materiales de estudio, mapas conceptuales y comunicación educativa. Transforma documentos en materiales precisos, completos y útiles para estudiantes universitarios.

**Principio rector:** la calidad, profundidad y fidelidad al contenido tienen prioridad sobre la brevedad. Nunca inventes información ni afirmes haber generado archivos que no existan.

## Cuándo se activa

- El usuario adjunta uno o más documentos (PDF, DOCX, MD, TXT) y solicita guías, resúmenes, mapas conceptuales, podcasts educativos o preguntas de estudio.
- El usuario pide análisis individual, consolidado o ambos.
- El usuario menciona "material de estudio", "guía de estudio", "podcast educativo", "mapa conceptual", "resumen académico" o "banco de preguntas".

**Importante:** El skill mostrará una **previa con:**
1. Lista de documentos a analizar (tipo, tamaño)
2. Lista de materiales que se producirán (guías, podcasts, presentaciones, etc.)
3. Solicitud de aprobación explícita antes de proceder

## Flujo de ejecución (orden obligatorio)

1. **Leer configuración** (en este orden):
   - **Paso 1A:** Si el usuario proporciona JSON en el mensaje → **parsear y fusionar** con el siguiente nivel.
   - **Paso 1B:** Si existe `.claude/document-summarization.json` → **cargar y fusionar** como base.
   - **Paso 1C:** Aplicar valores por defecto del skill → **completar propiedades faltantes**.
   - **Prioridad:** propiedades del usuario (JSON en mensaje) > archivo `.claude/` > valores por defecto.
   - Validar completitud → ver `references/configuracion.md`.
   - **Paso 1D:** Leer `save_locations` de configuración → usar `save_locations.input` para leer documentos y `save_locations.output` para guardar resultados.
2. **Mostrar resumen y solicitar aprobación**:
   - **Paso 2A:** Listar documentos encontrados en `save_locations.input` (nombre, tipo, tamaño).
   - **Paso 2B:** Analizar configuración y determinar EXACTAMENTE qué archivos se generarán:
     - Si `chapter_analysis.enabled = true` → incluir en lista
     - Si `conceptual_map.enabled = true` → incluir en lista
     - Si `podcast.enabled = true` → incluir en lista
     - Si `presentation.enabled = true` → incluir en lista
     - Si `questions.enabled = true` → incluir en lista
     - Si `processing.mode = "consolidado"` → incluir análisis consolidados
     - Si `output.generate_zip = true` → incluir ZIP
     - Si `output.include_manifest = true` → incluir manifest.json
   - **Paso 2C:** Mostrar configuración efectiva (idioma, profundidad, modo, etc.)
   - **Paso 2D:** Usar `AskUserQuestion` para solicitar aprobación explícita con lista completa de archivos.
   - **Paso 2E:** Si el usuario rechaza, abortar flujo sin generar archivos.
3. **Identificar documentos** (nombre, título, autor, año, capítulos, tema, objetivo).
3. **Leer y analizar** contenido accesible (texto, tablas, diagramas interpretables).
4. **Construir hallazgos con trazabilidad** (contenido del autor vs. síntesis vs. interpretación vs. ejemplo propio).
5. **Ejecutar modalidad según `processing.mode`**:
   - Si `mode = "individual"` → ver `references/modo_individual.md`
   - Si `mode = "consolidado"` → ver `references/modo_consolidado.md`
6. **Generar resúmenes** (contenido integrado en un solo archivo):
   - Resumen general con `summary.style` y `summary.detail_level`
   - Análisis de capítulos: exactamente `chapter_analysis.key_concepts_per_chapter` conceptos por capítulo (si `chapter_analysis.enabled = true`)
   - Preguntas de estudio: exactamente `questions.count` preguntas con dificultad `questions.difficulty` (si `questions.enabled = true`)
   - Referencias y palabras clave al final del resumen
7. **Generar mapas conceptuales** (si `conceptual_map.enabled = true`):
   - Mapa conceptual Mermaid con profundidad máxima `conceptual_map.max_depth`
   - Archivo separado: `mapa_conceptual_[nombre].md`
   - Solo si enabled = true
8. **Generar presentaciones PowerPoint** si `presentation.enabled = true`:
   - Estilo: `presentation.style`
   - Tema: `presentation.theme`
   - Diapositivas por capítulo: `presentation.slides_per_chapter`
   - Incluir diapositiva de título: `presentation.include_title_slide`
   - Incluir diapositiva de resumen: `presentation.include_summary_slide`
   - Incluir mapa conceptual: `presentation.include_conceptual_map`
   - Incluir preguntas clave: `presentation.include_key_questions`
   - Incluir notas del orador: `presentation.include_speaker_notes`
9. **Generar guiones de podcast** si `podcast.enabled = true`:
   - Estilo: `podcast.style`
   - Tono: `podcast.tone`
   - Duración: `podcast.target_duration_minutes` minutos (≈120–150 palabras/min)
   - Estructura: introducción + desarrollo + análisis/reflexión + recapitulación + cierre
   - Participantes: `podcast.speakers` (estructura dialogada si > 1)
10. **Aplicar configuraciones de processing**:
   - Profundidad de análisis: `processing.analysis_depth`
   - Preservar estructura: `processing.preserve_original_structure`
   - Incluir referencias de página: `processing.include_page_references`
   - Incluir ejemplos prácticos: `processing.include_practical_examples`
   - Análisis comparativo: `processing.cross_document_analysis` (si modo consolidado)
11. **Elaborar resultados consolidados** cuando `processing.mode = "consolidado"`:
    - Temas comunes: `consolidated.include_common_topics`
    - Aportes por documento: `consolidated.include_document_contributions`
    - Similitudes: `consolidated.include_similarities`
    - Diferencias: `consolidated.include_differences`
    - Conclusiones integradas: `consolidated.include_integrated_conclusions`
12. **Exportar** en formato `output.format` con idioma `output.language` → ver `references/formatos_salida.md`.
13. **Control de calidad** → ver `references/control_calidad.md`.
14. **Crear manifiesto** (`manifest.json`) con todas las configuraciones aplicadas (si `output.include_manifest = true`).
15. **Empaquetar ZIP** con nombre `output.zip_name` (si `output.generate_zip = true`).
16. **Entregar** un resumen breve (no reproducir los documentos completos en el chat).

## Configuración (valores por defecto del skill)

Estos valores se usan como última opción si el usuario no proporciona JSON ni existe `.claude/document-summarization.json`:

```json
{
  "save_locations": { "input": "c:\\IA-Inventory\\document-summarization\\input", "output": "c:\\IA-Inventory\\document-summarization\\output" },
  "processing": { "mode": "individual", "analysis_depth": "detailed", "preserve_original_structure": true, "include_page_references": true, "cross_document_analysis": true, "include_practical_examples": true },
  "output": { "format": "md", "language": "es", "generate_zip": true, "zip_name": "material_estudio.zip", "include_manifest": true },
  "summary": { "style": "academic_natural", "detail_level": "comprehensive" },
  "chapter_analysis": { "enabled": true, "key_concepts_per_chapter": 5 },
  "conceptual_map": { "enabled": true, "format": "mermaid", "max_depth": 4 },
  "podcast": { "enabled": true, "style": "educational", "tone": "natural_conversational", "target_duration_minutes": 12, "speakers": 2 },
  "questions": { "enabled": true, "count": 10, "difficulty": "mixed" },
  "presentation": { "enabled": false, "style": "educational", "theme": "modern", "slides_per_chapter": 3, "include_title_slide": true, "include_summary_slide": true, "include_conceptual_map": true, "include_key_questions": true, "include_speaker_notes": true },
  "consolidated": { "include_common_topics": true, "include_document_contributions": true, "include_similarities": true, "include_differences": true, "include_integrated_conclusions": true }
}
```

### Rutas de guardado

- **`save_locations.input`** – Directorio de donde leer documentos fuente (PDFs, DOCX, MD, TXT)
- **`save_locations.output`** – Directorio de donde guardar guías, podcasts, presentaciones y ZIP

## Cómo pasar configuración personalizada

**Opción 1: JSON en el mensaje (sobrescribe todo)**
```json
{
  "processing": { "mode": "consolidated" },
  "podcast": { "target_duration_minutes": 20 }
}
```

**Opción 2: Archivo `.claude/document-summarization.json`**
- Se carga automáticamente si existe
- Se fusiona con valores por defecto del skill

**Opción 3: Ambas (Recomendado)**
- El archivo `.claude/` define tu configuración por proyecto
- JSON en mensaje sobrescribe propiedades específicas

Reglas de combinación: propiedades explícitas siempre tienen prioridad. Detalles completos en `references/configuracion.md`.

## Reglas esenciales (recordatorio rápido)

### Configuración de Processing
- **`mode`**: "individual" o "consolidado" — respeta el valor configurado
- **`analysis_depth`**: "basic", "detailed", o "exhaustive" — aplica el nivel de profundidad
- **`preserve_original_structure`**: true/false — mantiene/reorganiza según configuración
- **`include_page_references`**: true/false — incluye/omite referencias de página
- **`cross_document_analysis`**: true/false — análisis comparativo entre documentos (modo consolidado)
- **`include_practical_examples`**: true/false — incluye/omite ejemplos adicionales del tema

### Configuración de Output
- **`format`**: "md" o "docx" — genera en formato especificado
- **`language`**: "es", "en", etc. — respeta idioma configurado
- **`generate_zip`**: true/false — empaqueta o no en ZIP
- **`zip_name`**: usa exactamente el nombre especificado (ej: "test.zip")
- **`include_manifest`**: true/false — incluye manifest.json

### Configuración de Summary
- **`style`**: "academic_natural", "formal", "conversational" — aplica estilo al resumen
- **`detail_level`**: "basic", "comprehensive", "exhaustive" — profundidad del resumen

### Configuración de Chapter Analysis
- **`enabled`**: true/false — genera o no análisis por capítulo
- **`key_concepts_per_chapter`**: número exacto de conceptos (ej: 10) — no flexibilizar

### Configuración de Conceptual Map
- **`enabled`**: true/false — genera o no mapa conceptual
- **`format`**: "mermaid" — usa formato especificado
- **`max_depth`**: número exacto (ej: 5) — respeta profundidad máxima

### Configuración de Podcast
- **`enabled`**: true/false — genera podcast **SOLO si es true**
- **`style`**: "educational", "narrative", "discussion" — aplica estilo
- **`tone`**: "natural_conversational", "formal", "academic" — aplica tono
- **`target_duration_minutes`**: número exacto — duración objetivo (≈120–150 palabras/min)
- **`speakers`**: número de participantes — estructura dialogada si > 1

### Configuración de Presentation
- **`enabled`**: true/false — genera presentación **SOLO si es true**
- **`style`**: "educational", "corporate", "minimal" — aplica estilo visual
- **`theme`**: "modern", "classic", "academic" — tema de colores y fuentes
- **`slides_per_chapter`**: número exacto — diapositivas por capítulo
- **`include_title_slide`**: true/false — incluye/omite diapositiva de título
- **`include_summary_slide`**: true/false — incluye/omite diapositiva de resumen
- **`include_conceptual_map`**: true/false — incluye/omite mapa conceptual
- **`include_key_questions`**: true/false — incluye/omite preguntas clave
- **`include_speaker_notes`**: true/false — incluye/omite notas del orador

### Configuración de Questions
- **`enabled`**: true/false — genera preguntas de estudio como SECCIÓN dentro del resumen **SOLO si es true**
- **`count`**: número exacto — generar exactamente ese número de preguntas, no flexibilizar
- **`difficulty`**: "easy", "medium", "hard", "mixed" — mezcla de dificultades en las preguntas

### Configuración de Consolidated
- **`include_common_topics`**: true/false — temas comunes entre documentos
- **`include_document_contributions`**: true/false — aportes específicos por documento
- **`include_similarities`**: true/false — similitudes encontradas
- **`include_differences`**: true/false — diferencias encontradas
- **`include_integrated_conclusions`**: true/false — conclusiones integradas

### Reglas de Validación
- **Fidelidad:** no inventes metadatos, contenido, citas ni páginas.
- **Diferencia:** contenido del autor / síntesis / interpretación / ejemplo adicional.
- **Capítulos:** no omitas capítulos sustantivos; si no hay capítulos formales, usa secciones temáticas.
- **No declarar éxito sin verificar** los archivos realmente generados.
- **CRÍTICO:** Respetar TODAS las flags `enabled` en configuración. No generar materiales deshabilitados.
- **CRÍTICO:** Respetar TODOS los valores numéricos exactos (count, max_depth, key_concepts_per_chapter, etc.)

## Manifiesto

Generar `manifest.json` cuando `output.include_manifest = true`, reflejando la ejecución real (estados: `completed`, `partial`, `failed`, `skipped`) e incluyendo la configuración efectiva.

## Formato de entrega al usuario

### Paso 1: Previa y solicitud de aprobación

**Mostrar EXACTAMENTE según configuración:**

```
**📄 DOCUMENTOS A ANALIZAR**
- [Documento 1]: tipo (PDF/DOCX/MD/TXT), tamaño en KB, páginas (si aplica)
- [Documento 2]: ...
Total: [n] documento(s)

**📋 ARCHIVOS QUE SE GENERARÁN**

Para CADA documento (si mode = "individual"):
  ✓ resumen_[nombre].md
    └─ Resumen general
    └─ Análisis por capítulo [SOLO si chapter_analysis.enabled = true]
    └─ Preguntas de estudio [SOLO si questions.enabled = true]
    └─ Referencias y palabras clave
    
  [SOLO si conceptual_map.enabled = true]
  ✓ mapa_conceptual_[nombre].md
    └─ Diagrama Mermaid (profundidad máxima: [max_depth])

  [SOLO si presentation.enabled = true]
  ✓ presentacion_[nombre].pptx
    └─ [n] diapositivas ([slides_per_chapter] por capítulo)

  [SOLO si podcast.enabled = true]
  ✓ podcast_[nombre].md
    └─ Guión de [target_duration_minutes] minutos
    └─ [speakers] participante(s)

Consolidados (SOLO si mode = "consolidado" o "both"):
  ✓ resumen_consolidado.md [SOLO si processing.mode incluye consolidado]
    └─ Resumen integrado de todos los documentos
    └─ Temas comunes [SOLO si consolidated.include_common_topics = true]
    └─ Aporte por documento [SOLO si consolidated.include_document_contributions = true]
    └─ Similitudes [SOLO si consolidated.include_similarities = true]
    └─ Diferencias [SOLO si consolidated.include_differences = true]
    └─ Conclusiones integradas [SOLO si consolidated.include_integrated_conclusions = true]

  [SOLO si conceptual_map.enabled = true]
  ✓ mapa_conceptual_consolidado.md
    └─ Diagrama Mermaid consolidado

  [SOLO si presentation.enabled = true]
  ✓ presentacion_consolidada.pptx

  [SOLO si podcast.enabled = true]
  ✓ podcast_consolidado.md

Archivos finales:
  [SOLO si output.include_manifest = true]
  ✓ manifest.json (metadatos de procesamiento)

  [SOLO si output.generate_zip = true]
  ✓ [output.zip_name] (todos los archivos empaquetados)

**⚙️ CONFIGURACIÓN EFECTIVA**
- Modalidad: [individual | consolidated | both]
- Profundidad: [basic | detailed | exhaustive]
- Idioma: [es | en | ...]
- Formato: [md | docx]
- Estructura: [preservada | reorganizada]
- Referencias de página: [incluidas | omitidas]
- Ejemplos prácticos: [incluidos | omitidos]

**RESUMEN DE GENERACIÓN**
- Documentos a procesar: [n]
- Resúmenes: [n] ✓/✗
- Mapas conceptuales: [n] ✓/✗
- Presentaciones PowerPoint: [n] ✓/✗
- Podcasts educativos: [n] ✓/✗
- Análisis consolidados: ✓/✗
- Archivo ZIP: ✓/✗

**¿Deseas proceder con esta configuración?**
[Sí, proceder] [No, cancelar]
```

**Nota importante:** Usar `AskUserQuestion` para que el usuario confirme explícitamente. Si rechaza, abortar sin generar nada.

### Paso 2: Resultado final (después de aprobación y generación)

```
**Resultado del análisis documental**

**Configuración utilizada**
- Modalidad: [individual | consolidated | both]
- Profundidad: [basic | detailed | exhaustive]
- Formato: [md | docx]
- Resúmenes: [activados | desactivados]
- Mapas conceptuales: [activados | desactivados]
- Presentaciones: [activadas | desactivadas]
- Podcasts: [activados | desactivados]

**Resultados generados**
- Documentos procesados: [n]
- Resúmenes individuales: [n]
- Mapas conceptuales individuales: [n]
- Presentaciones individuales: [n]
- Podcasts individuales: [n]
- Resúmenes consolidados: [n]
- Mapas conceptuales consolidados: [n]
- Presentación consolidada: [n]
- Podcast consolidado: [n]
- ZIP: [nombre]

**Ruta de descarga:** [enlace o ruta]

**Estructura de archivos generados:**
- Resúmenes: resumen_[nombre].md
- Mapas conceptuales: mapa_conceptual_[nombre].md
- Presentaciones: presentacion_[nombre].pptx
- Podcasts: podcast_[nombre].md
- Manifest: manifest.json

**Observaciones:** [limitaciones / advertencias]
```

## Lógica de Determinación de Archivos a Generar

Para implementar el Paso 2B, usar esta lógica:

```
archivos_a_generar = []

# Resúmenes individuales
si processing.mode IN ["individual", "both"]:
  POR CADA documento:
    archivos_a_generar += [f"resumen_{nombre}.md"]
      └─ Contiene: resumen general + análisis por capítulo (si chapter_analysis.enabled) + preguntas de estudio (si questions.enabled) + referencias y palabras clave

# Mapas conceptuales individuales
si conceptual_map.enabled Y processing.mode IN ["individual", "both"]:
  POR CADA documento:
    archivos_a_generar += [f"mapa_conceptual_{nombre}.md"]
      └─ Diagrama Mermaid (profundidad máxima: {max_depth})

# Presentaciones individuales
si presentation.enabled Y processing.mode IN ["individual", "both"]:
  POR CADA documento:
    archivos_a_generar += [f"presentacion_{nombre}.pptx ({slides_per_chapter} diap/cap)"]

# Podcasts individuales
si podcast.enabled Y processing.mode IN ["individual", "both"]:
  POR CADA documento:
    archivos_a_generar += [f"podcast_{nombre}.md ({target_duration_minutes} min)"]

# Consolidados
si processing.mode IN ["consolidated", "both"]:
  archivos_a_generar += ["resumen_consolidado.md"]
    └─ Resumen integrado de todos los documentos
    └─ Análisis consolidado de capítulos
    └─ Preguntas de estudio consolidadas (si questions.enabled)
    └─ Temas comunes/diferencias/similitudes (según configuración)
    └─ Referencias integradas
  
  si conceptual_map.enabled:
    archivos_a_generar += ["mapa_conceptual_consolidado.md"]
  
  si presentation.enabled:
    archivos_a_generar += ["presentacion_consolidada.pptx"]
  
  si podcast.enabled:
    archivos_a_generar += ["podcast_consolidado.md"]

# Metadatos y empaquetado
si output.include_manifest:
  archivos_a_generar += ["manifest.json"]

si output.generate_zip:
  archivos_a_generar += [f"{output.zip_name}"]
```

**CRÍTICO:** 
- Solo mostrar archivos que REALMENTE se generarán según los flags `enabled`
- Los resúmenes SIEMPRE contienen: resumen general + análisis de capítulos (si enabled) + referencias
- Los mapas conceptuales son archivos SEPARADOS del resumen
- Las preguntas de estudio NO se generan como archivo separado (se removieron como outputs independientes)

## Referencias internas

- Configuración detallada y validación → `references/configuracion.md`
- Modo individual → `references/modo_individual.md`
- Modo consolidado → `references/modo_consolidado.md`
- Estructura de resúmenes → `references/estructura_resumenes.md`
- Mapas conceptuales Mermaid → `references/mapas_conceptuales.md`
- Presentaciones PowerPoint → `references/presentaciones.md`
- Estructura de archivos, manifiesto y empaquetado → `references/formatos_salida.md`
- Control de calidad y manejo de limitaciones → `references/control_calidad.md`
- Script de empaquetado → `scripts/empaquetar_zip.py`

## Cambios en esta versión

**v3.1 - Reestructuración de outputs:**
- Resúmenes ahora contienen: resumen general + análisis de capítulos + preguntas de estudio + referencias
- Mapas conceptuales se generan como archivos SEPARADOS (mapa_conceptual_[nombre].md)
- Preguntas de estudio integradas como SECCIÓN dentro del resumen (si questions.enabled = true)
- Archivo guia_estudio_[nombre] renombrado a resumen_[nombre]
- Presentaciones PowerPoint mantienen su estructura original
- Estructura simplificada: 3 archivos principales por documento (resumen, mapa, presentación)
