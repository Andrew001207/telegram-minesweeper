import mines

#Vledz Komment

s_size = input()
x, y, num_mines = s_size.split(' ')
x = int(x)
y = int(y)
num_mines = int(num_mines)
print('\n')

game = mines.Minesweeper(x,y,num_mines)
game.print_field()
print('-'*x*2)
            
while True:
    print('input x and y:')
    x, y = input().split(' ')
    x = int(x)
    y = int(y)
    game.open_field(x-1,y-1)
    game.print_field()
    if game.check_victory() > 0:
        print('Game finished')
        break
    # victory = check_victory(mines, mask)
    # if victory == 1:
    #     print('Game lost')
    #     break
    # if victory == 2:
    #     print('U Won!')
    #     break
    # print('-'*x*2)
 