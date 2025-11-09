import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips
from moviepy.video.fx import fadein, fadeout
import os
from PIL import Image

st.title("Editor de Video Automático")
st.write("Sube fotos y una canción para crear un video editado automáticamente.")

# Subida de archivos
uploaded_images = st.file_uploader("Sube fotos (JPG/PNG)", accept_multiple_files=True, type=["jpg", "png"])
uploaded_audio = st.file_uploader("Sube la canción (MP3/WAV)", type=["mp3", "wav"])

if st.button("Generar Video") and uploaded_images and uploaded_audio:
    # Guardar archivos temporalmente
    image_paths = []
    for img in uploaded_images:
        img_path = f"temp_{img.name}"
        with open(img_path, "wb") as f:
            f.write(img.getbuffer())
        image_paths.append(img_path)
    
    audio_path = f"temp_{uploaded_audio.name}"
    with open(audio_path, "wb") as f:
        f.write(uploaded_audio.getbuffer())
    
    # Cargar audio y calcular duración
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    num_images = len(image_paths)
    clip_duration = audio_duration / num_images  # Tiempo por imagen
    
    # Crear clips de imagen con transiciones
    clips = []
    for i, img_path in enumerate(image_paths):
        img_clip = ImageClip(img_path).set_duration(clip_duration).resize(height=720)
        if i > 0:
            img_clip = fadein(img_clip, 1)  # Fade in de 1 segundo
        if i < num_images - 1:
            img_clip = fadeout(img_clip, 1)  # Fade out de 1 segundo
        clips.append(img_clip)
    
    # Concatenar clips y añadir audio
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)
    
    # Exportar video
    output_path = "video_editado.mp4"
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    
    # Mostrar resultado y descargar
    st.success("Video generado exitosamente!")
    st.video(output_path)
    with open(output_path, "rb") as f:
        st.download_button("Descargar Video", f, file_name="video_editado.mp4")
    
    # Limpiar archivos temporales
    for path in image_paths + [audio_path, output_path]:
        if os.path.exists(path):
            os.remove(path)