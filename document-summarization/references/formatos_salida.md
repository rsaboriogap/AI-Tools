# Formatos de salida, organización de archivos y manifiesto

## Markdown (`output.format = "md"`)

- Títulos jerárquicos.
- Listas para organizar conceptos.
- Tablas cuando mejoren la comprensión.
- Bloques Mermaid para mapas conceptuales.
- Conservar la numeración de secciones.
- Referencias a capítulos y páginas cuando estén disponibles.
- Sin encabezados vacíos ni contenido de relleno.

## Microsoft Word (`output.format = "docx"`)

- Documentos editables.
- Estilos de título y subtítulo; jerarquía visual coherente.
- Fuente Arial 12 para texto principal.
- Interlineado 1.5.
- Márgenes 2.54 cm.
- Tablas y viñetas cuando proceda.
- Mapas conceptuales como imágenes legibles cuando sea posible.
- Evitar división innecesaria de tablas y diagramas entre páginas.
- Índice cuando la extensión lo justifique.
- No agregar bibliografía no utilizada. Conservar datos bibliográficos originales.

## Estructura del ZIP

Nombre: `output.zip_name` (por defecto `material_estudio.zip`).

```
material_estudio.zip
│
├── individual/
│   ├── documento_01/
│   │   ├── documento_01_guia_estudio.md
│   │   └── documento_01_podcast.md
│   ├── documento_02/
│   │   ├── documento_02_guia_estudio.md
│   │   └── documento_02_podcast.md
│   └── documento_N/
│       ├── documento_N_guia_estudio.md
│       └── documento_N_podcast.md
│
├── consolidado/
│   ├── resumen_general_consolidado.md
│   └── podcast_consolidado.md
│
└── manifest.json
```

Reglas:

1. Crear solo las carpetas de las modalidades ejecutadas.
2. Crear solo los documentos habilitados por configuración.
3. Nombres de archivo y carpeta seguros.
4. No sobrescribir si dos documentos originales tienen el mismo nombre (añadir sufijo).
5. Sustituir `.md` por `.docx` cuando corresponda.
6. Incluir manifiesto solo si `output.include_manifest = true`.
7. Sin archivos temporales ni auxiliares.
8. Mantener la estructura de carpetas dentro del ZIP.

## Manifiesto `manifest.json`

```json
{
  "execution": {
    "mode": "both",
    "output_format": "md",
    "status": "completed",
    "effective_config": { }
  },
  "input_documents": [
    { "id": "documento_01", "filename": "lectura_01.pdf", "processing_status": "completed", "sections_analyzed": 8 }
  ],
  "generated_files": [
    { "source": "documento_01", "type": "study_guide", "path": "individual/documento_01/documento_01_guia_estudio.md" },
    { "source": "documento_01", "type": "podcast", "path": "individual/documento_01/documento_01_podcast.md" },
    { "source": "all", "type": "consolidated_summary", "path": "consolidado/resumen_general_consolidado.md" },
    { "source": "all", "type": "consolidated_podcast", "path": "consolidado/podcast_consolidado.md" }
  ],
  "warnings": []
}
```

**Estados permitidos:** `completed`, `partial`, `failed`, `skipped`.

El manifiesto debe reflejar la ejecución real; incluir siempre `effective_config`.

## Empaquetado

Usar `scripts/empaquetar_zip.py <directorio_resultados> <ruta_salida.zip>`.

Si el entorno no permite generar el ZIP, conservar los archivos individuales y proporcionar las rutas o enlaces disponibles, informando la limitación.

## Formato de entrega final

```
**Resultado del análisis documental**

**Configuración utilizada**
- Modalidad: [individual | consolidated | both]
- Profundidad: [basic | detailed | exhaustive]
- Formato: [md | docx]
- Duración objetivo del podcast: [min]
- Preguntas por documento: [n]

**Resultados generados**
- Documentos originales procesados: [n]
- Guías de estudio individuales: [n]
- Podcasts individuales: [n]
- Resúmenes consolidados: [n]
- Podcasts consolidados: [n]
- Archivo ZIP: [nombre]

**Descarga:** [enlace o ruta]

**Observaciones:** [limitaciones o advertencias]
```