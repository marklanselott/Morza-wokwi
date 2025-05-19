import menu, setting, profile, game, exit
from config import device

menus = {
    "Setting": setting,
       "Play": game,
    "Profile": profile,
       "Exit": exit
}

def main():
    while True:
        option = menu.ask(device, list(menus.keys()))
        menus[option].open_(device)

if __name__ == "__main__":
    device.version()
    main()
