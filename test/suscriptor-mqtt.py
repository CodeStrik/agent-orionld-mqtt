import paho.mqtt.client as mqtt

# Configuración del cliente MQTT
broker_address = "localhost"  
client = mqtt.Client("suscriptor")  

# Configuración de usuario y contraseña para la conexión
username = "admin"  
password = "strik"  
client.username_pw_set(username, password)

# Definición de una función para procesar los mensajes recibidos
def on_message(client, userdata, message):
    print("Mensaje recibido en el tópico: ", message.topic)
    print("Contenido del mensaje: ", message.payload.decode())

# Configuración de la función de recepción de mensajes
client.on_message = on_message

# Conexión al broker
client.connect(broker_address)

# Suscripción a un tópico específico
topic = "urn:ngsi-ld:PruebaDispositivo:002"
client.subscribe(topic)

# Mantener el cliente a la escucha de mensajes entrantes
client.loop_forever()
