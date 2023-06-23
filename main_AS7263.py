import time
import board
from displayio import Group
from adafruit_display_text import label

# from adafruit_as7341 import AS7341, Gain
from adafruit_as726x import AS726x_I2C

from adafruit_bitmap_font import bitmap_font

font = bitmap_font.load_font("VCROSDMono-21.pcf")

i2c = board.I2C()
sensor = AS726x_I2C(i2c)
sensor.driver_led_current = 12.5
sensor.driver_led = False

sensor.conversion_mode = 3 # one shot mode

# The integration time in milliseconds between 2.8 and 714 ms
sensor.integration_time = 166

# Gain options are: 1, 3.7, 16, 64
sensor.gain = 16

# channel mapping for AS7263
channel_map_calibrated = {
     "610" : 0x14,
     "680" : 0x18,
     "730" : 0x1C,
     "760" : 0x20,
     "810" : 0x24,
     "860" : 0x28,
}

channel_map_raw = {
     "610" : 0x08,
     "680" : 0x0A,
     "730" : 0x0C,
     "760" : 0x0E,
     "810" : 0x10,
     "860" : 0x12,
}

channel_values = {
     "610" : 0,
     "680" : 0,
     "730" : 0,
     "760" : 0,
     "810" : 0,
     "860" : 0,
}

while True:

     sensor.start_measurement()
     # Wait for data to be ready
     while not sensor.data_ready:
          time.sleep(0.1)
     
     # reset display
     display_group = Group()
     board.DISPLAY.show(display_group)
     row=0
     col=0

     for ch in sorted(channel_map_calibrated.keys()):
          value = sensor.read_calibrated_value(channel_map_calibrated[ch])
          # print(f'{value=} {sensor.read_channel(channel_map_raw[ch])}')
          channel_values[ch] = value
          # print(f'{ch} = {graph_map(value) * "="} {value}')

          l = label.Label(font, scale=1)

          l.text = f"{ch[:3]}={value}"[:9]

          l.anchor_point = (0, 0)
          l.color = 0xffffff
          l.anchored_position = (col*130, 5+28*row)
          display_group.append(l)
          row +=1
          if (row % 5 == 0):
               col +=1
               row = 0

     # Doing it this way sorts the keys (json.dumps does not)
     output_str = "{"
     for ch in sorted(channel_values.keys()):
          output_str += f'"{ch}": {channel_values[ch]}, ' 
     output_str += "}"

     print(f'{output_str}')  



