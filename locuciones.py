import tkinter as tk
from tkinter import filedialog, messagebox
from pydub.utils import which
from pydub import AudioSegment

# Configurar FFmpeg para pydub
AudioSegment.converter = which("ffmpeg")

# Variables globales
introduccion = None
cierres = []
ofertas = []

# Función para depurar archivos cargados
def depurar_audio(archivo, tipo):
    try:
        audio = AudioSegment.from_file(archivo)
        # Normalizar el audio a 44100 Hz y estéreo
        audio = audio.set_frame_rate(44100).set_channels(2)
        print(f"{tipo} cargado correctamente: {archivo}")
        print(f"Duración: {len(audio)} ms, Canales: {audio.channels}, Frame rate: {audio.frame_rate}")
        return audio
    except Exception as e:
        print(f"Error al cargar {tipo}: {archivo} - {e}")
        return None


# Funciones para cargar los archivos
def cargar_introduccion():
    global introduccion
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de Introduccion",
        filetypes=[("Archivos de audio", "*.mp3 *.wav")],
    )
    if archivo:
        introduccion = depurar_audio(archivo, "Introduccion")

def cargar_cierre():
    global cierres
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de Cierre",
        filetypes=[("Archivos de audio", "*.mp3 *.wav")],
    )
    if archivo:
        cierre = depurar_audio(archivo, "Cierre")
        if cierre:
            cierres.append(cierre)

def cargar_oferta():
    global ofertas
    producto_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de Producto",
        filetypes=[("Archivos de audio", "*.mp3 *.wav")],
    )
    precio_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de Precio",
        filetypes=[("Archivos de audio", "*.mp3 *.wav")],
    )
    if producto_archivo and precio_archivo:
        producto = depurar_audio(producto_archivo, "Producto")
        precio = depurar_audio(precio_archivo, "Precio")
        if producto and precio:
            ofertas.append((producto, precio))
            print(f"Oferta {len(ofertas)} cargada: Producto y Precio.")

# Función para generar locución
def generar_locucion():
    try:
        # Declarar variables globales
        global introduccion, ofertas, cierres

        # Crear un fragmento vacío para reemplazar valores None
        audio_vacio = AudioSegment.silent(duration=1000)  # 1 segundo de silencio

        # Reemplazar introduccion con silencio si es None
        if introduccion is None:
            introduccion = audio_vacio

        # Reemplazar productos y precios con silencio si son None
        for i, (producto, precio) in enumerate(ofertas):
            if producto is None:
                ofertas[i] = (audio_vacio, ofertas[i][1])  # Producto vacío
            if precio is None:
                ofertas[i] = (ofertas[i][0], audio_vacio)  # Precio vacío

        # Reemplazar cierres con silencio si son None
        for i, cierre in enumerate(cierres):
            if cierres[i] is None:
                cierres[i] = audio_vacio

        locucion_final = AudioSegment.empty()

        # Procesar introducción
        if introduccion:
            print("Procesando introduccion...")
            locucion_final += introduccion

        # Procesar productos y precios
        for idx, (producto, precio) in enumerate(ofertas):
            if producto:
                print(f"Procesando producto {idx + 1}...")
                locucion_final += producto
            if precio:
                print(f"Procesando precio {idx + 1}...")
                locucion_final += precio

        # Procesar cierres
        if cierres:
            for idx, cierre in enumerate(cierres):
                print(f"Procesando cierre {idx + 1}...")
                locucion_final += cierre

        # Verificar si hay audio válido
        if len(locucion_final) == 0:
            print("Error: No hay audio válido para generar la locución.")
            return

        # Guardar el archivo final
        archivo_salida = filedialog.asksaveasfilename(
            title="Guardar locución final",
            defaultextension=".mp3",
            filetypes=[("Archivos MP3", "*.mp3")],
        )
        if archivo_salida:
            locucion_final.export(archivo_salida, format="mp3")
            print(f"Locución final exportada: {archivo_salida}")
    except Exception as e:
        print(f"Error durante la generación de la locución: {e}")



# Interfaz gráfica
root = tk.Tk()
root.title("Generador de Locuciones")
root.geometry("400x400")

btn_introduccion = tk.Button(root, text="Cargar Introduccion", command=cargar_introduccion)
btn_introduccion.pack(pady=5)

btn_oferta = tk.Button(root, text="Cargar Oferta (Producto + Precio)", command=cargar_oferta)
btn_oferta.pack(pady=5)

btn_cierre = tk.Button(root, text="Cargar Cierre", command=cargar_cierre)
btn_cierre.pack(pady=5)

btn_generar = tk.Button(root, text="Generar Locución", command=generar_locucion)
btn_generar.pack(pady=20)

root.mainloop()
