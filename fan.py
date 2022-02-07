import machine, time

class new:

  #define GPIO ports
  fan_tach = 16
  fan_pwm = 17

  # Configurable temperature (°C)
  temp_min = 32
  temp_max = 38
  temp_delay = 15 # seconds

  # See "Noctua PWM specification white paper": https://noctua.at/media/wysiwyg/Noctua_PWM_specifications_white_paper.pdf
  pwm_freq = 25
  rpm_20 = 450
  rpm_100 = 1500
  pulse = 2

  duty_u16_max = 65535

  temperature_last = 0
  temperature_samples = []
  sample_size = 5
  current_speed = 50 # start speed %
  speed_step = 5
  temp_treshold = (temp_max - temp_min) / (100 / speed_step)

  t = time.time()

  def __init__(self):
    self.tach = machine.Pin(self.fan_tach, machine.Pin.IN, pull=machine.Pin.PULL_UP)
    self.pwm = machine.PWM(machine.Pin(self.fan_pwm))
    self.pwm.freq(self.pwm_freq)
    self.pwm.duty_u16(0)
    self.set_speed(self.current_speed)

  def get_rpm(self):
    pass

  def set_rpm(self, rpm):
    if 0 <= rpm <= self.rpm_100:
      print("Fan speed: %s%%" % round(rpm * (100 / self.rpm_100)), "/ rpm: %s" % rpm)
      self.pwm.duty_u16(round(rpm * (self.duty_u16_max / self.rpm_100)))

  def get_speed(self):
    pass

  def set_speed(self, speed):
    if 0 <= speed <= 100:
      print("Fan speed: %s%%" % speed, "/ rpm: %s" % round(speed * (self.rpm_100 / 100 )))
      self.pwm.duty_u16(round(speed * (self.duty_u16_max / 100)))

  def temperature(self, temperature):
    self.temperature_samples.append(temperature)

    while len(self.temperature_samples) > self.sample_size:
      del self.temperature_samples[0]

    if self.temperature_last == 0:
      self.temperature_last = sum(self.temperature_samples) / len(self.temperature_samples)

    # check time elapsed
    if time.time() - self.t > self.temp_delay:
      self.t = time.time()
    else:
      return

    if temperature <= self.temp_min:
      print("Temperature below the %.1f°C threshold" % self.temp_min)
      if self.current_speed != 0:
        self.current_speed = 0
    elif temperature >= self.temp_max:
      print("Temperature above the %.1f°C threshold" % self.temp_max)
      if self.current_speed != 100:
        self.current_speed = 100
    else:
      if self.temperature_last < temperature - self.temp_treshold:
        print("Temperature whent up (treshold ±%.1f°C): " % self.temp_treshold, "%.1f°C" % self.temperature_last, "=> %.1f°C" % temperature)
        if (self.current_speed + self.speed_step * 1.5 ) <= 100:
          self.current_speed += self.speed_step * 1.5
          self.temperature_last = sum(self.temperature_samples) / len(self.temperature_samples)
      elif self.temperature_last > temperature + self.temp_treshold:
        print("Temperature whent down outside (treshold ±%.1f°C): " % self.temp_treshold, "%.1f°C" % self.temperature_last, "=> %.1f°C" % temperature)
        if (self.current_speed - self.speed_step) >= 0:
          self.current_speed -= self.speed_step
          self.temperature_last = sum(self.temperature_samples) / len(self.temperature_samples)
      else:
        print("Temperature stayed within the treshold (±%.1f°C): " % self.temp_treshold, "%.1f°C" % self.temperature_last, "=> %.1f°C" % temperature)

    self.set_speed(self.current_speed)
    print("=====================")

if __name__ == "__main__":
  fan = new()
  while True:
    for speed in range(0, 110, 10):
      fan.set_speed(speed)
      print("=====================")
      time.sleep(5)
