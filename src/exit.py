import sys, device, menu


def open_(device: device.init):
    if menu.yes_no(device, "Exit?"):
        sys.exit()