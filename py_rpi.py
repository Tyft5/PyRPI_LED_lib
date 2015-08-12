import RPi.GPIO as GPIO
import board_driver as board
import threading
from stoppable_thread import StoppableThread

from board import PWM, COLS, ROWS
from pins import *

from signal import signal, SIGINT
from time import sleep


__run_thread = None
__sim_thread = None

__pause_event = threading.Event()


def start(user_sim, series=1, pwm=False):

    print "Initializing...",

    signal(SIGINT, __handle_interrupt)

    board.gpio_setup(series, pwm)

    global __run_thread = threading.StoppableThread(st_name="runBoard",
    st_target=board.run_board)
    global __sim_thread = threading.StoppableThread(st_name="simulate",
        st_target=user_sim)

    __run_thread.start()

    print "Done."
    print
    print "Starting simulation. Use ctrl-C to stop."

    __sim_thread.start()

    __pause_event.wait()


def write(array):

    if threading.current_thread().is_stopped():
        threading.current_thread().exit()

    update_thread = threading.Thread(st_name="updateBoard",
        st_target=board.update_board, st_args=(array,))

    while (True):
        if not update.is_alive(): break
        sleep(0.0001)

    update_thread.start()

    return


def init_array():
    array = ( [ [ [ 0 for _ in range(3) ] for _ in range(128) ]
            for _ in range(64) ] )
    return array


def __handle_interrupt(sig_num, frame):

    __run_thread.stop()
    __sim_thread.stop()

    print "Clearing board..."

    board.clear_board()

    __pause_event.set()

    print "Goodbye!"
    return
