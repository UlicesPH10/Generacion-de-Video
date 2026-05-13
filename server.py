from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from google import genai
from google.genai import types
import time
import os

app = FastAPI()

client = genai.Client(api_key="AIzaSyAnR_jEv7YW5vDpVDU9qhULMf2nYaOepIY")

# Endpoint 1: Recibe imagen y prompt, devuelve JSON con URL
# Endpoint 1: Recibe imagen, prompt y duración
@app.post("/generar-video/")
async def generar_video(
    imagen: UploadFile = File(...), 
    prompt_usuario: str = Form(...),
    duracion: int = Form(5) # <--- Agregamos esto (5 segundos por defecto)
):
    try:
        imagen_bytes = await imagen.read()
        mime_type = imagen.content_type 
        
        if mime_type not in ["image/jpeg", "image/png"]:
            return {"error": "Formato no soportado. Usa JPG o PNG."}

        imagen_obj = types.Image(
            image_bytes=imagen_bytes,
            mime_type=mime_type 
        )

        product_reference = types.VideoGenerationReferenceImage(
            image=imagen_obj, 
            reference_type="asset" 
        )

        print(f"Petición recibida. Prompt del usuario: {prompt_usuario}")
        
        # Le enviamos el prompt del usuario a Veo
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt_usuario,
            config=types.GenerateVideosConfig(
                reference_images=[product_reference], 
                aspect_ratio="16:9", 
            )
        )

        while not operation.done:
            time.sleep(10)
            operation = client.operations.get(operation=operation)

        if operation.error:
            return {"status": "error", "mensaje": operation.error.message}
        if not operation.response or not operation.response.generated_videos:
            return {"status": "error", "mensaje": "Filtro de seguridad o error."}

        video = operation.response.generated_videos[0]
        client.files.download(file=video.video)
        
        nombre_archivo = f"promo_{int(time.time())}.mp4"
        video.video.save(nombre_archivo)

        # Retornamos un JSON estructurado con la ruta para descargar el video
        return {
            "status": "success", 
            "mensaje": "¡Video generado correctamente!",
            "url_descarga": f"/descargar/{nombre_archivo}"
        }

    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


# Endpoint 2: Sirve el archivo .mp4 cuando la app lo pide
@app.get("/descargar/{nombre_video}")
async def descargar_video(nombre_video: str):
    # Verifica que el archivo exista en el servidor antes de enviarlo
    if os.path.exists(nombre_video):
        return FileResponse(path=nombre_video, media_type="video/mp4", filename=nombre_video)
    return {"error": "Video no encontrado"}