# PyRPi_LED_Lib

This is a python library for interfacing with and drawing to an LED matrix using a Raspberry Pi. The project used chained Adafruit 64x32 boards.

The library uses the RPi.GPIO library included with Raspbian to interface with the GPIO pins on the Pi. All other modules used are standard modules.

To use the library, simply create a .py file in the same directory as the library files. Your file should:
  - Import py_rpi for necessary functions
  - Use the init_array() function to easily create a 3D array (nested lists) (optional, but the array is necessary)
  - Define a function that runs your code, be it drawing a picture or running a simulation
  - In your function, pass your array to the write() function in py_rpi to write to the LED board
  - After your function has been defined, invoke the start() function in py_rpi to set the thing in motion

A couple sample simulation files have been included. They can be explored if the above is not clear and run to test the hardware setup.

****NOTE: The library uses the broadcom pin number scheme by default. This can be changed in board_driver.py if desired. If pin numbers need to be changed, they are defined in pins.py.
  
Documentation for py_rpi is below.
  
## Documentation

  
__py_rpi.init_array(row, col)__

Returns a 3D array with `row` rows, `col` columns, and 3 layers (red, green, and blue in that order).
  
_Parameters_
- row: the number of rows (first "dimension") desired for the array
- col: the number of columns (second "dimension") desired for the array
  
Implementation: init_array() creates a list of lists of lists, which can be accessed in python simply by chaining brackets  
  
  
__py_rpi.write(array)__

Writes the image implicit to `array` to the LED board.
The values stored in the array should be either True or False, or 1 or 0. Other values than 1 can be used, but they are interpreted logically i.e. x!=0 -> x=True. PWM is not implemented yet.
Each (x, y) coordinate represents an RGB LED on the board.
The layers 0, 1, and 2 indicate whether or not the red, green, and blue LED's should be lit up, respectively.
  
_Parameters_
- array: an array containing a pattern to be written to the board. The dimensions of the array should represent the dimensions of the conglomerate LED board as it appears (e.g. 4 boards in a 2x2 arrangement is 64x128).  
  
  
__py_rpi.start(function, series=1, pwm=False)__

Starts the process of running the user program and writing to the board. Should be invoked after the user function is defined.
  
_Parameters_
- function: the name of the function that invokes write(), sans parentheses (e.g. `my_func`). Any patter written to the board will be maintained until another is written; it is not necessary to continuously write a static image.
- series: the number of boards that are connected in series (chained)
- pwm: a boolean (or 1 or 0) indicating whether or not pulse width modulation should be used. Currently not implemented  
  
  

TO DO:
- PWM
- support for boards connected in parallel
- board writing optimization (not writing pixels that haven't changed)
- support for boards connected in series and arranged vertically
- package library for installation for improved file management and organization
- build-in support for non-broadcom pin numbering
