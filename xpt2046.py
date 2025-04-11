"""
MicroPython XPT2046 Touch Screen Driver
"""

import time
from micropython import const
import machine

# XPT2046 Command constants
_GET_X = const(0b10010000)  # X position
_GET_Y = const(0b11010000)  # Y position
_GET_Z1 = const(0b10110000)  # Z1 position
_GET_Z2 = const(0b11000000)  # Z2 position
_GET_TEMP0 = const(0b10000000)  # Temperature 0
_GET_TEMP1 = const(0b11110000)  # Temperature 1
_GET_BATTERY = const(0b10100000)  # Battery monitor
_GET_AUX = const(0b11100000)  # Auxiliary input

class XPT2046:
    """
    A driver for the XPT2046 touch controller, commonly used with ILI9341
    """
    
    def __init__(self, spi, cs, int_pin=None, width=240, height=320, 
                 x_min=100, x_max=1962, y_min=100, y_max=1900, rotation=0):
        """
        Initialize the touch screen driver.
        
        Args:
            spi: SPI bus instance
            cs: Chip select pin
            int_pin: Interrupt pin (optional)
            width: Display width (default: 240)
            height: Display height (default: 320)
            x_min: Minimum x ADC value (calibration)
            x_max: Maximum x ADC value (calibration)
            y_min: Minimum y ADC value (calibration)
            y_max: Maximum y ADC value (calibration)
            rotation: Screen rotation (0-3, should match display rotation)
        """
        self.spi = spi
        self.cs = cs
        self.int_pin = int_pin
        
        self.width = width
        self.height = height
        
        # Calibration values
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        
        # Set rotation
        self.rotation = rotation
        
        # If interrupt pin is provided, configure it
        if int_pin:
            self.int_pin.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
            
        # Settle time after touch
        self.touch_delay = 10  # ms
        # Number of samples to take for more accurate reading
        self.samples = 3
            
    def _command(self, cmd):
        """Send a command and read response from touch controller
        
        Args:
            cmd: Command byte to send
            
        Returns:
            12-bit response value
        """
        self.cs.value(0)
        
        # Send command byte
        self.spi.write(bytes([cmd]))
        
        # Read 12-bit response (stored in 2 bytes)
        data = self.spi.read(2)
        
        self.cs.value(1)
        
        # Combine the two bytes into a 12-bit value (first 12 bits of 16)
        return ((data[0] << 8) | data[1]) >> 3
        
    def is_touched(self):
        """Check if the screen is being touched
        
        Returns:
            True if screen is being touched, False otherwise
        """
        # If interrupt pin is provided, use it to detect touch
        if self.int_pin:
            # Int pin is pulled low when touched
            return not self.int_pin.value()
        
        # Otherwise, try to measure touch pressure
        # Get Z1 and Z2 values
        z1 = self._command(_GET_Z1)
        z2 = self._command(_GET_Z2)
        
        # Calculate pressure
        if z2 == 0:
            return False
            
        # Pressure formula: z = z1/z2 - 1
        pressure = z1 / z2 - 1
        
        # Return True if significant pressure detected
        return pressure > 0.1
        
    def get_raw_touch(self):
        """Get raw touch coordinates (ADC values)
        
        Returns:
            tuple (x, y) of raw touch position or None if not touched
        """
        if not self.is_touched():
            return None
            
        # Take multiple samples and average them
        x_samples = []
        y_samples = []
        
        for _ in range(self.samples):
            x_samples.append(self._command(_GET_X))
            y_samples.append(self._command(_GET_Y))
            time.sleep_ms(self.touch_delay)
            
        # Sort and take the middle value to remove outliers
        x_samples.sort()
        y_samples.sort()
        
        if self.samples >= 3:
            # Use median if we have at least 3 samples
            x = x_samples[self.samples // 2]
            y = y_samples[self.samples // 2]
        else:
            # Otherwise use average
            x = sum(x_samples) // len(x_samples)
            y = sum(y_samples) // len(y_samples)
            
        return x, y
        
    def get_touch(self):
        """Get calibrated touch position in display coordinates
        
        Returns:
            tuple (x, y) of calibrated touch position or None if not touched
        """
        raw = self.get_raw_touch()
        if raw is None:
            return None
            
        x_raw, y_raw = raw
        
        # Map raw ADC values to screen coordinates
        x = self.width - int((x_raw - self.x_min) * self.width / (self.x_max - self.x_min))
        y = int((y_raw - self.y_min) * self.height / (self.y_max - self.y_min))
        
        # Apply rotation
        if self.rotation == 0:
            return x, y
        elif self.rotation == 1:
            return y, self.width - x
        elif self.rotation == 2:
            return self.width - x, self.height - y
        elif self.rotation == 3:
            return self.height - y, x
            
    def calibrate(self):
        """Interactive calibration routine
        
        Prompts user to touch three points and calculates calibration values.
        Requires a connected display to show instructions.
        """
        # This would typically require user interaction and display output
        # For simplicity, not fully implemented here
        pass 