import time, device
from joistick import sides

morse_dict = {'.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G','....':'H','..':'I','.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N','---':'O','.--.':'P','--.-':'Q','.-.':'R','...':'S','-':'T','..-':'U','...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z','-----':'0','.----':'1','..---':'2','...--':'3','....-':'4','.....':'5','-....':'6','--...':'7','---..':'8','----.':'9'}

def pad(text: str, width: int) -> str:
    return text + " " * (width - len(text))

def ask(device: device.init, options: list[str]):
    options.reverse()
    selected = offset = 0
    visible_lines = device.screen.y
    last_move_time = time.ticks_ms()

    def render_menu():
        visible_options = options[offset:offset+visible_lines]
        for i, option in enumerate(visible_options):
            prefix = ">" if offset + i == selected else " "
            text = f"{prefix} {option}"[:device.screen.x]
            text += " " * (device.screen.x - len(text))
            device.screen.lcd.move_to(0, i)
            device.screen.lcd.putstr(text)

    device.screen.lcd.clear()
    render_menu()

    for data in device.joistick.get_data():
        now = time.ticks_ms()
        moved = False
        if time.ticks_diff(now, last_move_time) > 150:
            if data.stick[1] == sides.up or data.stick[0] == sides.left:
                selected = (selected - 1) % len(options)
                offset = min(offset, selected)
                moved = True
            elif data.stick[1] == sides.down or data.stick[0] == sides.right:
                selected = (selected + 1) % len(options)
                offset = max(offset, selected - visible_lines + 1)
                moved = True

            if moved:
                render_menu()
                last_move_time = now

        if data.btn_status:
            return options[selected]

def input(device: device.init, prompt: str) -> str:
    lcd = device.screen.lcd
    lcd.clear()

    first_line = prompt.split("\n")[0][:device.screen.x]
    lcd.putstr(pad(first_line, device.screen.x))
    lcd.move_to(0, 1)
    lcd.putstr("-" * device.screen.x)

    morse, buffer, press_start = "", "", None
    last_action_time = time.ticks_ms()
    input_timeout_ms = 1500
    cache_line2, cache_line3 = "", ""

    def render():
        nonlocal cache_line2, cache_line3
        full = (morse + buffer)[-2 * device.screen.x:]
        label = "You: "
        text = full[:device.screen.x - len(label)]
        text = pad(text, device.screen.x - len(label))
        line2 = label + text
        if line2 != cache_line2:
            lcd.move_to(0, 2)
            lcd.putstr(line2)
            cache_line2 = line2

        overflow = full[device.screen.x - len(label):]
        overflow = pad(overflow, device.screen.x)
        if overflow != cache_line3:
            lcd.move_to(0, 3)
            lcd.putstr(overflow)
            cache_line3 = overflow

    render()

    for data in device.joistick.get_data():
        now = time.ticks_ms()

        if data.btn_status:
            if press_start is None:
                press_start = now
            last_action_time = now
            continue

        if press_start:
            duration = time.ticks_diff(now, press_start)
            buffer += "." if duration < 500 else "-"
            press_start = None
            last_action_time = now
            render()
            continue

        if data.stick[1] in (sides.right, sides.left):
            if buffer:
                morse += morse_dict.get(buffer, '?')
                buffer = ""
                render()
            if data.stick[1] == sides.left:
                break
            last_action_time = now

        if buffer and time.ticks_diff(now, last_action_time) > input_timeout_ms:
            morse += morse_dict.get(buffer, '?')
            buffer = ""
            last_action_time = now
            render()

        if data.stick[1] == sides.down:
            return None

        if data.stick[0] == sides.right:
            lcd.clear()
            break

    return morse

def yes_no(device: device.init, question: str) -> bool:
    device.screen.lcd.clear()
    device.screen.lcd.putstr(question[:device.screen.x])
    device.screen.lcd.move_to(0, 1)
    device.screen.lcd.putstr("(press hold)")

    press_start = None

    for data in device.joistick.get_data():
        if data.btn_status:
            press_start = press_start or time.ticks_ms()
        elif press_start:
            return time.ticks_diff(time.ticks_ms(), press_start) >= 800


