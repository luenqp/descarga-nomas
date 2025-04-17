import os
import streamlit as st
import yt_dlp
from pathlib import Path
import imageio_ffmpeg

# Obtener la ruta del ejecutable de ffmpeg portable
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
print("ffmpeg_path: ", ffmpeg_path)

def descargar_mp3(url, carpeta_destino='descargas'):
    if not os.path.exists(carpeta_destino):
        print(f"Creando carpeta {carpeta_destino}")
        os.makedirs(carpeta_destino)

    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': f'{carpeta_destino}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path,  # Esta es la forma correcta
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=True)
            archivo = ydl.prepare_filename(info)
            mp3_file = Path(archivo).with_suffix(".mp3")
            return str(mp3_file)
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

if st.button("Convertir a MP3") and urls_input:
    urls = [u.strip() for u in urls_input.split(',') if u.strip()]
    for url in urls:
        with st.spinner(f"Convertiendo: {url}"):
            archivo = descargar_mp3(url)
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

