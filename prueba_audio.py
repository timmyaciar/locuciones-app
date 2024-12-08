from pydub import AudioSegment

try:
    # Cambia la ruta por la ubicación de tu archivo sin convertir
    audio = AudioSegment.from_file("D:/Vea/Archivo Locuciones/aper.mp3")
    print("Archivo cargado correctamente.")
    print(f"Duración: {len(audio)} ms")
    print(f"Canales: {audio.channels}")
    print(f"Frame rate: {audio.frame_rate}")
except Exception as e:
    print(f"Error al cargar el archivo: {e}")


