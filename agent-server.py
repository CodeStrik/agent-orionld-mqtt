from http.server import BaseHTTPRequestHandler, HTTPServer
import paho.mqtt.client as mqtt
import json

class ServerProcessRequest(BaseHTTPRequestHandler):
    
    # Incoming POST requests handler
    def do_POST(self):
        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(content_length)
        print(f"Received JSON-LD message:\n")
        response = self.handle_notification(content_type, request_data)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode())

    # It handles message body formatting and performs the publishing to the MQTT broker
    def handle_notification(self, content_type, request_data):
        if content_type == 'application/ld+json':
            notification_data = json.loads(request_data.decode('utf-8'))
            # It formats the notification to display it in JSON format
            formatted_notification = json.dumps(notification_data, indent=4)
            # Print notification body
            print(formatted_notification)
            
            device_id = notification_data["data"][0]["id"]     # Save the device ID

            json_data = notification_data["data"]   # We store all the device data
            formatted_device_attributes = []

            # Format the attributes of each device and store them in the list
            for device in json_data:
                formatted_attributes = []
                for attribute, value in device.items():
                    if attribute != "id" and attribute != "type":
                        formatted_attributes.append(f"{attribute.capitalize()} = {value['value']}")
                formatted_device_attributes.append(", ".join(formatted_attributes))
            # Data publishing:
            # MQTT client configuration
            broker_address = "localhost"  # Cambiar por la dirección de tu broker MQTT
            client = mqtt.Client("Agent")

            # Username and password configuration for the connection
            username = "admin" 
            password = "strik"  
            client.username_pw_set(username, password)

            # Connecting to the broker
            client.connect(broker_address)

            # Message publishing
            topic = device_id 
            message = str(formatted_device_attributes)
            client.publish(topic, message)

            # Client disconnection
            client.disconnect()

        return 'OK'

def main():
    host = '0.0.0.0'
    port = 8888
    agentserver = HTTPServer((host, port), ServerProcessRequest)
    print(f"Server listening at http://{host}:{port}/notify")
    agentserver.serve_forever()

if __name__ == '__main__':
    main()
