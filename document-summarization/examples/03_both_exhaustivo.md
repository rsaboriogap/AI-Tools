# Ejemplo 03 — Análisis `both` con profundidad exhaustiva

## Caso de uso

Un grupo de investigación necesita **material completo** (individual + consolidado) a partir de **dos capítulos de un manual**. Quieren profundidad máxima, mapa conceptual exhaustivo, y el podcast más largo posible.

## Entrada del usuario

> "Tengo dos capítulos de un manual de metodología. Necesito material de
> estudio completísimo: guías individuales, resumen consolidado, mapas
> conceptuales, podcasts. Usa modo both, profundidad exhaustiva y 20
> preguntas por documento."

## Configuración resultante

```json
{
  "processing": {
    "mode": "both",
    "analysis_depth": "exhaustive",
    "preserve_original_structure": true,
    "include_page_references": true,
    "cross_document_analysis": true
  },
  "output": {
    "format": "md",
    "generate_zip": true,
    "zip_name": "material_estudio.zip",
    "include_manifest": true
  },
  "chapter_analysis": {
    "enabled": true,
    "key_concepts_per_chapter": 8
  },
  "conceptual_map": {
    "enabled": true,
    "format": "mermaid",
    "max_depth": 5,
    "include_relationship_labels": true
  },
  "podcast": {
    "enabled": true,
    "target_duration_minutes": 20,
    "speakers": 2
  },
  "questions": {
    "enabled": true,
    "count": 20,
    "difficulty": "mixed"
  }
}
```

## Estructura del ZIP generado

```
material_estudio.zip
│
├── individual/
│   ├── capitulo_01_manual/
│   │   ├── capitulo_01_manual_guia_estudio.md
│   │   └── capitulo_01_manual_podcast.md
│   └── capitulo_02_manual/
│       ├── capitulo_02_manual_guia_estudio.md
│       └── capitulo_02_manual_podcast.md
│
├── consolidado/
│   ├── resumen_general_consolidado.md
│   └── podcast_consolidado.md
│
└── manifest.json
```

## Distribución de preguntas (20, mixed)

| Tipo | Cantidad |
|---|---|
| Conceptual | 4 |
| Comprensión | 4 |
| Analítica | 4 |
| Relación | 4 |
| Aplicación | 4 |

## Notas de ejecución

- Modo `both` → 6 archivos individuales + 2 consolidados + manifiesto.
- Cada podcast individual ≈ 20 min (~2 400–3 000 palabras).
- `max_depth` del mapa subido a 5 → subramas más detalladas.