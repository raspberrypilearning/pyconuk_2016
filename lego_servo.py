from gpiozero import PWMOutputDevice
from time import sleep

##red wire on 5V
##black wire to ground

C1 = PWMOutputDevice(19, frequency = 1200) ##white wire to pin 19
C2 = PWMOutputDevice(26, frequency = 1200) ##yellow wire to pin 26

C2.off()
C1.off()

positions = {7:1, 6:0.882, 5:0.76, 4: 0.635, 3: 0.501, 2: 0.38, 1:0.258, 0:0}

def turn(position):
    if position < -7 or position > 7:
        return
    if position > 0:
        #turning right
        C2.value = 0
        C1.value = positions[position]
    else:
        #turning left
        position = -position
        C1.value = 0
        C2.value = positions[position]


def test_turns():
    for i in range(-7,8):
        turn(i)
        sleep(0.5)










    
