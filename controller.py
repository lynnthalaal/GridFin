#!/usr/bin/python

import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

aMotorPins = [12, 15, 11, 13]
bMotorPins = [16, 18, 7, 31]

# Set all pins as output
for pin in aMotorPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

for pin in bMotorPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

aSequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    ]

iNumSteps = len(aSequence)

if sys.argv[3] == 'cw':
    iDirection = 1
else:
    iDirection = -1

fWaitTime = int(sys.argv[1]) / float(1000)
iDeg = int(int(sys.argv[2]) * 11.377777777777)
iSeqPos = 0

# If the fourth argument is present, it means that the motor should start at a
# specific position from the aSequence list

if len(sys.argv) > 4:
    iSeqPos = int(sys.argv[4])

# 1024 steps is 90 degrees
# 4096 steps is 360 degrees

try:
    for step in range(0, iDeg):
        for iPin in range(0, 4):
            
            iRealPin = aMotorPins[iPin]
            iRealPin2 = bMotorPins[iPin]
            chan_list = (iRealPin, iRealPin2)

            if aSequence[iSeqPos][iPin] != 0:
                GPIO.output(chan_list, True)
            else:
                GPIO.output(chan_list, False)

        iSeqPos += iDirection

        if iSeqPos >= iNumSteps:
            iSeqPos = 0

        if iSeqPos < 0:
            iSeqPos = iNumSteps + iDirection

        # Time to wait between steps
        time.sleep(fWaitTime)
        
# trap a CTRL+C keyboard interrupt
except KeyboardInterrupt:
    # resets all GPIO ports used by this program
    GPIO.cleanup()  

GPIO.cleanup()

# Print the position from the aSequence list which should have been the
# next position, if the previous loop was not ended
# Need to catch this output when running from another script

print iSeqPos
