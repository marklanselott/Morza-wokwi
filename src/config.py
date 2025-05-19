import screen, joistick
from device import init

device = init(
  screen.init(0, 1), 
  joistick.init(27, 28, 26), 
  "memory.json"
)


