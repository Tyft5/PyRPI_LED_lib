import py_rpi

grid = py_rpi.init_array()
next = grid

boards_in_series = 2
pwm = False

def game_of_life():

    while True:

        py_rpi.write(grid)

        for i in range(len(grid)):
            for j in range(len(grid[i])):

                cell = grid[i][j][0]

                if 0 <= i < len(grid)-1 and 0 <= j < len(grid[i])-1:

                    neighbors = [ grid[i+1][j][0],
                                  grid[i][j+1][0],
                                  grid[i-1][j][0],
                                  grid[i][j-1][0],
                                  grid[i+1][j+1][0],
                                  grid[i+1][j-1][0],
                                  grid[i-1][j+1][0],
                                  grid[i-1][j-1][0] ]

                elif j == len(grid[i])-1 and i == len(grid)-1:

                    neighbors = [ grid[0][j][0],
                                  grid[i][0][0],
                                  grid[i-1][j][0],
                                  grid[i][j-1][0],
                                  grid[0][0][0],
                                  grid[0][j-1][0],
                                  grid[i-1][0][0],
                                  grid[i-1][j-1][0] ]

                elif j == len(grid[i])-1:

                    neighbors = [ grid[i+1][j][0],
                                  grid[i][0][0],
                                  grid[i-1][j][0],
                                  grid[i][j-1][0],
                                  grid[i+1][0][0],
                                  grid[i+1][j-1][0],
                                  grid[i-1][0][0],
                                  grid[i-1][j-1][0] ]

                else:

                    neighbors = [ grid[0][j][0],
                                  grid[i][j+1][0],
                                  grid[i-1][j][0],
                                  grid[i][j-1][0],
                                  grid[0][j+1][0],
                                  grid[0][j-1][0],
                                  grid[i-1][j+1][0],
                                  grid[i-1][j-1][0] ]

                adjSum = sum(neighbors)

                if adjSum < 2 and cell:
                    next[i][j][0] = 0
                elif adjSum > 3 and cell:
                    next[i][j][0] = 0
                elif adjSum == 3 and not cell:
                    next[i][j][0] = 1

        grid = next


py_rpi.start(sim, boards_in_series, pwm)