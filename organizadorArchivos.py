#!/usr/bin/env python3
"Organizador de archivos: mueve cada archivo de una carpeta a subcarpetas por tipo."

import os
import shutil
import sys

# Relación extensión -> carpeta de destino
CATEGORIAS = {
    "Imagenes": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic", ".tiff"},
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".xls", ".xlsx", ".csv", ".ppt", ".pptx"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Comprimidos": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Programas": {".exe", ".msi", ".dmg", ".pkg", ".deb", ".apk"},
    "Codigo": {".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".json", ".sql"},
}
CARPETA_OTROS = "Otros"


def obtener_categoria(nombre_archivo):
    """Devuelve el nombre de la carpeta que le corresponde al archivo."""
    extension = os.path.splitext(nombre_archivo)[1].lower()
    for carpeta, extensiones in CATEGORIAS.items():
        if extension in extensiones:
            return carpeta
    return CARPETA_OTROS


def ruta_sin_conflicto(ruta_destino):
    """Si el archivo ya existe, agrega ' (1)', ' (2)', ... al nombre."""
    if not os.path.exists(ruta_destino):
        return ruta_destino
    base, extension = os.path.splitext(ruta_destino)
    contador = 1
    while os.path.exists(f"{base} ({contador}){extension}"):
        contador += 1
    return f"{base} ({contador}){extension}"


def organizar(carpeta):
    "Mueve los archivos y devuelve (movidos_por_categoria, errores)."
    movidos = {}
    errores = []
    script_actual = os.path.abspath(__file__)

    for nombre in os.listdir(carpeta):
        ruta_origen = os.path.join(carpeta, nombre)

        # Ignorar subcarpetas, archivos ocultos y este mismo script
        if not os.path.isfile(ruta_origen):
            continue
        if nombre.startswith("."):
            continue
        if os.path.abspath(ruta_origen) == script_actual:
            continue

        categoria = obtener_categoria(nombre)
        carpeta_destino = os.path.join(carpeta, categoria)

        try:
            os.makedirs(carpeta_destino, exist_ok=True)
            ruta_destino = ruta_sin_conflicto(os.path.join(carpeta_destino, nombre))
            shutil.move(ruta_origen, ruta_destino)
            movidos[categoria] = movidos.get(categoria, 0) + 1
        except (PermissionError, OSError) as error:
            errores.append((nombre, str(error)))

    return movidos, errores


def main():
    ruta = input("Ruta de la carpeta a organizar: ").strip().strip('"').strip("'")
    carpeta = os.path.abspath(os.path.expanduser(ruta))

    if not os.path.isdir(carpeta):
        print(f"Error: '{carpeta}' no es una carpeta válida.")
        sys.exit(1)

    confirmar = input(f"Se organizarán los archivos de:\n  {carpeta}\n¿Continuar? (s/n): ")
    if confirmar.strip().lower() not in ("s", "si", "sí"):
        print("Operación cancelada.")
        return

    movidos, errores = organizar(carpeta)
    total = sum(movidos.values())

    print("\n--- Resumen ---")
    if total == 0:
        print("No había archivos para mover.")
    else:
        print(f"Se movieron {total} archivo{'s' if total != 1 else ''}:")
        for categoria, cantidad in sorted(movidos.items()):
            print(f"  {categoria}: {cantidad}")

    if errores:
        print(f"\nNo se pudieron mover {len(errores)} archivo(s):")
        for nombre, motivo in errores:
            print(f"  {nombre} -> {motivo}")


if __name__ == "__main__":
    main()