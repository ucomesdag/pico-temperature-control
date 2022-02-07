import onewire, ds18x20, machine, time

class new:
  #define GPIO ports
  temp_sensor = 26

  def __init__(self):
    self.temperature_sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(self.temp_sensor)))
    self.roms = self.temperature_sensor.scan()
    self.temperature_sensor.convert_temp()
    time.sleep_ms(750)

  def get(self):
    self.temperature_sensor.convert_temp()
    temperature = 0
    for rom in self.roms:
      temperature += self.temperature_sensor.read_temp(rom)
    temperature = temperature / len(self.roms)
    return temperature

if __name__ == "__main__":
  temperature = new()

  while True:
    print("Temperature: %.1f°C" % temperature.get())
    print("=====================")
    time.sleep(5)
