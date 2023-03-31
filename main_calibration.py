import time
import board
import terminalio
from displayio import Group
from adafruit_display_text import label

from adafruit_as7341 import AS7341, Gain
import adafruit_veml6075
import digitalio
from adafruit_bitmap_font import bitmap_font
from micropython import const

# Responsivity at gain= GAIN_0_64X and integration_time = 100ms
counts_per_uw2 = 50



i2c = board.I2C()  # uses board.SCL and board.SDA
spectral = AS7341(i2c)

# vaid gains are 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256 and 512 
# spectral.gain = Gain.GAIN_0_5X
spectral.gain = Gain.GAIN_64X
# spectral.gain = Gain.GAIN_32X

gain_lookup = {
     0 : 0.5,
     1 : 1,
     2 : 2,
     3 : 4,
     4 : 8,
     5 : 16,
     6 : 32,
     7 : 64,
     8 : 128,
     9 : 256,
     10 : 512,
}

spectral.atime = 35 #Max
# spectral.atime = 255 #Max
print(f'{spectral.astep=}')

print(f'AS7341 integration time is {(spectral.atime + 1) * (spectral.astep + 1) * 2.78 / 1000}mS')
print(f'AS7341 gain is {spectral.gain}, check this against lookup table') #default 8 = Gain.GAIN_128X


gain = gain_lookup[spectral.gain]
int_time_ms = (spectral.atime + 1) * (spectral.astep + 1) * 2.78 / 1000
print(f'{int_time_ms=}')
responsivity = counts_per_uw2 * (gain/64) * (int_time_ms/100)

print(f'{responsivity=}')


# typical uva responsivity 0.93 counts/μW/cm2
# typical uvb responsivity 2.1 counts/μW/cm2

# valid integration times are 50, 100, 200, 400 or 800ms
uv = adafruit_veml6075.VEML6075(i2c, integration_time=200)
print(f'VEML6075 integration time is {uv.integration_time}ms') 

font = bitmap_font.load_font("VCROSDMono-21.pcf")

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
    channels = {
    #  '315nm' : uv.uvb,
    # '365nm' : uv._read_register(const(0x07)),  #This is the raw uncorrected value.
    '365nm' : uv.uva,
    '415nm' : spectral.channel_415nm,
    '445nm' : spectral.channel_445nm,
    '480nm' : spectral.channel_480nm,
    '515nm' : spectral.channel_515nm,
    '555nm' : spectral.channel_555nm,
    '590nm' : spectral.channel_590nm,
    '630nm' : spectral.channel_630nm,
    'clr' : spectral.channel_clear,
    'NIR  ' : spectral.channel_nir,
    }

    display_group = Group()


    l = label.Label(font, scale=1)
    l.text = f"{'555nm'}={(channels['555nm'])/responsivity} uW/cm2"
    l.anchor_point = (0, 0)
    l.anchored_position = (0, 5+28*0)
    l.color = display_colors['555nm']
    display_group.append(l)

    l2 = label.Label(font, scale=1)
    l2.text = f"{'555nm'}={(channels['555nm'])} counts"
    l2.anchor_point = (0, 0)
    l2.anchored_position = (0, 5+28*1)
    l2.color = display_colors['555nm']
    display_group.append(l2)

    l3 = label.Label(font, scale=1)
    l3.text = f"{'555nm'}={(channels['555nm']/65535*100):05.2f}%"
    l3.anchor_point = (0, 0)
    l3.anchored_position = (0, 5+28*2)
    l3.color = display_colors['555nm']
    display_group.append(l3)   
        
    l3 = label.Label(font, scale=1)
    l3.text = f"Gain = {gain} Int={int_time_ms}"
    l3.anchor_point = (0, 0)
    l3.anchored_position = (0, 5+28*3)
    l3.color = display_colors['555nm']
    display_group.append(l3)   


    # row=0
    # col=0
    # for ch in sorted(channels.keys()):
    #     l = label.Label(font, scale=1)
    #     # l = label.Label(terminalio.FONT, scale=2)
    #     if ch=="365nm":
    #         # l.text = f"{ch[:3]}={channels[ch]}"
    #         l.text=''

    #     if ch =="555nm":
    #         l.text = f"{ch[:3]}={(channels[ch])/responsivity}"[:9]
    #         print(f"{ch[:3]}={(channels[ch])/responsivity} uW/cm2")
    #         print(f"{ch[:3]}={(channels[ch])} counts")
    #         print(f"{ch[:3]}={(channels[ch]/65535*100):05.2f}%")
    #         print('')

    #     else:
    #         l.text=''
    #         # l.text = f"{ch[:3]}={(channels[ch])}"[:9]
    #         # l.text = f"{ch[:3]}={(channels[ch])*responsivity/1000}"[:9]

    #     l.anchor_point = (0, 0)
    #     l.color = display_colors[ch]
    #     # print(f'{col=}')
    #     l.anchored_position = (col*130, 5+28*row)
    #     # l.anchored_position = (col*130, 5+20*row)
    #     display_group.append(l)
    #     row +=1
    #     if (row % 5 == 0):
    #         col +=1
    #         row = 0

    board.DISPLAY.show(display_group)

    time.sleep(0.01)
