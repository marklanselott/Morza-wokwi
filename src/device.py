import screen, joistick, time

__version__ = "v1.0.2"

def center_insert(base: str, text: str) -> str:
    width = len(base)
    base = (base + " " * width)[:width]
    base = list(base)
    start = (width - len(text)) // 2
    for i, char in enumerate(text):
        if start + i < width:
            base[start + i] = char
    return ''.join(base)

class init:
    def __init__(self, screen: screen.init, joistick: joistick.init, memory: str):
        self.screen = screen
        self.joistick = joistick
        self.memory = memory

    def __repr__(self):
        return f"<Device memory='{self.memory}'>"

    def version(self):
        lcd = self.screen.lcd
        x, y = self.screen.x, self.screen.y
        center_row = y // 2
        full_block = chr(255) * x
        blank_line = " " * x

        for row in range(y):
            lcd.move_to(0, row)
            lcd.putstr(full_block)
        time.sleep(0.4)

        for row in range(y):
            lcd.move_to(0, row)
            lcd.putstr(blank_line)

        lcd.move_to(0, center_row)
        lcd.putstr(center_insert(blank_line, __version__))
        time.sleep(0.8)

        lcd.move_to(0, center_row)
        lcd.putstr(center_insert(blank_line, "Hello World)"))
        time.sleep(0.8)

        for row in range(y):
            lcd.move_to(0, row)
            lcd.putstr(blank_line)
        lcd.move_to(0, 0)
