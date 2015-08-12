import py_rpi

pix = py_rpi.init_array()

boards_in_series = 2
pwm = False

def sim():
    red = 1
    green = 0
    blue = 0
    t = 0

    while True:

        py_rpi.write(pix)

        for i in range(len(pix)):
            for j in range(len(pix[i])):

                pix[i][j][0] = red
                pix[i][j][1] = green
                pix[i][j][2] = blue

        t += 1

        if t%500 == 0:
            if red:
                red = 0
                green = 1
            elif green:
                blue = 1
                green = 0
            else:
                blue = 0
                red = 1


py_rpi.start(sim, boards_in_series, pwm)