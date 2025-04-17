import streamlit as st
import yt_dlp
import os
import imageio_ffmpeg

# Configurar ruta de ffmpeg para yt_dlp
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

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

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        return "✅ MP3 descargado con éxito."
    except Exception as e:
        print(e)
        return "❌ Error: escribe correctamente la(s) url(s)."

# --- Streamlit App ---

st.set_page_config(page_title="Descarga Nomás", page_icon="🎧")

# Crear dos columnas: una para el logo y otra para el título
col1, col2 = st.columns([1, 4])  # Puedes ajustar la proporción si deseas

with col1:
    st.image("logo.png", width=150)  # Ajusta el tamaño según lo que necesites

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
            resultado = descargar_mp3(url)
            st.success(resultado)
