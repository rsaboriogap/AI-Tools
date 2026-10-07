# Ejemplos de Preview - Paso 2

Este documento muestra cómo se vería el preview (Paso 2) con diferentes configuraciones.

---

## Ejemplo 1: Configuración Individual Básica

**Archivo de configuración:**
```json
{
  "processing": {"mode": "individual"},
  "chapter_analysis": {"enabled": true},
  "conceptual_map": {"enabled": true},
  "questions": {"enabled": true},
  "podcast": {"enabled": false},
  "presentation": {"enabled": false},
  "output": {"generate_zip": true, "include_manifest": true}
}
```

**Preview que se mostraría:**

```
📄 DOCUMENTOS A ANALIZAR
- codigo_etica.pdf (PDF, 1250 KB, 30 páginas)
Total: 1 documento

📋 ARCHIVOS QUE SE GENERARÁN

Para CADA documento (si mode = "individual"):
  ✓ guia_estudio_codigo_etica.md
    └─ Resumen general
    └─ Análisis por capítulo (13 capítulos)
    └─ 10 preguntas de estudio
    └─ Mapa conceptual Mermaid (profundidad máx. 5)

Archivos finales:
  ✓ manifest.json (metadatos de procesamiento)
  ✓ test.zip (todos los archivos empaquetados)

⚙️ CONFIGURACIÓN EFECTIVA
- Modalidad: individual
- Profundidad: detailed
- Idioma: es
- Formato: md
- Estructura: preservada
- Referencias de página: incluidas
- Ejemplos prácticos: incluidos

RESUMEN DE GENERACIÓN
- Documentos a procesar: 1
- Guías de estudio: ✓
- Presentaciones PowerPoint: ✗
- Podcasts educativos: ✗
- Análisis consolidados: ✗
- Mapas conceptuales: ✓
- Conjuntos de preguntas: ✓
- Archivo ZIP: ✓

¿Deseas proceder con esta configuración?
[Sí, proceder] [No, cancelar]
```

---

## Ejemplo 2: Configuración con Todo Habilitado (Individual)

**Archivo de configuración:**
```json
{
  "processing": {"mode": "individual"},
  "chapter_analysis": {"enabled": true, "key_concepts_per_chapter": 10},
  "conceptual_map": {"enabled": true, "max_depth": 5},
  "questions": {"enabled": true, "count": 15},
  "podcast": {"enabled": true, "target_duration_minutes": 20, "speakers": 2},
  "presentation": {"enabled": true, "slides_per_chapter": 3},
  "output": {"generate_zip": true, "include_manifest": true}
}
```

**Preview:**

```
📄 DOCUMENTOS A ANALIZAR
- codigo_etica.pdf (PDF, 1250 KB, 30 páginas)
Total: 1 documento

📋 ARCHIVOS QUE SE GENERARÁN

Para CADA documento (si mode = "individual"):
  ✓ guia_estudio_codigo_etica.md
    └─ Resumen general
    └─ Análisis por capítulo (10 conceptos por capítulo)
    └─ 15 preguntas de estudio
    └─ Mapa conceptual Mermaid (profundidad máx. 5)

  ✓ presentacion_codigo_etica.pptx
    └─ 40 diapositivas (3 por capítulo + título + resumen + mapa + preguntas)
    └─ Incluye notas del orador

  ✓ podcast_codigo_etica.md
    └─ Guión de 20 minutos (~2400-3000 palabras)
    └─ 2 participantes (diálogo)

Archivos finales:
  ✓ manifest.json (metadatos de procesamiento)
  ✓ test.zip (todos los archivos empaquetados)

⚙️ CONFIGURACIÓN EFECTIVA
- Modalidad: individual
- Profundidad: detailed
- Idioma: es
- Formato: md
- Estructura: preservada
- Referencias de página: incluidas
- Ejemplos prácticos: incluidos

RESUMEN DE GENERACIÓN
- Documentos a procesar: 1
- Guías de estudio: ✓
- Presentaciones PowerPoint: ✓
- Podcasts educativos: ✓
- Análisis consolidados: ✗
- Mapas conceptuales: ✓
- Conjuntos de preguntas: ✓
- Archivo ZIP: ✓

¿Deseas proceder con esta configuración?
[Sí, proceder] [No, cancelar]
```

---

## Ejemplo 3: Configuración Consolidada (Múltiples Documentos)

**Archivo de configuración:**
```json
{
  "processing": {
    "mode": "consolidated",
    "cross_document_analysis": true
  },
  "chapter_analysis": {"enabled": true},
  "conceptual_map": {"enabled": false},
  "questions": {"enabled": true},
  "podcast": {"enabled": false},
  "presentation": {"enabled": true},
  "consolidated": {
    "include_common_topics": true,
    "include_document_contributions": true,
    "include_similarities": true,
    "include_differences": true,
    "include_integrated_conclusions": true
  },
  "output": {"generate_zip": true, "include_manifest": true}
}
```

**Preview:**

