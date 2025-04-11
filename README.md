# MicroPython XPT2046 Touch Screen Driver

A MicroPython driver for the **XPT2046 resistive touch controller**, commonly used alongside displays such as the **ILI9341**. This driver allows reading touch positions and supports calibration and screen rotation handling.

## Features

- 🖱️ Touch detection with pressure calculation
- 📐 Coordinate calibration (adjustable min/max ADC values)
- 🔄 Display rotation support (0 to 3)
- 📊 Multi-sample filtering for stable touch input
- ⚡ Optional interrupt pin support for efficient polling

## Usage

### 1. Initialize the driver

```python
from xpt2046 import XPT2046
import machine
import spi

spi = machine.SPI(1, baudrate=10000000, polarity=0, phase=0)
cs = machine.Pin(15, machine.Pin.OUT)
int_pin = machine.Pin(4, machine.Pin.IN)

touch = XPT2046(spi, cs, int_pin=int_pin, rotation=0)
```

### 2. Check for touch and read coordinates
```python
if touch.is_touched():
    x, y = touch.get_touch()
    print("Touch at:", x, y)

```

### 3. Raw touch data (ADC values)
```python
raw = touch.get_raw_touch()
if raw:
    print("Raw:", raw)
```

### Calibration
```python
  touch = XPT2046(
    spi, cs,
    x_min=100, x_max=1962,
    y_min=100, y_max=1900,
    rotation=0
)
#⚠️ The calibrate() method is a placeholder for implementing an on-screen calibration routine.
```

### Constructor Parameters

| Parameter	| Description |
|-----------|-------------|
|spi	|SPI interface instance|
cs	|Chip Select (CS) pin
int_pin|	Optional interrupt pin (pulled low on touch)
width	|Display width in pixels
height	|Display height in pixels
x_min / x_max|	Calibration min/max for X ADC
y_min / y_max	| Calibration min/max for Y ADC
rotation	|Screen rotation (0=0°, 1=90°, 2=180°, 3=270°)

### Credits
Developed by skand7x.

This driver is intended for embedded systems enthusiasts working with MicroPython and SPI TFT displays.
Disclaimer:The content of Readme is taken from Chatgpt and formatted by me.

---

# License
This project is licensed under the GNU General Public License v3.0 (GPLv3).
You are free to use, modify, and distribute this software under the terms of the GPLv3. Any derivative work must also be distributed under the same license.
Copyright (C) 2025 skand7x
---

Let me know if you want to include an example wiring diagram, images, or GIFs for demonstration — or if you want to tailor it for a specific board like ESP32.

