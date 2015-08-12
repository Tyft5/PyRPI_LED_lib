import RPi.GPIO as GPIO
import threading
from stoppable_thread import StoppableThread

from GPIO import HIGH, LOW, OUT
from pins import *

from time import sleep

PWM = False
COLS = 0
ROWS = 0

__row_order = [0, 1, 2, 3, 8, 9, 10, 11, 4, 5, 6, 7, 12, 13, 14, 15]
__board_lock = threading.RLock()


# Sets up pins as either binary or pwm
def gpio_setup(series=1, pwm=False):

    global COLS = series * 64
    global ROWS = 32
    global PWM = pwm

    GPIO.setmode(GPIO.BCM)

    if PWM:
        softPwmCreate(R1, 0, 100)
        softPwmCreate(R2, 0, 100)
        softPwmCreate(G1, 0, 100)
        softPwmCreate(G2, 0, 100)
        softPwmCreate(B1, 0, 100)
        softPwmCreate(B2, 0, 100)
    else:
        GPIO.setup(R1, OUT)
        GPIO.setup(R2, OUT)
        GPIO.setup(G1, OUT)
        GPIO.setup(G2, OUT)
        GPIO.setup(B1, OUT)
        GPIO.setup(B2, OUT)

    GPIO.setup(A, OUT)
    GPIO.setup(B, OUT)
    GPIO.setup(C, OUT)
    GPIO.setup(D, OUT)
    GPIO.setup(LATCH, OUT)
    GPIO.setup(CLOCK, OUT)
    GPIO.setup(OE, OUT)

    if GPIO.input(A):      GPIO.output(A, LOW)
    if GPIO.input(B):      GPIO.output(B, LOW)
    if GPIO.input(C):      GPIO.output(C, LOW)
    if GPIO.input(D):      GPIO.output(D, LOW)
    if GPIO.input(CLOCK):  GPIO.output(CLOCK, LOW)
    if GPIO.input(LATCH):  GPIO.output(LATCH, LOW)

    GPIO.output(OE, HIGH)

    return


# Writes a new image to the board
def update_board(pixelArray):

    with __board_lock:

        clear_board()
        reset_rows()
        
        for i in __row_order:
            for j in range(COLS):

                r1Val = pixelArray[i][j][0]
                r2Val = pixelArray[i + 16][j][0]
                g1Val = pixelArray[i][j][1]
                g2Val = pixelArray[i + 16][j][1]
                b1Val = pixelArray[i][j][2]
                b2Val = pixelArray[i + 16][j][2]

                GPIO.output(CLOCK, HIGH)
     
                if PWM:     softPwmWrite(R1, r1Val) 
                elif r1Val: GPIO.output(R1, HIGH) 
                else:       GPIO.output(R1, LOW) 

                if PWM:     softPwmWrite(R2, r2Val) 
                elif r2Val: GPIO.output(R2, HIGH) 
                else:       GPIO.output(R2, LOW) 


                if PWM:     softPwmWrite(R1, g1Val) 
                elif g1Val: GPIO.output(R1, HIGH) 
                else:       GPIO.output(R1, LOW) 

                if PWM:     softPwmWrite(R2, g2Val) 
                elif g2Val: GPIO.output(R2, HIGH) 
                else:       GPIO.output(R2, LOW) 


                if PWM:     softPwmWrite(R1, b1Val) 
                elif b1Val: GPIO.output(R1, HIGH) 
                else:       GPIO.output(R1, LOW) 

                if PWM:     softPwmWrite(R2, b2Val) 
                elif b2Val: GPIO.output(R2, HIGH) 
                else:       GPIO.output(R2, LOW) 


                GPIO.output(CLOCK, LOW)

            GPIO.output(LATCH, HIGH)
            GPIO.output(LATCH, LOW)

            sleep(0.00001)

            next_row()

    return


# Continually scans the board to display the currently written image
def run_board():
    while true:
        
        with __board_lock:
            next_row()

        sleep(0.0001)

        if threading.current_thread().is_stopped(): return
    return


# Returns the row address to the beginning
def reset_rows():
    GPIO.output(A, LOW)
    GPIO.output(B, LOW)
    GPIO.output(C, LOW)
    GPIO.output(D, LOW)
    return


# Iterates the row address
def next_row():
    if GPIO.input(A)==0: 
        GPIO.output(A, HIGH)
    elif GPIO.input(B)==0: 
        GPIO.output(B, HIGH)
        GPIO.output(A, LOW)
    elif GPIO.input(C)==0: 
        GPIO.output(C, HIGH)
        GPIO.output(B, LOW)
        GPIO.output(A, LOW)
    elif (GPIO.input(D)==0: 
        GPIO.output(D, HIGH)
        GPIO.output(C, LOW)
        GPIO.output(B, LOW)
        GPIO.output(A, LOW)
    else:
        GPIO.output(D, LOW)
        GPIO.output(C, LOW)
        GPIO.output(B, LOW)
        GPIO.output(A, LOW)
    return


# Turns all LEDs off
def clear_board():
    reset_rows()

    for i in range(200):
        for j in range(COLS):

            GPIO.output(CLOCK, HIGH)

            if PWM:
                softPwmWrite(R1, 0)
                softPwmWrite(R2, 0)
                softPwmWrite(G1, 0)
                softPwmWrite(G2, 0)
                softPwmWrite(B1, 0)
                softPwmWrite(B2, 0)
            else:
                GPIO.output(R1, LOW)
                GPIO.output(R2, LOW)
                GPIO.output(G1, LOW)
                GPIO.output(G2, LOW)
                GPIO.output(B1, LOW)
                GPIO.output(B2, LOW)
            
            GPIO.output(CLOCK, LOW)
        
        GPIO.output(LATCH, HIGH)
        GPIO.output(LATCH, LOW)

        sleep(0.000001)

        next_row()

    return
