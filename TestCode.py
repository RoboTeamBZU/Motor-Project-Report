import pigpio
import time

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio daemon not running")

# Motor A pins (left motor)
ENA, IN1, IN2 = 18, 23, 24
# Motor B pins (right motor)
ENB, IN3, IN4 = 19, 27, 22   # <-- example GPIOs, change to match your wiring

# Set pins as outputs
for p in (ENA, IN1, IN2, ENB, IN3, IN4):
    pi.set_mode(p, pigpio.OUTPUT)

# Set PWM frequency
pi.set_PWM_frequency(ENA, 2000)
pi.set_PWM_frequency(ENB, 2000)

def run_motor(enable_pin, pin1, pin2, value):
    """Run motor forward or backward.
    Positive value → forward
    Negative value → backward
    Value range: -255 to 255
    """
    forward = value >= 0
    pi.write(pin1, 1 if forward else 0)
    pi.write(pin2, 0 if forward else 1)
    pi.set_PWM_dutycycle(enable_pin, min(255, abs(int(value))))

def stop_motor(enable_pin, pin1, pin2):
    pi.set_PWM_dutycycle(enable_pin, 0)
    pi.write(pin1, 0)
    pi.write(pin2, 0)

try:
    # Motor A test
    print("Motor A forward...")
    run_motor(ENA, IN1, IN2, 100)
    time.sleep(2)
    stop_motor(ENA, IN1, IN2)
    time.sleep(1)

    print("Motor A backward...")
    run_motor(ENA, IN1, IN2, -210)
    time.sleep(2)
    stop_motor(ENA, IN1, IN2)

    # Motor B test
    print("Motor B forward...")
    run_motor(ENB, IN3, IN4, 150)
    time.sleep(2)
    stop_motor(ENB, IN3, IN4)
    time.sleep(1)

    print("Motor B backward...")
    run_motor(ENB, IN3, IN4, -200)
    time.sleep(2)
    stop_motor(ENB, IN3, IN4)

finally:
    stop_motor(ENA, IN1, IN2)
    stop_motor(ENB, IN3, IN4)
    pi.stop()
    print("All motors stopped. Cleanup complete.")