```
📄 DOCUMENTOS A ANALIZAR
- codigo_etica_psicologia.pdf (PDF, 1250 KB, 30 páginas)
- codigo_etica_medicos.pdf (PDF, 890 KB, 25 páginas)
- codigo_etica_abogados.pdf (PDF, 1100 KB, 28 páginas)
Total: 3 documentos

📋 ARCHIVOS QUE SE GENERARÁN

Para CADA documento (si mode = "consolidado"):
  ✓ guia_estudio_codigo_etica_psicologia.md
    └─ Resumen general
    └─ Análisis por capítulo
    └─ 10 preguntas de estudio

  ✓ guia_estudio_codigo_etica_medicos.md
    └─ Resumen general
    └─ Análisis por capítulo
    └─ 10 preguntas de estudio

  ✓ guia_estudio_codigo_etica_abogados.md
    └─ Resumen general
    └─ Análisis por capítulo
    └─ 10 preguntas de estudio

Consolidados (SOLO si mode = "consolidado"):
  ✓ analisis_consolidado.md
    └─ Temas comunes entre los 3 códigos
    └─ Aportes específicos de cada documento
    └─ Similitudes encontradas
    └─ Diferencias encontradas
    └─ Conclusiones integradas

  ✓ presentacion_consolidada.pptx
    └─ 35+ diapositivas comparativas

Archivos finales:
  ✓ manifest.json (metadatos de procesamiento)
  ✓ test.zip (todos los archivos empaquetados)

⚙️ CONFIGURACIÓN EFECTIVA
- Modalidad: consolidated
- Profundidad: detailed
- Idioma: es
- Formato: md
- Análisis comparativo: activado
- Referencias de página: incluidas
- Ejemplos prácticos: incluidos

RESUMEN DE GENERACIÓN
- Documentos a procesar: 3
- Guías de estudio: ✓ (3 individuales)
- Presentaciones PowerPoint: ✓ (1 consolidada)
- Podcasts educativos: ✗
- Análisis consolidados: ✓
- Mapas conceptuales: ✗
- Conjuntos de preguntas: ✓ (3 individuales)
- Archivo ZIP: ✓

¿Desesar proceder con esta configuración?
[Sí, proceder] [No, cancelar]
```

---

## Ejemplo 4: Configuración Mínima (Solo Guías)

**Archivo de configuración:**
```json
{
  "processing": {"mode": "individual"},
  "chapter_analysis": {"enabled": false},
  "conceptual_map": {"enabled": false},
  "questions": {"enabled": false},
  "podcast": {"enabled": false},
  "presentation": {"enabled": false},
  "output": {"generate_zip": false, "include_manifest": false}
}
```

**Preview:**

```
📄 DOCUMENTOS A ANALIZAR
- codigo_etica.pdf (PDF, 1250 KB, 30 páginas)
Total: 1 documento

📋 ARCHIVOS QUE SE GENERARÁN

Para CADA documento (si mode = "individual"):
  ✓ guia_estudio_codigo_etica.md
    └─ Resumen general SOLAMENTE

⚙️ CONFIGURACIÓN EFECTIVA
- Modalidad: individual
- Profundidad: detailed
- Idioma: es
- Formato: md
- Estructura: preservada
- Referencias de página: incluidas
- Ejemplos prácticos: incluidos

RESUMEN DE GENERACIÓN
- Documentos a procesar: 1
- Guías de estudio: ✓
- Presentaciones PowerPoint: ✗
- Podcasts educativos: ✗
- Análisis consolidados: ✗
- Mapas conceptuales: ✗
- Conjuntos de preguntas: ✗
- Archivo ZIP: ✗

¿Deseas proceder con esta configuración?
[Sí, proceder] [No, cancelar]
```

---

## Notas Importantes

### Lo que Se Muestra:
✅ Lista clara de TODOS los documentos de entrada
✅ TODOS los archivos que se generarán (SOLO los habilitados)
✅ Configuración efectiva (valores reales que se usarán)
✅ Resumen visual de qué está activado/desactivado
✅ Solicitud explícita de aprobación

### Lo que NO se Muestra (aún):
❌ Contenido real de los documentos
❌ Ejemplos de qué habrá en las guías
❌ Texto de las preguntas

### Comportamiento Esperado:
- Si usuario elige **Sí**: Proceder con generación
- Si usuario elige **No**: Abortar sin generar nada
- Si usuario elige **Otro**: Permitir cambios en configuración (opcional)

---

## Reglas de Oro para el Preview

1. **Se genera SOLO lo que está habilitado**
   - `enabled: false` → NO aparece en la lista

2. **Valores exactos**
   - Si `count: 15` → mostrar "15 preguntas"
   - Si `slides_per_chapter: 3` → mostrar "3 por capítulo"

3. **Nombres de archivos reales**
   - Usar nombres exactos que se generarán
   - Incluir extensiones

4. **Configuración actual**
   - Mostrar valores reales (no defaults si están sobrescritos)
   - Reflejar las prioridades de carga aplicadas

5. **Claridad**
   - Lista con viñetas
   - Jerárquica (indentación)
   - Símbolos (✓/✗) para claridad
