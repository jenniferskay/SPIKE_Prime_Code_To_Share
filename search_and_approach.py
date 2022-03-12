from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

print ("Hello I'm here!")

class State():
    LEFT = 1
    RIGHT = 2
    APPR = 3
    FOUND = 4
    ERROR = 5



# Python doesn't have built in constants, but we're going to agree to never
# change the following variables.
CONST_MIN_YAW = -45
CONST_MAX_YAW = 45
CONST_MAX_SPIKE_CM_DIST = 200
CONST_DECTECTION_MAX_DIST_CM = 60
CONST_WAIT_TIME = 0.1
CONST_HUB = PrimeHub()
CONST_MOTOR_PAIR = MotorPair("C", "D")
CONST_ULTRASONIC = DistanceSensor("A")
CONST_POW = 10


# -------------------- searchAndApproach ----------------------------
# Assumes that the current position should be equal to the initialYaw
def searchAndApproach():
    CONST_HUB.light_matrix.show_image('HAPPY')
    CONST_HUB.speaker.beep()

    state = State.LEFT
    done = False
    CONST_HUB.motion_sensor.reset_yaw_angle()  #make sure we start with yaw of 0

    while not(done):
        if (state == State.LEFT):
            state = doLeft()
        elif (state == State.RIGHT):
            state = doRight()
        elif (state == State.APPR):
            state = doAppr()
        elif (state == State.FOUND):
            state = doFound()
            done = True
        else:  # ERROR!!!
            state = State.ERROR
            done = True

    if state != State.ERROR:
        print("Success!!")
        #CONST_HUB.light_matrix.write("Success")
    else:
        print("searchAndApproach finished with error")
        CONST_HUB.light_matrix.show_image('NO')
        CONST_HUB.speaker.beep(note=55, seconds = 1.5)
        print ("all done")
        



# ------------------ doLeft -----------------------
# Start motors turning left and then wait for detection or yaw to be <= CONST_MIN_YAW
# Note - if CONST_MIN_YAW is too close to -180 we'll never exit!!

def doLeft():
    print("starting doLeft!")
    CONST_HUB.light_matrix.show_image("GO_LEFT")  #Draw Left Arrow

    CONST_MOTOR_PAIR.start(steering=-100, speed=CONST_POW) # Start Turning Left

    # Wait until you have a "detection event" or a "max left yaw event"
    # Note that this function is non-deterministic, if the two events happen simultaneously 
    # which one will fire depends exclusively on where you are in the loop!
    while(True):
        CONST_MOTOR_PAIR.start(steering=-100, speed=CONST_POW)
        wait_for_seconds(CONST_WAIT_TIME)
        myDistance = CONST_ULTRASONIC.get_distance_cm() 
        if myDistance == None: # Spike returns None if it can't detect the reflection, I'm changing that to max
            myDistance = CONST_MAX_SPIKE_CM_DIST 

        if myDistance < CONST_DECTECTION_MAX_DIST_CM: 
            CONST_MOTOR_PAIR.stop() 
            print ("\ngot ultra result:", str(myDistance))
            return State.APPR

        myYaw = CONST_HUB.motion_sensor.get_yaw_angle() 
        print("got yaw result: ", str(myYaw))
        if (myYaw < CONST_MIN_YAW):
            CONST_MOTOR_PAIR.stop() 
            return State.RIGHT
        
       
            


# A few stubs so you can run this ...

# -------------------- 

def doRight():
    CONST_MOTOR_PAIR.stop()
    print("starting doRight")
    CONST_HUB.light_matrix.show_image("GO_RIGHT")
    wait_for_seconds(1)  # Just so you can see the go right symbol
    print("Just because I'm a stub I'm going to return State.Error")
    return State.ERROR 

def doAppr():
    print("starting doAppr!")
    CONST_HUB.light_matrix.show_image("GO_UP")  
    wait_for_seconds(1) # Just so you can see the go up symbol
    print("Just because I'm a stub I'm going to return State.Error")
    return State.ERROR

def doFound():
    print("starting doFound!")
    CONST_HUB.light_matrix.show_image("HEART_SMALL")
    CONST_MOTOR_PAIR.stop()
    wait_for_seconds(1)
    print("Just because I'm a stub I'm going to return State.Error")
    return State.ERROR

def main():
    searchAndApproach()



main()

