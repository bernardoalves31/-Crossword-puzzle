class FileRead:
    @staticmethod
    def load(array, path):
        with open(path, "r") as i:
            for line in i:
                array.append(list(line.strip()))

    def find_horizontal_spaces(grid):   
        ROWS = len(grid)
        COLS = len(grid[0]) if grid else 0

        spaces = []
        for r in range(ROWS):
            c = 0
            while c < COLS:
                if grid[r][c] == '?':
                    start = c
                    while c < COLS and grid[r][c] == '?':
                        c += 1
                    length = c - start
                    if length > 1:
                        spaces.append((r, start, length, 'H'))
                else:
                    c += 1
        return spaces

    def find_vertical_spaces(grid):
        ROWS = len(grid)
        COLS = len(grid[0]) if grid else 0

        spaces = []
        for c in range(COLS):
            r = 0
            while r < ROWS:
                if grid[r][c] == '?':
                    start = r
                    while r < ROWS and grid[r][c] == '?':
                        r += 1
                    length = r - start
                    if length > 1:
                        spaces.append((start, c, length, 'V'))
                else:
                    r += 1
        return spaces