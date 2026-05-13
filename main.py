import time
from google import genai
from google.genai import types

# 1. Inicializar el cliente
client = genai.Client(api_key="AIzaSyAnR_jEv7YW5vDpVDU9qhULMf2nYaOepIY)

print("Leyendo imagen base localmente...")

# Ruta exacta de tu imagen usando 'r' para evitar problemas con las diagonales invertidas
ruta_imagen = r"C:\Users\zenai\OneDrive\Escritorio\Tec Enero-Mayo 2026\Hackatec 2026 Local+\Generacion de Video\TecladoGenerico.jpg"

# Leemos la imagen en formato binario
with open(ruta_imagen, "rb") as f:
    imagen_bytes = f.read()

# 2. Configurar el objeto Image con los bytes leídos
# IMPORTANTE: Como tu imagen es .png, el mime_type debe ser "image/png"
imagen_obj = types.Image(
    image_bytes=imagen_bytes,
    mime_type="image/jpeg" # <-- Cambiado a jpeg para que coincida con tu foto
)

# 3. Configurar la referencia del video usando el asset en bytes
product_reference = types.VideoGenerationReferenceImage(
    image=imagen_obj, 
    reference_type="asset" 
)

# 4. El Prompt Promocional
prompt = "El objeto de la imagen flota sobre un pedestal de agua cristalina, luces de neón en el fondo, movimiento de cámara circular, 4k, cinematic, comercial de alta calidad, debe de aparecer el precio que es de 200 MXN."

print("Enviando petición a Veo 3.1...")

# 5. Generar el Video
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    config=types.GenerateVideosConfig(
        reference_images=[product_reference], 
        aspect_ratio="16:9", 
    )
)

# 6. Sistema de Polling (Consulta de estado)
while not operation.done:
    print("Generando video... (esto puede tardar unos minutos)")
    time.sleep(10)
    operation = client.operations.get(operation=operation)

print("¡La operación finalizó!")

# 7. Manejo de Errores y Descarga
if operation.error:
    # Si la API falló, imprimimos el motivo exacto
    print("❌ Error: La API rechazó la generación del video.")
    print(f"Motivo: {operation.error.message}")
    
elif not operation.response or not operation.response.generated_videos:
    # Si no hay error explícito pero tampoco hay video
    print("❌ Error: No se generó el video. Es probable que la imagen o el prompt hayan sido bloqueados por los filtros de seguridad de Google.")
    
else:
    # Si todo salió bien, guardamos el video
    print("✅ ¡Video generado exitosamente!")
    video = operation.response.generated_videos[0]
    
    # Descargar el archivo desde los servidores
    client.files.download(file=video.video)
    
    # Guardar en la misma carpeta donde ejecutas el script
    nombre_archivo = "promo_producto_final.mp4"
    video.video.save(nombre_archivo)
    
    print(f"Archivo guardado como: {nombre_archivo}")


    

