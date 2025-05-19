from pico_i2c_lcd import I2cLcd
from machine import I2C, Pin



class init:
    def __init__(self, sda: int, scl: int, x: int = 20, y: int = 4):
        self.i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
        self.I2C_ADDR = self.i2c.scan()[0]
        self.lcd = I2cLcd(self.i2c, self.I2C_ADDR, y, x)
        self.y = y
        self.x = x

    def __repr__(self):
        return f"<LCD init x={self.x}, y={self.y}, addr=0x{self.I2C_ADDR:X}>"