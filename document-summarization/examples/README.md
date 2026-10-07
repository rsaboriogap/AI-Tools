# Ejemplos de uso

Esta carpeta contiene casos completos que muestran cómo invocar el skill con distintas configuraciones y qué salida esperar.

| Archivo | Escenario | Modo | Profundidad | Formato | PPT |
|---|---|---|---|---|---|
| `01_individual_basico.md` | 1 documento, guía + podcast breve | `individual` | `basic` | `md` | No |
| `02_consolidado_docx.md` | 3 papers, resumen + podcast conjunto | `consolidated` | `detailed` | `docx` | No |
| `03_both_exhaustivo.md` | 2 capítulos, material completo | `both` | `exhaustive` | `md` | No |
| `04_podcast_extendido.md` | Solo podcast, 1 narrador, 25 min | `individual` | `detailed` | `md` | No |
| `05_presentacion_educativa.md` | 1 documento, material + presentación | `individual` | `detailed` | `md` + `pptx` | Sí |

Cada ejemplo incluye:

1. **Caso de uso** — contexto del usuario.
2. **Entrada del usuario** — texto literal de la petición.
3. **Configuración resultante** — JSON fusionado con los valores por defecto.
4. **Estructura del ZIP generado** — árbol de carpetas y archivos.
5. **Contenido esperado** — fragmento o esquema de los archivos.
6. **Notas de ejecución** — decisiones tomadas por el skill.

Consulta estos ejemplos para:

- Aprender qué combinaciones de opciones son válidas.
- Verificar la salida esperada antes de ejecutar.
- Copiar configuraciones como plantilla para tus propias peticiones.