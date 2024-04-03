import os
import time
import board
import smbus2
import RPi.GPIO as GPIO
import busio
import Adafruit_SSD1306
from PIL import ImageFont, ImageDraw, Image
import cv2

# Function to detect cars in an image and count them
def detect_cars(image):
    # Load pre-trained Haar cascade for car detection
    #car_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + '/home/user/Downloads/cars.xml')

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect cars in the image
    cars = car_cascade.detectMultiScale(gray, 1.1, 3)

    # Return the count of cars detected
    return len(cars)

# Initialize OLED display
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=0x3C)
disp.begin()
disp.clear()
disp.display()
bus = smbus2.SMBus(1)
# Initialize servo motor
GPIO.setmode(GPIO.BCM)
servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz PWM frequency
pwm.start(0)

# Path to the directory where images are loaded
image_directory = '/home/user/Pictures'

# Load font for OLED display
font = ImageFont.load_default()

# Function to display message on OLED
def display_message(message):
    disp.clear()
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), message, font=font, fill=255)
    disp.image(image)
    disp.display()

# Function to control servo motor
def control_servo(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)
print("code running")
# Load the Haar cascade file for car detection
car_cascade = cv2.CascadeClassifier('/home/user/Downloads/cars.xml')

# Check if the cascade classifier was loaded successfully
if car_cascade.empty():
    print("Error: Unable to load the cascade classifier.")
else:
    print("Cascade classifier loaded successfully.")
while True:
    # List all files in the image directory
    files = os.listdir(image_directory)

    for file in files:
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith("jpeg"):
            # Read the image
            image = cv2.imread(os.path.join(image_directory, file))

            # Perform car detection and count cars
            car_count = detect_cars(image)

            # Display message based on car count
            if car_count > 5:
                display_message(f"{car_count}cars barricade down, More than 5 cars")
                print("more than 5 cars, barricade down")
                #print(car_count)
                # Move the servo motor to 90 degrees
                control_servo(90)
            elif car_count == 0:
                display_message("No cars")
            else:
                display_message(f"{car_count} cars, barricade up")
                print("barricade up")

            # Remove the processed image
            #os.remove(os.path.join(image_directory, file))

            # Wait for a while before checking for the next image
            time.sleep(2)

# Clean up GPIO and PWM on program exit
GPIO.cleanup()
pwm.stop()