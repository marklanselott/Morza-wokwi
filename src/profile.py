import menu, device, json

def open_(device: device.init):
    with open(device.memory, "r", encoding="utf-8") as file:
        data = json.load(file)

    profile = data['profile']
    headers = list(profile.keys())

    while True:
        options = []
        for head in headers:
            options.append(f"{head}: {profile[head]}")

        options.append("back")
        
        answer = menu.ask(device, options)
        if answer == "back": 
            break
