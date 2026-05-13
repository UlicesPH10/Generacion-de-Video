import requests

# 1. URL limpia y correcta usando tu IP de Google Cloud
url = "http://34.46.15.98/generar-video/" 

ruta_imagen = "TecladoGenerico.jpg" 
prompt = "Un fondo de luces de neón vibrantes para este producto."

print("Conectando con el servidor en la nube...")

# Como vamos directo a la IP, ya no necesitamos los trucos de ngrok
with open(ruta_imagen, "rb") as f:
    
    # 2. Actualizamos el tipo de archivo a "image/jpeg"
    archivos = {"imagen": (ruta_imagen, f, "image/jpeg")}
    
    datos = {
        "prompt_usuario": prompt,
        "duracion": 5  
    }

    # Hacemos la petición POST limpia
    respuesta = requests.post(url, files=archivos, data=datos)

print("\nRespuesta del servidor:")
print(respuesta.json())