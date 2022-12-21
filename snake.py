import curses
from random import randint

# setup window
curses.initscr()
win = curses.newwin(20, 60, 0, 0)  # y,x
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

# snake and food
snake = [(4, 10), (4, 9), (4, 8)]  # y,x
food = (10, 20)  # y,x

# game logic
score = 0

ESCAPE_KEY = 27
key = curses.KEY_RIGHT

while key != ESCAPE_KEY:
    win.addstr(0, 2, f"Score {score} ")
    win.timeout(150 - (len(snake)) // 5 + len(snake)//10 % 120)  # increase speed

    prev_key = key
    event = win.getch()

    #use last key if none entered
    key = event if event != -1 else prev_key

    # protect from bad input
    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESCAPE_KEY]:
        key = prev_key

    # calculate the next coordinates
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    snake.insert(0, (y, x))  # add to head of snake

    # did we hit a wall?
    if y == 0: break
    if y == 19: break
    if x == 0: break
    if x == 59: break

    # did snake run over itself?
    if snake[0] in snake[1:]: break

    if snake[0] == food:
        # eat the food
        score += 1
        food = ()

        # pick new food location, not within the snake
        while food == ():
            food = (randint(1, 18), randint(1, 59))
            if food in snake:
                food = ()

        win.addch(food[0], food[1], '#')  # put the food on the board
    else:
        # move snake
        last = snake.pop()
        win.addch(last[0], last[1], ' ')

    win.addch(snake[0][0], snake[0][1], '*')

    for c in snake:
        win.addch(c[0], c[1], '*')

    win.addch(food[0], food[1], '#')



curses.endwin()
print(f"Final score = {score}")
