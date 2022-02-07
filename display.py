import machine, time, _thread, re, gc

class new:

  refresh_rate = 0.003

  #define GPIO ports
  digits = [2,3,4,5] # Digits: 1, 2, 3, 4
  dot = 6
  segments = [7,8,9,10,11,12,13] # Segments: A,B,C,D,E,F,G

  display_text = []

  # DIGIT map (a,b,c,d,e,f,g): https://en.wikipedia.org/wiki/Seven-segment_display_character_representations
  digit_map = {
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,1,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1),
    'a':(0,0,1,1,0,0,1),
    'b':(0,0,1,1,1,1,1),
    'c':(0,0,1,1,1,0,1),
    'd':(0,1,1,1,1,0,1),
    'e':(0,0,0,1,1,0,0),
    'f':(0,0,0,0,1,1,1),
    'g':(1,0,0,1,1,0,1),
    'h':(0,0,1,0,1,1,1),
    'i':(1,0,0,1,1,0,0),
    'j':(1,0,1,1,0,0,0),
    'k':(1,0,0,1,0,1,1),
    'l':(0,0,0,0,1,1,0),
    'm':(1,0,1,0,1,0,1),
    'n':(0,0,1,0,1,0,1),
    'o':(0,0,1,1,1,0,1),
    'p':(1,1,0,0,1,1,1),
    'q':(1,1,1,0,0,1,1),
    'r':(0,0,0,0,1,0,1),
    's':(0,0,1,1,0,0,0),
    't':(0,0,0,1,1,1,1),
    'u':(0,0,1,1,1,0,0),
    'v':(0,0,1,1,0,0,0),
    'w':(0,1,0,1,0,1,0),
    'x':(0,0,0,1,0,0,1),
    'y':(0,1,1,1,0,1,1),
    'z':(0,0,0,1,0,0,1),
    'A':(1,1,1,0,1,1,1),
    'B':(1,1,1,1,1,1,1),
    'C':(1,0,0,1,1,1,0),
    'D':(1,1,1,1,1,0,0),
    'E':(1,0,0,1,1,1,1),
    'F':(1,0,0,0,1,1,1),
    'G':(1,0,1,1,1,1,0),
    'H':(0,1,1,0,1,1,1),
    'I':(0,0,0,0,1,1,0),
    'J':(0,1,1,1,0,0,0),
    'K':(1,0,1,0,1,1,1),
    'L':(0,0,0,1,1,1,0),
    'M':(1,1,0,1,0,1,0),
    'N':(1,1,1,0,1,1,0),
    'O':(1,1,1,1,1,1,0),
    'P':(1,1,0,0,1,1,1),
    'Q':(1,1,0,1,0,1,1),
    'R':(1,1,0,1,1,1,1),
    'S':(1,0,1,1,0,1,1),
    'T':(1,0,0,0,1,1,0),
    'U':(0,1,1,1,1,1,0),
    'V':(0,1,1,1,0,1,0),
    'W':(1,0,1,1,1,0,0),
    'X':(1,0,0,1,0,0,1),
    'Y':(0,1,0,1,0,1,1),
    'Z':(1,1,0,1,1,0,1),
    '=':(0,0,0,1,0,0,1),
    '-':(0,0,0,0,0,0,1),
    '_':(0,0,0,1,0,0,0),
    '"':(0,1,0,0,0,1,0),
    ' ':(0,0,0,0,0,0,0),
    '\'':(0,0,0,0,0,1,0)
  }

  def __init__(self):
    # Initialize all segments
    for digit in new.digits:
      machine.Pin(digit, machine.Pin.OUT).value(1)
      for segment in new.segments:
        machine.Pin(segment, machine.Pin.OUT).value(1)
      machine.Pin(new.dot, machine.Pin.OUT).value(1)
      new.display_text.append(" ")

    # Start thread
    print("Display thread started..")
    _thread.start_new_thread(self.display, ())

  def exit(self):
    self.write("    ")
    print("Display thread exiting..")
    time.sleep(new.refresh_rate * len(new.digits))
    _thread.exit

  def display(self):
    self.counter = 0
    while True:
      for d in reversed(range(0, len(new.digits))):
        for s in range(len(new.segments)):
          char = new.display_text[d].replace(".", "")
          if len(char) == len(new.display_text[d]):
            machine.Pin(new.dot, machine.Pin.OUT).value(1)
          else:
            machine.Pin(new.dot, machine.Pin.OUT).value(0)
          machine.Pin(new.segments[s], machine.Pin.OUT).value(1 - new.digit_map[char][s])
        machine.Pin(new.digits[d], machine.Pin.OUT).value(1)
        time.sleep(new.refresh_rate)
        machine.Pin(new.digits[d], machine.Pin.OUT).value(0)
      self.counter += 1
      if (self.counter % 100) == 0:
        gc.collect()
        self.counter = 0
    print("Oups, display thread has exited..")
    _thread.exit

  def format(self, text): # splits string to digits to display
    if not re.match(r'^[0-9a-zA-Z \.\-_=\'\"]*$', text):
      print("Unsupported characters")
      return None
    text = list(text)
    for i in range(len(text)):
      if text[i] == ".":
        text[(i-1)] += text[i]
    while "." in text:
      text.remove(".")

    if len(text) > len(new.digits):        
      print("String too long")
      return None
    elif len(text) < len(new.digits):
      for i in range(len(text), len(new.digits)):
        text.insert(0, " ")
    return text

  def write(self, text):
    text = self.format(text)
    if text is not None:
      new.display_text = text
      
if __name__ == "__main__":
  display = new()
  text = "    "
  while True: 
    for digit in sorted(new.digit_map):
      text = text[1:] + digit
      display.write(text)
      print(text)
      print("used: %s" % gc.mem_alloc(), "free: %s" % gc.mem_free())
      time.sleep(0.1)
  display.exit()
  
  
