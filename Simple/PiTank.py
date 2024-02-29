from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs
import RPi.GPIO as GPIO
import time

# Nastavení režimu pinů
GPIO.setmode(GPIO.BCM)

# Definice pinů pro ovládání motorů
motor1_input1 = 17
motor1_input2 = 22
motor2_input1 = 23
motor2_input2 = 24

# Nastavení pinů jako výstupní
GPIO.setup(motor1_input1, GPIO.OUT)
GPIO.setup(motor1_input2, GPIO.OUT)
GPIO.setup(motor2_input1, GPIO.OUT)
GPIO.setup(motor2_input2, GPIO.OUT)

# Funkce pro pohyb motorů vpřed
def drive_forward():
    GPIO.output(motor1_input1, GPIO.HIGH)
    GPIO.output(motor1_input2, GPIO.LOW)
    GPIO.output(motor2_input1, GPIO.HIGH)
    GPIO.output(motor2_input2, GPIO.LOW)

# Funkce pro pohyb motorů vzad
def drive_backward():
    GPIO.output(motor1_input1, GPIO.LOW)
    GPIO.output(motor1_input2, GPIO.HIGH)
    GPIO.output(motor2_input1, GPIO.LOW)
    GPIO.output(motor2_input2, GPIO.HIGH)

# Funkce pro pohyb motorů dopředu a dozadu
def turn_right():
    GPIO.output(motor1_input1, GPIO.HIGH)
    GPIO.output(motor1_input2, GPIO.LOW)
    GPIO.output(motor2_input1, GPIO.LOW)
    GPIO.output(motor2_input2, GPIO.HIGH)

# Funkce pro pohyb motorů dopředu a dozadu
def turn_left():
    GPIO.output(motor1_input1, GPIO.LOW)
    GPIO.output(motor1_input2, GPIO.HIGH)
    GPIO.output(motor2_input1, GPIO.HIGH)
    GPIO.output(motor2_input2, GPIO.LOW)

# Funkce pro zastavení motorů
def stop_motors():
    GPIO.output(motor1_input1, GPIO.LOW)
    GPIO.output(motor1_input2, GPIO.LOW)
    GPIO.output(motor2_input1, GPIO.LOW)
    GPIO.output(motor2_input2, GPIO.LOW)

class RequestHandler(SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        params = parse_qs(post_data)
        command = params['command'][0]

        if command == 'forward':
            drive_forward()
        elif command == 'backward':
            drive_backward()
        elif command == 'right':
            turn_right()
        elif command == 'left':
            turn_left()
        elif command == 'stop':
            stop_motors()

        self._set_response()
        self.wfile.write("Command received: {}".format(command).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

if __name__ == '__main__':
    run()
