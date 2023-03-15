import time
import board
import terminalio
from displayio import Group
from adafruit_display_text import label

from adafruit_as7341 import AS7341
import adafruit_veml6075
import digitalio

# Silly hack to make it work without stemma qt cable
gnd = digitalio.DigitalInOut(board.D5)
pwr = digitalio.DigitalInOut(board.D6)
gnd.direction = digitalio.Direction.OUTPUT
pwr.direction = digitalio.Direction.OUTPUT
gnd.value = False
pwr.value = True
time.sleep(1)


i2c = board.I2C()  # uses board.SCL and board.SDA
spectral = AS7341(i2c)

print(f'AS7341 integration time is {(spectral.atime + 1) * (spectral.astep + 1) * 2.78}uS')
print(f'AS7341 gain is {spectral.gain}') #default 8

# valid integration times are 50, 100, 200, 400 or 800ms
# uv = adafruit_veml6075.VEML6075(i2c, integration_time=100)
# print(f'VEML6075 integration time is {uv.integration_time}ms') 
time.sleep(3)

display_colors = {
#  '315nm' : 1000,
 '365nm' : 0x610061,
 '415nm' : 0x7600ed,
 '445nm' : 0x0028ff,
 '480nm' : 0x00d5ff,
 '515nm' : 0x1fff00,
 '555nm' : 0xb3ff00,
 '590nm' : 0xffdf00,
 '630nm' : 0xff4f00,
 'clr'   : 0xffffff,
 'NIR  ' : 0xaf0000,
}

while True:
    # channels = {
    # #  '315nm' : uv.uvb,
    # #  '365nm' : uv.uva,
    # '415nm' : spectral.channel_415nm,
    # '445nm' : spectral.channel_445nm,
    # '480nm' : spectral.channel_480nm,
    # '515nm' : spectral.channel_515nm,
    # '555nm' : spectral.channel_555nm,
    # '590nm' : spectral.channel_590nm,
    # '630nm' : spectral.channel_630nm,
    # 'clr' : spectral.channel_clear,
    # 'NIR  ' : spectral.channel_nir,
    # }
    channels = {
    #  '315nm' : 1000,
    '365nm' : 1000,
    '415nm' : 1000,
    '445nm' : 1000,
    '480nm' : 1000,
    '515nm' : 1000,
    '555nm' : 1000,
    '590nm' : 1000,
    '630nm' : 1000,
    'clr'   : 1000,
    'NIR  ' : 1000,
    }
# typical uva responsivity 0.93 counts/μW/cm2
# typical uvb responsivity 2.1 counts/μW/cm2


    main_group = Group()

    row=0
    col=0
    for ch in sorted(channels.keys()):
        l = label.Label(terminalio.FONT, scale=2)
        l.text = f"{ch[:3]}={channels[ch]}"
        l.anchor_point = (0, 0)
        l.color = display_colors[ch]
        # print(f'{col=}')
        l.anchored_position = (col*130, 10+20*row)
        main_group.append(l)
        row +=1
        if (row % 5 == 0):
            col +=1
            row = 0


    board.DISPLAY.show(main_group)

    time.sleep(0.01)
