import os
import streamlit as st
import yt_dlp
from pathlib import Path
import ffmpeg
import shutil
import imageio_ffmpeg

# Ruta a ffmpeg portable
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

def descargar_y_convertir_mp3(url, carpeta_destino='descargas'):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Descargar el mejor audio sin convertir
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': f'{carpeta_destino}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=True)
            archivo_origen = ydl.prepare_filename(info)
            archivo_salida = Path(archivo_origen).with_suffix('.mp3')

            # Convertir a MP3 usando ffmpeg-python
            ffmpeg.input(archivo_origen).output(str(archivo_salida), format='mp3', audio_bitrate='192k').run(quiet=True, overwrite_output=True)

            return str(archivo_salida)
    except Exception as e:
        print("Error:", e)
        return None

# --- Streamlit App ---

st.set_page_config(page_title="Descarga Nomás", page_icon="🎧")

col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=120)
with col2:
    st.markdown("<h1 style='margin-top: 20px;'>Descarga Nomás 🎶</h1>", unsafe_allow_html=True)

st.write("Descarga tu música MP3 de manera rápida y sencilla.")
urls_input = st.text_area("🔗 Pega una o más URLs de YouTube (separadas por comas):", height=100)

if st.button("Descargar MP3") and urls_input:
    urls = [u.strip() for u in urls_input.split(',') if u.strip()]
    for url in urls:
        with st.spinner(f"Descargando: {url}"):
            archivo = descargar_y_convertir_mp3(url)
            if archivo and os.path.exists(archivo):
                st.success(f"✅ Descargado: {Path(archivo).name}")
                with open(archivo, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Descargar {Path(archivo).name}",
                        data=f,
                        file_name=Path(archivo).name,
                        mime="audio/mpeg"
                    )
            else:
                st.error("❌ Error al descargar el MP3.")
