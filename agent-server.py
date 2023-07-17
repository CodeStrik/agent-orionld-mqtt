from http.server import BaseHTTPRequestHandler, HTTPServer
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

        return 'OK'

def main():
    host = '0.0.0.0'
    port = 8888
    agentserver = HTTPServer((host, port), ProcessRequest)
    print(f"Servidor escuchando en http://{host}:{port}/notify")
    agentserver.serve_forever()

if __name__ == '__main__':
    main()
