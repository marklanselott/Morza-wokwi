from machine import ADC, Pin
import time

class sides:
    left = "left"
    right = "right"
    middle = "middle"
    up = "up"
    down = "down"

class init:
    def __init__(self, x: int, y: int, btn: int):
        self.xAxis = ADC(Pin(x))
        self.yAxis = ADC(Pin(y))
        self.button = Pin(btn, Pin.IN, Pin.PULL_UP)

        self.stick = ["middle", "middle"]
        self.btn_status = False

    def __repr__(self):
        return f"<Joystick xPin={self.xAxis.pin()}, yPin={self.yAxis.pin()}, btnPin={self.button.pin()}>"

    def get_data(self):
        while True:
            xValue = self.xAxis.read_u16()
            
            yValue = self.yAxis.read_u16()
            buttonValue = self.button.value()

            # X
            if xValue <= 600:
                self.stick[0] = sides.left
            elif xValue >= 60000:
                self.stick[0] = sides.right
            else:
                self.stick[0] = sides.middle

            # Y
            if yValue <= 600:
                self.stick[1] = sides.up
            elif yValue >= 60000:
                self.stick[1] = sides.down
            else:
                self.stick[1] = sides.middle

            self.btn_status = (buttonValue == 0)
            time.sleep(0.05)
            yield self