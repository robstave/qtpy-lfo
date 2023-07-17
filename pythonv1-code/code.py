# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython LFO."""
import time
import board
import busio
import random
import neopixel
import adafruit_mcp4728
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn


analog_in = AnalogIn(board.A0)
freq_in = AnalogIn(board.A1)

# pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel = neopixel.NeoPixel(board.A3, 1)

pixel.brightness = 0.1

last_time_read = time.monotonic_ns()
last_time_write = time.monotonic_ns()

write_len = 800000
read_len = 50000000

# gate output pin
# gate = DigitalInOut(board.A2)
# gate.direction = Direction.OUTPUT

 
#  i2c setup
# i2c = board.I2C()  
i2c = busio.I2C(board.SCL, board.SDA)
# uses board.SCL and board.SDA
 

#  dac setup over i2c
dac = adafruit_mcp4728.MCP4728(i2c, 0x64)
# gate.value = True
#  dac raw value (12 bit)
# dac.raw_value = 4095

accumulator1 = 0
accumulator2 = 0
accumulator3 = 0
accumulator4 = 0

tuneword4 = 1000
tuneword3 = 1000
tuneword2 = 9000
tuneword1 = 8000

waveform = 2

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
    
def mapRange(x, in_min, in_max, out_min, out_max):
    """Map an input x from range (in_min, in_max) to range (out_min, out_max).  This
    is a Python implementation of the Arduino map() function.  Works on either
    integers or floating point.
    """
    divisor = in_max - in_min
    
    if divisor == 0:
        return out_min
    else:
        return ((x - in_min) * (out_max - out_min) / divisor) + out_min
        
while True:
    
    now = time.monotonic_ns()
    
    if (now - last_time_read) > read_len:
        
        f = freq_in.value
        rootFreq = mapRange(freq_in.value, 0, 65535, 50, 9200)
        tuneword1 = int(rootFreq)
        tuneword2 = int(rootFreq * 0.88)
        tuneword3 = int(rootFreq * 0.62)
        tuneword4 = int(rootFreq * 0.45)
        
        v = analog_in.value
        x = mapRange(analog_in.value, 0, 65535, 1, 8)
        
        waveform = int(x)

        if (waveform == 1):
            pixel.fill(0x420000)
            pixel.brightness = 0.1
            pixel.show()
        
        if waveform == 2:
            pixel.fill(0x004200)
            pixel.show()
            
        if waveform == 3:
            pixel.fill(0x000042)
            pixel.show()

        if waveform == 4:
            pixel.fill(0x420042)
            pixel.show()
            
        if waveform == 5:
            pixel.fill(0x424200)
            pixel.show()
            
        if waveform == 6:
            pixel.fill(0x004242)
            pixel.show()
            
        if waveform == 7:
            pixel.fill(0x424242)
            pixel.show()

        last_time_read = now

    if (now - last_time_write) > write_len:
        
        accumulator1 = accumulator1 + tuneword1
        accumulator2 = accumulator2 + tuneword2
        accumulator3 = accumulator3 + tuneword3
        accumulator4 = accumulator4 + tuneword4

        mask = 0xfffff
        
        val1 = ((accumulator1 & mask) >> 8) 
        val2 = ((accumulator2 & mask) >> 8) 
        val3 = ((accumulator3 & mask) >> 8) 
        val4 = ((accumulator4 & mask) >> 8) 


# ramp
        if waveform == 1:        
            dac.channel_a.raw_value = val1 
            dac.channel_b.raw_value = val2 
            dac.channel_c.raw_value = val3 
            dac.channel_d.raw_value = val4 

# ramp down
        if waveform == 2:
            dac.channel_a.raw_value = 4095 - val1  
            dac.channel_b.raw_value = 4095 - val2
            dac.channel_c.raw_value = 4095 - val3 
            dac.channel_d.raw_value = 4095 - val4 
       
# triangle
        if waveform == 3:
            
            if val1 > 2048:
                val1 = 4095 - val1
                
            dac.channel_a.raw_value = (val1 << 1 & 0xfff) 
            
            if val2 > 2048:
                val2 = 4095 - val2
                
            dac.channel_b.raw_value = (val2 << 1 & 0xfff) 
        
            if val3 > 2048:
                val3 = 4095 - val3
                
            dac.channel_c.raw_value = (val3 << 1 & 0xfff) 
       
            if val4 > 2048:
                val4 = 4095 - val4
                
            dac.channel_d.raw_value = (val4 << 1 & 0xfff)       
         
# square
        if waveform == 4:
            
            if val1 < 2048:
                dac.channel_a.raw_value = 0
            else:
                dac.channel_a.raw_value = 4095
                
            if val2 < 2048:
                dac.channel_b.raw_value = 0
            else:
                dac.channel_b.raw_value = 4095
                
            if val3 < 2048:
                dac.channel_c.raw_value = 0
            else:
                dac.channel_c.raw_value = 4095
                
            if val4 < 2048:
                dac.channel_d.raw_value = 0
            else:
                dac.channel_d.raw_value = 4095
        
#  90 deg ramps        
        if waveform == 5:
           
            dac.channel_a.raw_value = ((val1) & 0xfff) 
            dac.channel_b.raw_value = ((val1 - 1024) & 0xfff)
            dac.channel_c.raw_value = ((val1 - 2048) & 0xfff)
            dac.channel_d.raw_value = ((val1 - 3072) & 0xfff) 
            
        if waveform == 6:

            if val1 > 2048:
                val1 = 4095 - val1
                
            if val2 > 2048:
                val2 = 4095 - val2

            if val3 > 2048:
                val3 = 4095 - val3
                
            if val4 > 2048:
                val4 = 4095 - val4 
            
            
            dac.channel_a.raw_value = ((val1  + val2) & 0xfff)

            dac.channel_b.raw_value = ((val2  + max(0, val3 - (val4 >> 2))) & 0xfff)
            dac.channel_c.raw_value = ((val3  + max(0, val4 - (val1 >> 2))) & 0xfff)
            dac.channel_d.raw_value = ((val1  + val4) & 0xfff)

        if waveform == 7:
            dac.channel_a.raw_value = (((val1  + val2)) >> 1 & 0xfff)

            dac.channel_b.raw_value = (((val2  + 4095 - val4)) >> 1 & 0xfff)
            dac.channel_c.raw_value = (((val3  + val1)) >> 1 & 0xfff)
            dac.channel_d.raw_value = (((val4  + 4095 - val3)) >> 1 & 0xfff)			
 
        last_time_write = now
        
  