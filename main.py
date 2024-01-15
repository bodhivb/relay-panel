from guizero import App, Box, PushButton
import RPi.GPIO as GPIO

# Define the GPIO pins for shift register connections
DATA_PIN = 17
CLOCK_PIN = 18
LATCH_PIN = 27

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(CLOCK_PIN, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)

# Function to shift data into the shift register
def shift_data(data):
    for bit in range(16):
        GPIO.output(DATA_PIN, (data >> bit) & 1)
        GPIO.output(CLOCK_PIN, GPIO.HIGH)
        GPIO.output(CLOCK_PIN, GPIO.LOW)

    GPIO.output(LATCH_PIN, GPIO.HIGH)
    GPIO.output(LATCH_PIN, GPIO.LOW)

# Function to toggle the relay state
def toggle_relay_state(index):
    rb = relay_buttons[index]
    rb.toggle()
    relay_state = 0b0000000000000000
    for i, button in enumerate(relay_buttons):
        if button.value:
            relay_state |= (1 << i)
    shift_data(relay_state)

# Create the app
app = App("Relay Panel")

# Create a box to hold the relay buttons
relay_box = Box(app, layout="grid")

# Create the relay buttons
relay_buttons = []
for i in range(16):
    relay_button = PushButton(relay_box, text="Relay {}".format(i+1), grid=[i, 0], command=lambda: toggle_relay_state(i))
    relay_buttons.append(relay_button)
    
# Clean up GPIO after the app is closed
def on_close():
    GPIO.cleanup()
    app.destroy()

# Set the app close event handler
app.when_closed = on_close

# Run the app
app.display()
