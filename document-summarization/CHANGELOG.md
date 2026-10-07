# Changelog

Todos los cambios notables de este skill se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el versionado sigue [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### Añadido
- **Generación de presentaciones PowerPoint** como componente de materiales de estudio.
- Configuración `presentation` con opciones de estilo, tema, diapositivas por capítulo y notas del orador.
- Documento de referencia `references/presentaciones.md` con guía completa de opciones.
- Ejemplo práctico `examples/05_presentacion_educativa.md` con configuraciones y uso.
- Soporte para presentaciones individuales y consolidadas (modo `both`).
- Temas visuales: `modern`, `classic`, `colorful`, `dark`.
- Estilos de presentación: `educational`, `corporate`, `minimalist`.

### Planeado
- Soporte para exportación a PDF con estilo académico.
- Integración con herramientas de text-to-speech para previsualización del podcast.
- Plantillas de mapa conceptual por dominio (ciencias, humanidades, ingeniería).
- Soporte multilingüe adicional (inglés, portugués, francés).
- Generador de cuestionarios interactivos para presentaciones.

---

## [1.0.0] — 2025-01-15

### Añadido
- Estructura inicial del skill `document-study-material-generator`.
- Archivo `SKILL.md` con frontmatter, flujo de ejecución y reglas esenciales.
- Carpeta `references/` con documentación modular:
  - `configuracion.md`: esquema JSON completo, validación y reglas de combinación.
  - `modo_individual.md`: generación de guías de estudio y podcasts individuales.
  - `modo_consolidado.md`: análisis conjunto de múltiples lecturas.
  - `formatos_salida.md`: Markdown, Word, estructura de ZIP y manifiesto.
  - `control_calidad.md`: verificaciones y manejo de limitaciones.
- Script `scripts/empaquetar_zip.py` para empaquetado reproducible.
- `README.md` con descripción funcional, disparadores, JSON completo y ejemplos.
- Carpeta `examples/` con cuatro casos de uso completos.
- `CONTRIBUTING.md` con convenciones para extender el skill.
- `LICENSE` (MIT).
- `.gitignore` para entornos Python y editores comunes.