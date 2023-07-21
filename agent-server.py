from http.server import BaseHTTPRequestHandler, HTTPServer
import paho.mqtt.client as mqtt
import json

class ProcessRequest(BaseHTTPRequestHandler):
    def do_POST(self):
        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(content_length)
        print(f"Recibido mensaje JSON-LD:\n")
        response = self.handle_notification(content_type, request_data)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode())

    def handle_notification(self, content_type, request_data):
        if content_type == 'application/ld+json':
            notification_data = json.loads(request_data.decode('utf-8'))
            # Formatea la notificación para mostrarla en formato JSON
            formatted_notification = json.dumps(notification_data, indent=4)
            # Imprimir cuerpo de la notificación
            print(formatted_notification)
            
            id_dispositivo = notification_data["data"][0]["id"]     # Guarda el id del dispositivo

            json_data = notification_data["data"]   # almacenamos todos los datos del dispositivo
            atributos_dispositivos = []

            # Almacenar los atributos de cada dispositivo en la lista
            for dispositivo in json_data:
                atributos_dispositivo = {}
                for key, value in dispositivo.items():
                    if key != "id" and key != "type":
                        atributos_dispositivo[key] = value
                atributos_dispositivos.append(atributos_dispositivo)
                
            # Publicación de los datos:
            # Configuración del cliente MQTT
            broker_address = "localhost"  # Cambiar por la dirección de tu broker MQTT
            client = mqtt.Client("Agent")

            # Configuración de usuario y contraseña para la conexión
            username = "admin" 
            password = "strik"  
            client.username_pw_set(username, password)

            # Conexión al broker
            client.connect(broker_address)

            # Publicación de un mensaje
            topic = id_dispositivo 
            message = str(atributos_dispositivo)
            client.publish(topic, message)

            # Desconexión del cliente
            client.disconnect()

        return 'OK'

def main():
    host = '0.0.0.0'
    port = 8888
    agentserver = HTTPServer((host, port), ProcessRequest)
    print(f"Servidor escuchando en http://{host}:{port}/notify")
    agentserver.serve_forever()

if __name__ == '__main__':
    main()
