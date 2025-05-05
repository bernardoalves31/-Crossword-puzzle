from time import time
from FileRead import FileRead
from CspSolver import CspSolver
from constraint import Problem, AllDifferentConstraint

gridsPath = ['data/grid-11x11-20W-83L-38B.txt',
            'data/grid-15x15-34W-169L-56B.txt',
            'data/grid-25x25-88W-400L-225B.txt']

pathGrid = gridsPath[0]
pathWords = "data/lista_palavras.txt"

outputPath = 'output/result.txt'

grid = []
words = []
FileRead.load(grid, pathGrid)
FileRead.load(words, pathWords)

grid = [list(row) for row in grid]
words = [''.join(word) if isinstance(word, list) else word for word in words]
words = list(set(words))
filtered_spaces = []

class App:
    def run():
        start_time = time()
        
        spaces = FileRead.find_horizontal_spaces(grid) + FileRead.find_vertical_spaces(grid)

        problem = Problem(CspSolver())
        allDomains = []

        for idx, (r, c, length, direction) in enumerate(spaces):
            domain = [word for word in words if len(word) == length]
            if domain:
                allDomains.append(domain)
                problem.addVariable(idx, domain)
                filtered_spaces.append((idx, (r, c, length, direction)))

        for i in range(len(filtered_spaces)):
            for j in range(i + 1, len(filtered_spaces)):
                idx1, space1 = filtered_spaces[i]
                idx2, space2 = filtered_spaces[j]
                problem.addConstraint(
                    lambda w1, w2, s1=space1, s2=space2: App.no_conflict(w1, w2, s1, s2),
                    (idx1, idx2)
                )
                
        problem.addConstraint(AllDifferentConstraint())

        solutions = problem.getSolution()
        
        end_time = time()
        execution_time = end_time - start_time

        App.print(solutions, execution_time)
    
    def no_conflict(word1, word2, space1, space2):
        (r1, c1, len1, dir1) = space1
        (r2, c2, len2, dir2) = space2

        occupied1 = []
        for i in range(len1):
            if dir1 == 'H':
                occupied1.append((r1, c1 + i, word1[i]))
            else:
                occupied1.append((r1 + i, c1, word1[i]))

        occupied2 = []
        for i in range(len2):
            if dir2 == 'H':
                occupied2.append((r2, c2 + i, word2[i]))
            else:
                occupied2.append((r2 + i, c2, word2[i]))

        pos1 = {(row, col): letter for row, col, letter in occupied1}
        pos2 = {(row, col): letter for row, col, letter in occupied2}

        for pos in pos1.keys() & pos2.keys():
            if pos1[pos] != pos2[pos]:
                return False
        return True
    

    def fill_grid(solution):
        filled = [row.copy() for row in grid]
        for idx, word in solution.items():
            r, c, length, direction = next((space[1] for space in filtered_spaces if space[0] == idx), (None, None, None, None))
            if r is not None:
                if direction == 'H':
                    for i, ch in enumerate(word):
                        filled[r][c + i] = ch
                else:
                    for i, ch in enumerate(word):
                        filled[r + i][c] = ch
        return filled


    def print(solution, execution_time):
        with open(outputPath, 'w') as file:
            file.write(f"Execution time:")
            file.write(f"\n\t{execution_time:.4f} seconds")

            file.write("\n\nGrade inicial:")
            for row in grid:
                file.write(f'\n\t{''.join(row)}')

            file.write(f"\n\nNúmero de palavras:")
            file.write(f"\n\t{len(words)}")

            file.write("\n\nSolução:")
            filled = App.fill_grid(solution)
            for row in filled:
                file.write(f'\n\t{''.join(row)}')