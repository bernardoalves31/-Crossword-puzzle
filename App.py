grid = []
pathGrid = "tests/grid-11x11-20W-83L-38B.txt"
pathWords = "tests/words_list.txt"

with open(pathGrid, "r") as i:
    for line in i:
        grid.append(list(line.strip()))

print(grid[0][0])

words = []

with open(pathWords, "r") as i:
    for line in i:
        words.append(list(line.strip()))

