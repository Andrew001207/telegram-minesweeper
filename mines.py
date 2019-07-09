import itertools
from random import randint
print("init")
class Minesweeper:
    def __init__(self, width, height, num_mines):
        self.state = 0
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.minefield = None
        self.values = None
        self.mask = [['#' for i in range(self.width)]for j in range(self.height)]
        print('mask created')

    def generate_minefield(self, x, y, num_mines,exclude = None):
        mines = list(list(0 for i in range(x)) for j in range(y))
        if num_mines + len(exclude) > x * y:
            raise Exception("TOO MANY MINEZ!")
        for i in range(num_mines):
            while True:
                mine_x, mine_y = randint(0,x-1), randint(0,y-1)
                #print('placing mine at {0} {1}'.format(mine_x, mine_y))
                if mines[mine_y][mine_x] == 0 and not [mine_x, mine_y] in exclude:
                    mines[mine_y][mine_x] = 1
                    break
        return mines

    def count_mines(self, mines):
        values = [[0 for j in range(len(mines[0]))] for i in range(len(mines))]
        for i, line in enumerate(mines):
            for j, el in enumerate(line):
                for a,b in set(itertools.permutations([-1,0,1], 2))|set(itertools.combinations_with_replacement([-1,0,1],2)):
                    if 0 <= i+a < len(mines) and 0 <= j+b < len(mines[0]) and mines[i+a][j+b] == 1 and mines[i][j] == 0:
                        values[i][j] += 1
                    if mines[i][j] == 1:
                        values[i][j] = 9
        return values

    def open_field (self, x, y):
        if self.minefield == None or self.values == None or self.mask == None:
            self.minefield = self.generate_minefield(self.width, self.height, self.num_mines, exclude=[[x,y]] )
            print('Excludes({}, {})'.format(x,y))
            print('starting minefield generated')
            self.values = self.count_mines(self.minefield)
            print('start values calculated')

        def open_neighbors(x,y,mask,values):
            mask[y][x] = values[y][x]
            if values[y][x] == 0:
                if x+1 < len(mask[0]) and mask[y][x+1] == '#':
                    mask = open_neighbors(x+1, y, mask, values)
                if x-1 >= 0 and mask[y][x-1] == '#':
                    mask = open_neighbors(x-1, y, mask, values)
                if y+1 < len(mask) and mask[y+1][x] == '#':
                    mask = open_neighbors(x, y+1, mask, values)
                if y-1 >= 0 and mask[y-1][x] == '#':
                    mask = open_neighbors(x, y-1, mask, values)
            return mask
        self.mask = open_neighbors(x,y, self.mask, self.values)

    def print_field(self):
        field = self.minefield
        if field == None:
            print('NONE!')
            print(''.join(''.join(' #' for i in range(self.width))  + '\n' for j in range(self.height)))
            return
        for line in field:
            str_line = ''
            for i in range(len(line)):
                if line[i] == -1:
                    str_line += '*'
                else: 
                    str_line += ' {0}'.format(line[i])
            print(str_line)

    def check_victory(self):
        game = False
        for _mine_line, _mask_line in zip(self.minefield, self.mask):
            for _mine, _mask in zip(_mine_line, _mask_line):
                if _mine == 1 and _mask != '#':
                    self.state = 1
                    return 1
                if _mine == 0 and _mask == '#':
                    game = True
        if game == False:
            self.state = 2
            return 2
        else:
            return 0