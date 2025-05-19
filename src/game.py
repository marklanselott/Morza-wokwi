import menu, device, json, random, time

def save_game(device: device.init, score: str, **kwargs):
    with open(device.memory, "r", encoding="utf-8") as file:
        data = json.load(file)

    history = data['game']['history']
    history.append(score)
    data['game']['history'] = history

    with open(device.memory, "w", encoding="utf-8") as file:
        json.dump(data, file)

class levels:
    easy = "easy"
    normal = "normal"
    hard = "hard"

def game(device: device.init):
    while True:
        lvl = menu.ask(device, [levels.easy, levels.normal, levels.hard, "back"])
        if lvl == "back":
            break
        else:
            points = 0
            reverse_morse_dict = {v: k for k, v in menu.morse_dict.items()}

            while True:
                if lvl == levels.easy:
                    morse = random.choice(list(menu.morse_dict.keys()))
                    base = menu.morse_dict[morse]

                    answer = menu.input(device, f"{points} | {base}: {morse}")
                    if answer:
                        if answer.replace(" ", "") == base:
                            points += 1
                        else:
                            points -= 1
                    else:
                        save_game(device, f"{time.localtime()[3]:02}:{time.localtime()[4]:02} | {points} | {lvl}")
                        break
                elif lvl in [levels.normal, levels.hard]:
                    with open(device.memory, "r", encoding="utf-8") as file:
                        data = json.load(file)

                    word = random.choice(data["game"]["words"]).upper()
                    letters = list(word)
                    user_input = ""

                    for i, letter in enumerate(letters):
                        morse = reverse_morse_dict.get(letter, "?")
                        prompt = f"{points} | {word} | {letter} {morse}" if lvl == levels.normal else f"{points} | {'?'*(i+1)} | {letter} {morse}"
                        answer = menu.input(device, prompt)
                        if answer is None:
                            save_game(device, f"{time.localtime()[3]:02}:{time.localtime()[4]:02} | {points} | {lvl}")
                            return
                        user_input += answer.upper()

                    if user_input == word:
                        points += 1
                    else:
                        points -= 1

def history(device: device.init):
    with open(device.memory, "r", encoding="utf-8") as file:
        data = json.load(file)

    options = data['game']['history']
    options.append("back")

    while True:
        answer = menu.ask(device, options)
        if answer == "back":
            break

def open_(device: device.init):
    params = {
        "game": lambda: game(device),
        "history": lambda: history(device)
    }
 
    while True:
        options = list(params.keys())

        options.append("back")
            
        answer = menu.ask(device, options)
        if answer == "back": 
            break
        else:
            params[answer]()

      

