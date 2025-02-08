import time
import smbus2
import RPi.GPIO as GPIO
import threading

# Default I2C bus and AS1170 address
I2C_BUS = 3  # Default Raspberry Pi I2C bus
I2C_ADDR = 0x30  # Default AS1170 I2C address

# AS1170 Registers
REG_STROBE_SIGNAL = 0x07
REG_FLASH_TIMER = 0x05
REG_CURRENT_LED1 = 0x01
REG_CURRENT_LED2 = 0x02
REG_CONTROL = 0x06

# STROBE pin configuration
STROBE_PIN = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(STROBE_PIN, GPIO.OUT, initial=GPIO.LOW)

# Initialize I2C bus
bus = smbus2.SMBus(I2C_BUS)

def set_i2c_bus(bus_id):
    """Sets the I2C bus dynamically."""
    global I2C_BUS, bus
    I2C_BUS = bus_id
    bus.close()  # Close the old bus before reassigning
    bus = smbus2.SMBus(I2C_BUS)
    print(f"I2C bus set to {I2C_BUS}")

def set_id(new_id):
    """Sets the AS1170 I2C address dynamically."""
    global I2C_ADDR
    I2C_ADDR = new_id
    print(f"AS1170 I2C address set to {hex(I2C_ADDR)}")

def write_register(register, value):
    """Writes a value to an AS1170 register."""
    bus.write_byte_data(I2C_ADDR, register, value)
    time.sleep(0.01)  # Small delay for stability

def convert_mA_to_register(current_mA):
    """Converts current in mA (0-450) to register value (0x00-0x7F)."""
    return max(0, min(0x7F, int((current_mA / 450) * 0x7F)))

class LEDController:
    """Class to control both LEDs connected to AS1170."""
    def __init__(self):
        self.led1 = convert_mA_to_register(450)  # Default current for LED1 (~450mA)
        self.led2 = convert_mA_to_register(450)  # Default current for LED2 (~450mA)
        self.strobe_active = False
        self.strobe_thread = None

    def set_intensity(self, led1=None, led2=None):
        """Sets intensity for LED1 and/or LED2 separately using mA values."""
        if led1 is not None:
            self.led1 = convert_mA_to_register(led1)
            write_register(REG_CURRENT_LED1, self.led1)
        if led2 is not None:
            self.led2 = convert_mA_to_register(led2)
            write_register(REG_CURRENT_LED2, self.led2)
        print(f"LED1 intensity: {led1}mA, LED2 intensity: {led2}mA")

    def on(self):
        """Turns on both LEDs with their current intensity."""
        self.strobe_active = False
        write_register(REG_CURRENT_LED1, self.led1)
        write_register(REG_CURRENT_LED2, self.led2)
        write_register(REG_CONTROL, 0x1B)  # Enable flash mode
        GPIO.output(STROBE_PIN, GPIO.HIGH)
        print("Both LEDs ON")

    def off(self):
        """Turns off both LEDs and stops any active strobe mode."""
        self.strobe_active = False
        write_register(REG_CONTROL, 0x00)  # Disable LEDs
        GPIO.output(STROBE_PIN, GPIO.LOW)
        print("Both LEDs OFF")

    def _strobe_loop(self, frequency):
        """Internal method for strobe effect."""
        period = 1.0 / frequency
        print("Strobe mode activated")
        while self.strobe_active:
            write_register(REG_CURRENT_LED1, self.led1)
            write_register(REG_CURRENT_LED2, self.led2)
            write_register(REG_CONTROL, 0x1B)  # Enable flash mode
            GPIO.output(STROBE_PIN, GPIO.HIGH)
            time.sleep(period / 2)
            write_register(REG_CONTROL, 0x00)  # Disable LEDs
            GPIO.output(STROBE_PIN, GPIO.LOW)
            time.sleep(period / 2)
        print("Strobe mode stopped")

    def strobe(self, frequency=10):
        """Flashes both LEDs on and off at a given frequency until manually stopped."""
        if self.strobe_active:
            print("Strobe is already running")
            return
        self.strobe_active = True
        self.strobe_thread = threading.Thread(target=self._strobe_loop, args=(frequency,), daemon=True)
        self.strobe_thread.start()

# Create LED controller object
led = LEDController()

# If used as a standalone script, run a basic test
if __name__ == "__main__":
    try:
        set_id(0x30)  # Example: Set I2C address
        set_i2c_bus(3)  # Example: Set I2C bus
        
        led.set_intensity(led1=300, led2=200)  # Example intensity settings in mA
        led.strobe(frequency=5)  # Strobe effect at 5 Hz until manually stopped
        time.sleep(10)  # Let it strobe for 10 seconds
        led.off()
    except KeyboardInterrupt:
        led.off()
        print("Exiting program...")
    finally:
        GPIO.cleanup()
        bus.close()
