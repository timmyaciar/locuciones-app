from pydub import AudioSegment

def probar_fragmento(archivo, tipo):
    try:
        audio = AudioSegment.from_file(archivo)
        # Normalización
        audio = audio.set_frame_rate(44100).set_channels(2)
        # Exportar el fragmento para verificar
        audio.export(f"{tipo}_prueba.mp3", format="mp3")
        print(f"{tipo} exportado correctamente.")
    except Exception as e:
        print(f"Error al procesar {tipo}: {e}")

# Archivos de prueba
probar_fragmento("D:/Vea/Archivo Locuciones/aper_convertido.mp3", "introduccion")
probar_fragmento("D:/Vea/Archivo Locuciones/oferta_convertido.mp3", "producto")
probar_fragmento("D:/Vea/Archivo Locuciones/precio_convertido.mp3", "precio")
probar_fragmento("D:/Vea/Archivo Locuciones/aper_convertido.mp3", "cierre")
