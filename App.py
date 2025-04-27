from FileRead import FileRead
from constraint import Problem, AllDifferentConstraint

pathGrid = "tests/grid-7x7-8W-33L-16B.txt"
pathWords = "tests/words_list.txt"

grid = []
words = []

FileRead.load(grid, pathGrid)
FileRead.load(words, pathWords)
