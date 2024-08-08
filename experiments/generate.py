import time
from sudoku.generator import Generator

settings = [
    {"max_iter": 100},
    {"max_iter": 300},
    {"max_iter": 1_000},
    {"max_iter": 3_000},
    {"max_iter": 10_000},
    {"max_iter": 30_000},
    {"max_iter": 50_000},
    {"max_iter": 100_000},
    # {"max_iter": 300_000},
    # {"max_iter": 500_000},
]

for setting in settings:
    generator = Generator(**setting)
    start = time.time()
    for i in range(100):
        sudoku_gt, sudoku = generator.generate(difficulty=2)
    print(setting, time.time() - start)

# 개선 후
# {'max_iter': 100} 13.153430938720703
# {'max_iter': 300} 7.073630332946777
# {'max_iter': 1000} 4.715806245803833
# {'max_iter': 3000} 5.754875183105469
# {'max_iter': 10000} 7.788494825363159
# {'max_iter': 30000} 9.983426094055176
# {'max_iter': 50000} 12.5775728225708
# {'max_iter': 100000} 17.169249057769775
