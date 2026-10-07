# Ejemplo 02 — Análisis consolidado en Word (.docx)

## Caso de uso

Un docente sube **tres artículos académicos** sobre un mismo tema y pide un resumen integrado + podcast conjunto, en formato Word editable.

## Entrada del usuario

> "Te paso tres papers sobre aprendizaje significativo. Quiero un análisis
> consolidado que los integre, con podcast, y me lo entregues en Word
> para poder editarlo."

## Configuración resultante

```json
{
  "processing": {
    "mode": "consolidated",
    "analysis_depth": "detailed",
    "cross_document_analysis": true
  },
  "output": {
    "format": "docx",
    "generate_zip": true,
    "zip_name": "material_estudio.zip",
    "include_manifest": true
  },
  "consolidated": {
    "include_common_topics": true,
    "include_document_contributions": true,
    "include_similarities": true,
    "include_differences": true,
    "include_integrated_conclusions": true
  },
  "podcast": {
    "target_duration_minutes": 15,
    "speakers": 2
  }
}
```

## Estructura del ZIP generado

```
material_estudio.zip
│
├── consolidado/
│   ├── resumen_general_consolidado.docx
│   └── podcast_consolidado.docx
│
└── manifest.json
```

## Formato Word aplicado

- Fuente Arial 12 para texto principal.
- Interlineado 1.5.
- Márgenes 2.54 cm.
- Estilos de título y subtítulo.
- Mapa conceptual insertado como imagen.
- Índice automático si la extensión lo justifica.

## Notas de ejecución

- Modo `consolidated` → **no** se generan archivos individuales.
- Si el renderizado de Mermaid a imagen no está disponible, se incluye un
  esquema jerárquico alternativo y se reporta la limitación en el manifiesto.