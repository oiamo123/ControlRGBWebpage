import RPi.GPIO as GPIO
from flask import Flask, request

app = Flask(__name__)

# Define LED pins
GPIO.setmode(GPIO.BCM)
r_pin = 17
g_pin = 27
b_pin = 22

# Set the pins
GPIO.setup(r_pin, GPIO.OUT)
GPIO.setup(g_pin, GPIO.OUT)
GPIO.setup(b_pin, GPIO.OUT)

# Setup PWM for pins
r_pwm = GPIO.PWM(r_pin, 100)
g_pwm = GPIO.PWM(g_pin, 100)
b_pwm = GPIO.PWM(b_pin, 100)

# Start PWM
r_pwm.start(0)
g_pwm.start(0)
b_pwm.start(0)

# Method to configure the rgb pins
def change_light_state(r, g, b):
    r_duty_cycle = (r / 255) * 100
    g_duty_cycle = (g / 255) * 100
    b_duty_cycle = (b / 255) * 100

    r_pwm.ChangeDutyCycle(r_duty_cycle)
    g_pwm.ChangeDutyCycle(g_duty_cycle)
    b_pwm.ChangeDutyCycle(b_duty_cycle)

# HTTP Route
@app.route("/")
def index():
    # Get values
    red = int(request.args.get("red", 0))
    green = int(request.args.get("green", 0))
    blue = int(request.args.get("blue", 0))

    change_light_state(red, green, blue)
    return f"color changed"

@app.route("/shutdown")
def shutdown():
    GPIO.cleanup()
    return "GPIO cleaned up and server shutting down.", 200

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()