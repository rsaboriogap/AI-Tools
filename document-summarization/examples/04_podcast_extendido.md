# Ejemplo 04 — Podcast extendido de un solo narrador

## Caso de uso

Un estudiante quiere únicamente un **episodio largo tipo monólogo** para escuchar en el coche, de **25 minutos**, sobre una lectura densa. No le interesan las guías escritas ni las preguntas.

## Entrada del usuario

> "Solo quiero un podcast largo, tipo monólogo, de unos 25 minutos, sobre este
> PDF de filosofía. No necesito guía ni preguntas, solo el audio-texto."

## Configuración resultante

```json
{
  "processing": {
    "mode": "individual",
    "analysis_depth": "detailed"
  },
  "output": {
    "format": "md",
    "generate_zip": false,
    "include_manifest": false
  },
  "chapter_analysis": { "enabled": false },
  "conceptual_map":  { "enabled": false },
  "questions":       { "enabled": false },
  "podcast": {
    "enabled": true,
    "style": "narrative",
    "tone": "natural_conversational",
    "target_duration_minutes": 25,
    "speakers": 1,
    "include_introduction": true,
    "include_examples": true,
    "include_reflection": true,
    "include_recap": true,
    "include_closing": true
  }
}
```

## Salida esperada

Un único archivo en el chat (no ZIP, porque `generate_zip = false`):

```markdown
# Podcast — [Título del documento]

**Documento de origen:** filosofia_lectura.pdf
**Duración estimada:** 25 minutos (~3 000–3 750 palabras)
**Participantes:** Narrador

---

**Narrador:** Hoy vamos a explorar una de las reflexiones más profundas
de este texto. Empecemos por entender el contexto del autor...
```

## Extensión orientativa

| Duración | Palabras |
|---|---|
| 20 min | 2 400 – 3 000 |
| **25 min** | **3 000 – 3 750** |
| 30 min | 3 600 – 4 500 |

## Notas de ejecución

- `speakers: 1` → narrador único, exposición educativa conversacional.
- `generate_zip: false` y `include_manifest: false` → solo el guion.
- Secciones 1, 2, 3 y 5 omitidas por configuración (`enabled: false`).
- No se generan carpetas `individual/` ni `consolidado/` ni `manifest.json`.