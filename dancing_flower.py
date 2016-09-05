from gpiozero import MCP3008, Servo
from time import time, sleep
import matplotlib.pyplot as plt
from math import sqrt

mic = MCP3008()

def calc_background():
    background = []
    for i in range(5000):
        sleep(1/20000)
        background.append(mic.value)
    return background

def calc_rms(values):
    return sqrt(sum(n*n for n in values)/len(values))

background = sum(calc_background())/5000

def sample_half():
    values = []
    for i in range(2500):
        values.append(mic.value - background)
        sleep(1/20000)
    return calc_rms(values)

# def sample_half():
#     values = []
#     for i in range(2500):
#         values.append(mic.value - background)
#         sleep(1/20000)
#     return values

def gen_graph():
    volumes = []
    times = []
    for i in range(25):
        volumes.append(sample_half())
        times.append(time())
        print(volumes[-1])
        if volumes[-1] > 0.04:
            print('NOISE')
    plt.plot(times,volumes)
    plt.show()
        

s = Servo(17)
s.detach()
def go():
    multiplier = 10
    while True:
        vol = sample_half()
        if vol < 0.01 or vol > 0.1:
            s.detach()
        else:
            s.value = vol * multiplier
            multiplier = -multiplier
            sleep(0.2)
            s.mid()
            

        print(vol)
        
def check():
    volumes = []
    while True:
        vol = sample_half()
        volumes.append(vol)
        print('Volume is {0}'.format(vol))
        print('Max volume is {0}'.format(max(volumes)))
