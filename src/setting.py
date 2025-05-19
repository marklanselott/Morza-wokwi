import menu, device, json

def set_new_name(device: device.init):
    new_name = menu.input(device, "Write your name:")
    if new_name:
        with open(device.memory, "r", encoding="utf-8") as file:
            data = json.load(file)

        data['profile']['name'] = new_name

        with open(device.memory, "w", encoding="utf-8") as file:
            json.dump(data, file)



def open_(device: device.init):

    params = {
        "edit name": lambda: set_new_name(device)
    }

    while True:
        options = list(params.keys())

        options.append("back")
            
        answer = menu.ask(device, options)
        if answer == "back": 
            break
        else:
            params[answer]()
        



