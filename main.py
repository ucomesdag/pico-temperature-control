import machine, time, gc
import temperature
import fan
import display

temperature = temperature.new()
fan = fan.new()
display = display.new()

while True:
  temperature_celsius = temperature.get()
  fan.temperature(temperature_celsius)
  # fan.set_speed(60)
  # print("used: %s" % gc.mem_alloc(), "free: %s" % gc.mem_free())
  display.write("{:.1f}C".format(temperature_celsius))
  time.sleep(5)
display.exit()
