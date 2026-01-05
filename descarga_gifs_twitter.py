import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import uuid

def procesar_twitter(url_tweet, opcion):
    # --- Configuración de carpetas ---
    carpeta_raiz = "twitter_extract"
    subcarpetas = {
        "1": "videos",
        "2": "gifs",
        "3": "imagenes"
    }
    
    # Crear carpeta principal y subcarpeta específica
    ruta_destino = os.path.join(carpeta_raiz, subcarpetas[opcion])
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
        print(f"Carpeta '{ruta_destino}' preparada.")

    id_unico = str(uuid.uuid4())[:8]
    
    # Definición de rutas
    ruta_temp = os.path.join(ruta_destino, f"temp_{id_unico}.mp4")
    ruta_final_mp4 = os.path.join(ruta_destino, f"video_{id_unico}.mp4")
    ruta_final_gif = os.path.join(ruta_destino, f"animacion_{id_unico}.gif")
    ruta_final_img = os.path.join(ruta_destino, f"captura_{id_unico}.jpg")

    try:
        # 1. Descarga del vídeo (Base igual)
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': ruta_temp,
            'quiet': True,
        }

        print(f"Descargando contenido de X...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_tweet])

        # 2. Procesamiento según elección del menú
        if opcion == "1": # MP4
            os.rename(ruta_temp, ruta_final_mp4)
            print(f"✅ ¡Éxito! Vídeo guardado en: {ruta_final_mp4}")
        
        elif opcion == "2": # GIF
            print("Convirtiendo a GIF (esto puede tardar)...")
            with VideoFileClip(ruta_temp) as clip:
                clip.write_gif(ruta_final_gif, fps=12, logger=None)
            print(f"✅ ¡Éxito! GIF guardado en: {ruta_final_gif}")
            
        elif opcion == "3": # IMAGEN
            print("Extrayendo fotograma...")
            with VideoFileClip(ruta_temp) as clip:
                clip.save_frame(ruta_final_img, t=0)
            print(f"✅ ¡Éxito! Imagen guardada en: {ruta_final_img}")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        # 3. Limpieza del temporal si existe
        if os.path.exists(ruta_temp):
            try:
                os.remove(ruta_temp)
                print("🧹 Archivo temporal eliminado.")
            except PermissionError:
                pass

if __name__ == "__main__":
    print("        --- TWITTER EXTRACTOR ---")
    print("Selecciona qué quieres obtener del tweet:")
    print("1. Vídeo (MP4)")
    print("2. Animación (GIF)")
    print("3. Imagen fija (JPG)")
    
    seleccion = input("\nElige una opción (1, 2 o 3): ")
    
    if seleccion in ["1", "2", "3"]:
        link = input("Pega el enlace del tweet: ")
        procesar_twitter(link, seleccion)
    else:
        print("Opción no válida. Reinicia el script.")