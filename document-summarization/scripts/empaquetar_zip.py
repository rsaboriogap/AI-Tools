#!/usr/bin/env python3
"""
Empaqueta en un ZIP los materiales de estudio generados.

Uso:
    python empaquetar_zip.py <directorio_resultados> <ruta_salida.zip>

Respeta la estructura de carpetas (individual/, consolidado/, manifest.json)
y usa nombres de archivo relativos al directorio raíz.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path


def empaquetar(directorio_resultados: str, ruta_salida: str) -> None:
    """Comprime recursivamente `directorio_resultados` en `ruta_salida`."""
    base = Path(directorio_resultados)
    if not base.is_dir():
        raise SystemExit(f"Error: el directorio '{base}' no existe o no es válido.")

    salida = Path(ruta_salida)
    salida.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as zf:
        for archivo in sorted(base.rglob("*")):
            if archivo.is_file():
                zf.write(archivo, arcname=archivo.relative_to(base))

    print(f"✔ ZIP creado: {salida} ({salida.stat().st_size} bytes)")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Uso: python empaquetar_zip.py <directorio_resultados> <ruta_salida.zip>")
        return 1
    empaquetar(argv[1], argv[2])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))