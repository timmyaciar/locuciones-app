import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

# Lista para almacenar los archivos de audio cargados
archivos = []

def cargar_audio():
    """Cargar un archivo de audio."""
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de audio",
        filetypes=[("Archivos de audio", "*.mp3 *.wav")]
    )
    if archivo:
        archivos.append(archivo)
        messagebox.showinfo("Éxito", f"Archivo {len(archivos)} cargado correctamente.")
        print(f"Archivo {len(archivos)} cargado: {archivo}")

def exportar_audio():
    """Concatenar y exportar los archivos de audio usando FFmpeg."""
    if len(archivos) < 2:
        messagebox.showwarning("Advertencia", "Debes cargar al menos 2 archivos para concatenar.")
        return

    # Crear un archivo temporal con la lista de archivos para concatenar
    archivo_lista = "lista_archivos.txt"
    with open(archivo_lista, "w") as f:
        for archivo in archivos:
            f.write(f"file '{archivo}'\n")

    # Seleccionar el archivo de salida
    archivo_salida = filedialog.asksaveasfilename(
        title="Guardar audio concatenado",
        defaultextension=".mp3",
        filetypes=[("Archivos MP3", "*.mp3")]
    )
    if not archivo_salida:
        return

    # Ejecutar el comando de FFmpeg para concatenar
    try:
        comando = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", archivo_lista,
            "-c", "copy",
            archivo_salida
        ]
        print("Ejecutando comando FFmpeg:", " ".join(comando))
        subprocess.run(comando, check=True)

        messagebox.showinfo("Éxito", f"Archivo exportado correctamente: {archivo_salida}")
        print(f"Archivo exportado correctamente: {archivo_salida}")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"FFmpeg falló al concatenar los archivos: {e}")
        print(f"Error de FFmpeg: {e}")

    finally:
        # Limpiar el archivo temporal
        if os.path.exists(archivo_lista):
            os.remove(archivo_lista)

# Configuración de la interfaz
root = tk.Tk()
root.title("Concatenar y Exportar Audio con FFmpeg")

btn_cargar = tk.Button(root, text="Cargar Audio", command=cargar_audio)
btn_cargar.pack(pady=10)

btn_exportar = tk.Button(root, text="Exportar Audio", command=exportar_audio)
btn_exportar.pack(pady=10)

# Iniciar la aplicación
root.mainloop()
