#calibrates, then prints the color it senses every second.
#connect Vin to 3.3v, ground to ground
#this code uses GPIO 2 for SDA and GPIO 3 for SCL


#!/usr/bin/env python3
"""
Read RGBC color data from an APDS-9960 on a Raspberry Pi (I2C bus 1).

Setup:
    sudo raspi-config        # Interface Options -> I2C -> Enable
    sudo apt install i2c-tools python3-pip
    pip install smbus2       # (or: sudo apt install python3-smbus2)
    i2cdetect -y 1           # should show 39
"""
import colorsys
import time

from smbus2 import SMBus

ADDR = 0x39            # 7-bit I2C address (datasheet)
BUS = 1                # /dev/i2c-1 on the Pi's header pins 3 (SDA) / 5 (SCL)

# Registers (datasheet register map)
ENABLE = 0x80
ATIME = 0x81
CONTROL = 0x8F
ID = 0x92
STATUS = 0x93
CDATAL = 0x94          # C, R, G, B low/high pairs: 0x94..0x9B

# ENABLE bits
PON = 0x01
AEN = 0x02

# AGAIN field values (CONTROL bits 1:0)
GAIN_1X, GAIN_4X, GAIN_16X, GAIN_64X = 0, 1, 2, 3


class APDS9960:
    def __init__(self, bus_num=BUS, gain=GAIN_4X, atime=0xC0):
        self.bus = SMBus(bus_num)

        dev_id = self.bus.read_byte_data(ADDR, ID)
        if dev_id not in (0xAB, 0xA8):          # 0xAB per datasheet; 0xA8 seen on some parts
            raise RuntimeError(f"Unexpected device ID 0x{dev_id:02X} (expected 0xAB)")

        # Power down while configuring, as the datasheet advises
        self.bus.write_byte_data(ADDR, ENABLE, 0x00)

        # Integration time: cycles = 256 - ATIME, each cycle = 2.78 ms
        # 0xC0 -> 64 cycles -> ~178 ms, max count 65535
        self.bus.write_byte_data(ADDR, ATIME, atime)
        self.integration_ms = (256 - atime) * 2.78

        self.set_gain(gain)

        # Power on, wait for the ~7 ms EXIT SLEEP, then enable the ALS/color engine
        self.bus.write_byte_data(ADDR, ENABLE, PON)
        time.sleep(0.01)
        self.bus.write_byte_data(ADDR, ENABLE, PON | AEN)

    def set_gain(self, gain):
        self.bus.write_byte_data(ADDR, CONTROL, gain & 0x03)

    def read_raw(self):
        """Return (clear, red, green, blue) as 16-bit counts."""
        # Wait for AVALID (STATUS bit 0): a full integration cycle has finished
        deadline = time.time() + 2 * self.integration_ms / 1000 + 0.1
        while not (self.bus.read_byte_data(ADDR, STATUS) & 0x01):
            if time.time() > deadline:
                raise TimeoutError("Timed out waiting for valid color data")
            time.sleep(0.005)

        # One 8-byte block read starting on an even address, low byte first.
        # Reading CDATAL latches all eight bytes at once.
        d = self.bus.read_i2c_block_data(ADDR, CDATAL, 8)
        c = d[0] | (d[1] << 8)
        r = d[2] | (d[3] << 8)
        g = d[4] | (d[5] << 8)
        b = d[6] | (d[7] << 8)
        return c, r, g, b

    white = None   # (r/c, g/c, b/c) measured from a white reference

    def calibrate_white(self, samples=10):
        """Point the sensor at a white/grey card under your light, then call this.
        Cancels the sensor's channel bias and the light source's tint."""
        total = [0, 0, 0, 0]
        for _ in range(samples):
            for i, v in enumerate(self.read_raw()):
                total[i] += v
        c, r, g, b = (t / samples for t in total)
        if c == 0:
            raise RuntimeError("No light detected during calibration")
        self.white = (r / c, g / c, b / c)
        return self.white

    def read_rgb(self):
        """Return ((r, g, b) scaled 0-255, clear count)."""
        c, r, g, b = self.read_raw()
        if c == 0:
            return (0, 0, 0), 0
        ratios = [r / c, g / c, b / c]
        if self.white:
            # Divide by the white reference: white -> (1, 1, 1)
            ratios = [x / w for x, w in zip(ratios, self.white)]
            return tuple(int(255 * min(1.0, x)) for x in ratios), c
        # Uncalibrated fallback: stretch so the strongest channel is 255
        peak = max(ratios) or 1
        return tuple(int(255 * x / peak) for x in ratios), c

    def close(self):
        self.bus.write_byte_data(ADDR, ENABLE, 0x00)
        self.bus.close()


def name_color(rgb):
    """Very rough color naming from hue/saturation/value."""
    h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in rgb))
    if s < 0.25:
        return "white/grey"
    hue = h * 360
    for limit, name in [(20, "red"), (45, "orange"), (70, "yellow"),
                        (165, "green"), (200, "cyan"), (260, "blue"),
                        (300, "purple"), (340, "pink"), (361, "red")]:
        if hue < limit:
            return name


if __name__ == "__main__":
    sensor = APDS9960(gain=GAIN_4X)
    input("Place a white card at your normal sensing distance, then press Enter...")
    print("White reference (r/c, g/c, b/c):", sensor.calibrate_white())
    print("Reading... Ctrl+C to stop.")
    try:
        while True:
            c, r, g, b = sensor.read_raw()
            rgb, _ = sensor.read_rgb()
            note = "  (SATURATED - lower gain)" if c >= 65000 else \
                   "  (very dim - raise gain)" if c < 100 else ""
            print(f"C={c:5d} R={r:5d} G={g:5d} B={b:5d} -> rgb{rgb} "
                  f"{name_color(rgb)}{note}")
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        sensor.close()
