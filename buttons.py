from machine import I2C, Pin
import time
from pca9555 import PCA9555

# Initialize I2C and PCA9555
i2c_bus = I2C(1, scl=Pin(6), sda=Pin(7))  # Adjust pin numbers as needed
expander = PCA9555(i2c_bus, address=0x21)

# Configure pins 0-8 as inputs (for buttons)
for pin in range(9):  
    expander.input_pins(pin)

# Define the interrupt callback function
def interrupt_handler(pin):
    # Optional debounce to prevent noise from triggering multiple interrupts
    time.sleep_ms(50)  # Adjust debounce delay as necessary

    # Debug message to confirm interrupt activation
    print("Interrupt detected on GPIO", pin)

    # Poll the expander for the current button states for pins 0-8
    button_states = [expander.read_pin(p) for p in range(9)]
    print("Button States:", button_states)

    # Additional handling logic can be added here based on button states

# Set up the ESP32 interrupt pin on GPIO 5 to trigger the interrupt handler
interrupt_pin = Pin(5, Pin.IN, Pin.PULL_UP)
interrupt_pin.irq(trigger=Pin.IRQ_FALLING, handler=interrupt_handler)

# Main loop (no need to continuously poll)
while True:
    # Optional: Add any non-blocking code here
    time.sleep(0.1)  # Small delay to allow for other processing
