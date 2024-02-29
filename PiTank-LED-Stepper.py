from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs
import RPi.GPIO as GPIO
import time
import neopixel
import board

# Nastavení režimu pinů
GPIO.setmode(GPIO.BCM)

# Definice pinů pro ovládání motorů
motor1_input1 = 17
motor1_input2 = 22
motor2_input1 = 23
motor2_input2 = 24

# Definice pinů pro krokový motor
step_motor = 2
GPIO.setup(step_motor, GPIO.OUT)
pwm = GPIO.PWM(step_motor, 50)
pwm.start(0)
current_angle = 0

# LED
LED_PIN = board.D18
LED_COUNT = 8
strip=neopixel.NeoPixel(LED_PIN, LED_COUNT)

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

# LED ON
def turn_on_led():
    strip.fill((255, 255, 255))

# LED OFF
def turn_off_led():
    strip.fill((0, 0, 0))

# Krokový motor definice
def SetAngle(angle):
    if angle < 0:
        angle = 0
    elif angle > 60:
        angle = 60

    duty = angle / 18 + 2
    GPIO.output(2, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(2, False)
    pwm.ChangeDutyCycle(0)
    current_angle = angle

def RotateUp():
    global current_angle
    new_angle = current_angle + 15
    if new_angle > 60:
        new_angle = 60
    SetAngle(new_angle)
    current_angle = new_angle

def RotateDown():
    global current_angle
    new_angle = current_angle - 15
    if new_angle < 0:
        new_angle = 0
    SetAngle(new_angle)
    current_angle = new_angle

SetAngle(0)

class RequestHandler(SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/home/pi/index.html'
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
        elif command == 'lights_on':
            turn_on_led()
        elif command == 'lights_off':
            turn_off_led()
        elif command == 'up':
            RotateUp()
        elif command == 'down':
            RotateDown()

        self._set_response()
        self.wfile.write("Command received: {}".format(command).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

if __name__ == '__main__':
    run()
