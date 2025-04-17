import streamlit as st
import yt_dlp
import os
from pathlib import Path

# Función para descargar el MP3
def descargar_mp3(url, carpeta_destino='descargas'):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': f'{carpeta_destino}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    archivo_mp3 = None

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=True)
            nombre_base = ydl.prepare_filename(info)
            archivo_mp3 = Path(nombre_base).with_suffix('.mp3')
        return archivo_mp3
    except Exception as e:
        print(e)
        return None

# --- Streamlit UI ---

st.set_page_config(page_title="Descarga Nomás", page_icon="🎧")

# Logo + Título
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=130)
with col2:
    st.markdown("<h1 style='margin-top: 20px;'>Descarga Nomás 🎶</h1>", unsafe_allow_html=True)

st.write("Descarga tu música MP3 de manera rápida y sencilla.")
st.write("Pega una o más URLs de YouTube (separadas por comas):")

urls_input = st.text_area("🔗 URLs", height=100)
descargar_btn = st.button("Descargar MP3")

if descargar_btn and urls_input:
    urls = [u.strip() for u in urls_input.split(',') if u.strip()]
    with st.spinner("Descargando MP3..."):
        for url in urls:
            archivo = descargar_mp3(url)
            if archivo and archivo.exists():
                st.success(f"✅ {archivo.name} descargado.")
                with open(archivo, 'rb') as f:
                    st.download_button(
                        label=f"⬇️ Descargar {archivo.name}",
                        data=f,
                        file_name=archivo.name,
                        mime="audio/mpeg"
                    )
            else:
                st.error("❌ Error: no se pudo descargar el archivo.")
