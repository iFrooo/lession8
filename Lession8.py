
"""Лото
 
Правила игры в лото.
 
Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.
 
Количество бочонков — 90 штук (с цифрами от 1 до 90).
 
Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:
 
--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------
 
В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 
 
Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.
 
Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
 
Побеждает тот, кто первый закроет все числа на своей карточке.
 
Пример одного хода:
 
Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 87     - 14    11      
      16 49    55 88    77    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)
 
Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.
 
Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://d...content-available-to-author-only...n.org/3/library/random.html
 
"""

import random, copy

MAX_BARREL = 90
DIGITS_IN_CARD = 15
DIGITS_IN_LINE = 5


def gen_card():
    '''
    :return: combination of int digits without repetition, k = DIGITS_IN_CARD, n = 1..MAX_BARREL, divided into 3 sorted lines
    eg. [[2, 11, 14, 30, 79], [43, 54, 60, 69, 77], [16, 74, 81, 82, 83]]
    '''
    # combination of 15 random digits 1..MAX_BARREL without repetitions
    num_comb = random.sample(range(1, MAX_BARREL + 1), DIGITS_IN_CARD)
    # make list of sorted slices of num_comb of size DIGITS_IN_LINE;
    # ie. divide num_comb into 3 sorted lists
    card = [sorted(num_comb[i:i + DIGITS_IN_LINE]) for i in range(0, len(num_comb), DIGITS_IN_LINE)]
    return card


def gen_barr_list():
    '''
    :return: list of barrels from 1 to MAX_BARREL distributed randomly
    '''
    return random.sample(range(1, MAX_BARREL + 1), 90)


def get_barrel(barr_list):
    '''
    return barrel generator from barrel list
    '''
    return barr_list.pop()


def show_card(card):
    '''
    return list of 3 card lines
    each line consists of 9 cells randomly filled with 5 sorted digits and 4 spaces
    cells are divided by spaces
    :param card: list of
    :return:
    '''
    card = copy.deepcopy(card)  # we don't want to modify the original list
    placeholders = ' '.join(['{:>2}' for i in range(9)])  # create 9 placeholders in 'cells', separated by spaces
    for line in card:
        for space in ' ' * 4:
            line.insert(random.randint(0, len(line) - 1), space)  # randomly insert 4 spaces in each card line
    return [placeholders.format(*line) for line in card]


def update_card(card, barrel):
    '''
    change digit in card to '-' if it match with barrel
    eg. 45 -> '-'
    player or comp
    :param card: list of 3 list, with 5 int in each
    :return: generator of a new card, where barrel digit is substituted for '-'
    '''
    # return [['-' if x == barrel else x for x in line] for line in card]
    for line in card:
        yield ['-' if x == barrel else x for x in line]


def is_empty(card):
    '''
    return False if card has at least one digit (non-dash symbol), True otherwise
    :param card: list of 3 lists, each contains up to 5 digits or '-' symbols
    '''
    for line in card:
        for elt in line:
            if elt != '-':
                return False
    return True


def barr_in_card(card, barrel):
    '''
    :return: True if card contains given digit
    '''
    return barrel in [barrel for line in card for barrel in line]
    # return True


def play_round():
    print('''Welcome to the loto game. You are playing against the computer.
You must not mistake or you lose.
Generating your card and mixing the barrels...\n''')
    player_card, comp_card = gen_card(), gen_card()
    barrels = gen_barr_list()
    while True:  # check if all digits are crossed
        next_barrel = get_barrel(barrels)
        print('New barrel: {}. Left: {}'.format(next_barrel, len(barrels)))
        print("{0} Player's card {0}\n{1}\n{2}\n{3}".format('-' * 6, *show_card(player_card)))
        print("{0} Computer's card {0}\n{1}\n{2}\n{3}".format('-' * 5, *show_card(comp_card)))
        answ = 'a'
        while answ not in 'ynq':
            answ = input("Is the barrel in player's card? y/n or q for exit: ")
        if answ == 'q':
            break
        elif (answ == 'y' and barr_in_card(player_card, next_barrel)) or (answ == 'n' and not barr_in_card(player_card,
                                                                                                           next_barrel)):
            print("You're right! \n\nNext turn...")
        else:
            print("You lose!")
            break
        player_card = list(update_card(player_card, next_barrel))
        comp_card = list(update_card(comp_card, next_barrel))
        if is_empty(player_card):
            print('You filled the entire card!')
            break
        if is_empty(comp_card):
            print('Computer filled the entire card!')
            break


play_round()y