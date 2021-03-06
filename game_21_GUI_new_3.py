"""Game BlackJack (21, point)"""
# Игра "Очко" ("21" или BlackJack) с использованием Tkinter

from tkinter import*
from random import randint
import json
from tkinter import messagebox
from datetime import datetime, timedelta


# Масти и номиналы карт
card_suits = ['diamonds', 'hearts', 'clubs', 'spades']
card_values = ['ace', 'king', 'queen', 'jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']

# розданные карты
cards = []
# сколько денег у игрока
balance = 1
# кол-во раздач
deal_count = 0

'''
# конструкция, чтобы изначально запустить файл
best_player = "Abo"
filename = 'best_player.json'
with open(filename, 'w') as f:
    json.dump(best_player, f)'''

# лучший показатель баланса, даже если игрок потом все проиграл
filename = 'record.json'
with open(filename) as f:
    best_balance = json.load(f)
# имя игрока с наибольшим достигнутым кол-вом $
filename = 'best_player.json'
with open (filename) as f:
    best_player = json.load(f)

'''
# конструкция, чтобы изначально запустить файлы
biggest_win = 1
filename = 'biggest_win.json'
with open(filename, 'w') as f:
    json.dump(biggest_win, f)
biggest_win_player = ""
filename = 'biggest_win_player.json'
with open(filename, 'w') as f:
    json.dump(biggest_win_player, f)'''
# наибольший выигрыш
filename = 'biggest_win.json'
with open (filename) as f:
    biggest_win = json.load(f)
# имя игрока с наибольшим выигрышем
filename = 'biggest_win_player.json'
with open (filename) as f:
    biggest_win_player = json.load(f)
filename = 'biggest_win.json'
with open(filename, 'w') as f:
    json.dump(biggest_win, f)

'''players_accounts = {}
filename = 'players_accounts.json'
with open(filename, 'w') as f:
    json.dump(players_accounts, f)'''
filename = 'players_accounts.json'
with open (filename) as f:
    players_accounts = json.load(f)
filename = 'players_accounts.json'
with open (filename, 'w') as f:
    json.dump(players_accounts, f)

# карты игрока и компьютера
my_cards = []
pc_cards = []
# выведенные на экран надписи и картинки
lbls = []
# текущий коэффицент начисления очков за победу - ставка (bet)
bet = 1
# коэффициент увеличения очков в зависимости от набора карт
ratio = 0
# выигрыш за одну раздачу
gain = 0
# имя игрока
player_name = ""
best_balance_date = ""
biggest_win_date = ""

game_time = timedelta(hours=0, minutes=0, seconds=0, milliseconds=0)
game_active = True


def init_name():
    global player_name
    # инициализация игрока и ввод имени
    # запрос имени игрока
    lbl_name = Label(window, text="Who are you?", font=("Courier", 14))
    lbl_name.place(x=10, y=10, width=140, height=30)
    # окно ввода
    name_entry = Entry(textvariable=player_name, width=20, font=("Courier", 14))
    name_entry.place(x=160, y=10, width=140, height=30)
    # установка курсора в поле ввода
    name_entry.focus()
    # кнопка подтверждения имени -> функция активирует кнопку Take card
    name_btn = Button(text="OK", width=16, font=("Courier", 14),
                      command=lambda: btn_take_normal(lbl_name, name_btn, name_entry))
    name_btn.place(x=310, y=10, width=140, height=30)


def btn_take_normal(lbl_name, name_btn, name_entry):
    global player_name
    # инициализация имени игрока
    player_name = name_entry.get()
    # убираю с экрана все поля, связанные с вводом имени игрока
    lbl_name.destroy()
    name_btn.destroy()
    name_entry.destroy()
    # вместо поля для ввода имени вывожу приветствие
    lbl = Label(window, text=f"Good luck {player_name}!", font=("Courier", 18))
    lbl.place(x=10, y=10)
    # кнопка Take card становится активной после ввода имени игрока
    btn_take.config(state='normal')
    # вызов функции обновляющей текущее время
    update_time()


def deal():
    # Сдача карты
    while True:
        # случайная масть
        random_suit = randint(0, 3)
        # случайный номинал карты
        random_value = randint(0, 12)
        card = f"{card_values[random_value]}_of_{card_suits[random_suit]}"
        # проверяю, если такая карта уже была выдана, то выдается заново
        if card in cards:
            cards.remove(card)
        # если не выдана, то добавляем к выданным
        else:
            cards.append(card)
            return card


def count_points(value):
    # Определение кол-ва очков в зависимости от номинала карты по первой букве card
    points = 0
    for x in value:
        # если карта ace (туз)
        if x[0] == 'a':
            # проверяю, если очков будет больше 21, то туз = 1 очко
            if (points + 11) > 21:
                points += 1
            # если очков будет меньше 21, то туз = 11 очков
            else:
                points += 11
        # если карты это "картинки" или "10", то прибавляем 10 очков
        elif x[0] == 'k' or x[0] == 'q' or x[0] == 'j' or x[0] == '1':
            points += 10
        # прибавляю очки в зависимости от номинала карты
        else:
            points += int(x[0])

    return points


def get_my_cards():
    # набор карт игрока
    global ratio

    # кнонка play again пока недоступна
    btn_clear.config(state='disabled')
    # вызываю функцию deal, чтобы выдать мне карту
    my_cards.append(deal())
    # рассчитываем кол-во очков в зависмости от выданной карты
    my_points = count_points(my_cards)
    for i in range(len(my_cards)):
        # вывожу на экран мои карты
        card_image = PhotoImage(file=f"images/{my_cards[i]}.gif")
        #card_image = card_image.subsample(2, 2)
        lbl = Label(window)
        lbl.image = card_image
        lbl['image'] = lbl.image
        lbl.place(x=40, y=230 + i*50)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)
        # вывожу на экран кол-во очков
        lbl = Label(window, text=f"{my_points} points", font=("Courier", 12))
        lbl.place(x=30, y=160)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)

    # если очков достаточно - нажимаем кнопку Enough
    btn_enough = Button(window, text="Enough", font=("Courier", 12), width=16,
                        command=lambda: get_pc_cards(my_points))
    btn_enough.place(x=160, y=110, width=140)

    if my_points > 21:
        # если кол-во очков больше 21 - проигрыш -перебор
        lbl = Label(window, text=f"Too many", font=("Courier", 12))
        lbl.place(x=30, y=190)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)
        # кнопки Take card и Enough не активны
        btn_take.config(state='disabled')
        btn_enough.config(state='disabled')
        # общий счет добавляется в пользу pc с учетом коэффицента
        ratio = -1
        # кнопка play_again снова активна
        btn_clear.config(state='normal')
        # переход в функцию, отображающую общий счет
        show_total_score()

    # если 21 очко на 2-х картах - BlackJack
    elif my_points == 21 and len(my_cards) == 2:
        #blackjack = True
        ratio = 2
        lbl = Label(window, text="Blackjack", font=("Courier", 12))
        lbl.place(x=30, y=190)
        lbls.append(lbl)
    # если карт 5 и очков 21 или меньше - возможен выигрыш с тройной ставкой
    elif len(my_cards) == 5 and my_points <= 21:
        #five_cards = True
        ratio = 3
        lbl = Label(window, text="5 cards", font=("Courier", 12))
        lbl.place(x=30, y=190)
        lbls.append(lbl)
    # если карт 6 и более и очков 21 или меньше - возможен выигрыш с четверной ставкой
    elif len(my_cards) >= 6 and my_points <= 21:
        ratio = 4
        #six_cards = True
        lbl = Label(window, text="6 cards", font=("Courier", 12))
        lbl.place(x=30, y=190)
        lbls.append(lbl)

    elif len(my_cards) == 3:
        count_7 = 0
        for i in range(3):
            for k in my_cards[i]:
                if k[0] == '7':
                    count_7 += 1
        if count_7 == 3:
            ratio = 5
            lbl = Label(window, text="7 7 7", font=("Courier", 12))
            lbl.place(x=30, y=190)
            lbls.append(lbl)
        else:
            ratio = 1


def get_pc_cards(my_points):
    # набор карт компа и расчет очков в зависимости от всех карт
    pc_points = 0
    # кнопка take отключена
    btn_take.config(state='disabled')
    # Определение карт компьютера
    while pc_points < 17:
        # карта PC
        pc_cards.append(deal())
        pc_points = count_points(pc_cards)

        for i in range(len(pc_cards)):
            # вывод на экран карт PC
            card_image = PhotoImage(file=f"images/{pc_cards[i]}.gif")
            lbl = Label(window)
            lbl.image = card_image
            lbl['image'] = lbl.image
            lbl.place(x=190, y=230 + i * 50)
            # все надписи на экране добавляются в список
            lbls.append(lbl)

        # вывод кол-ва очков pc на экран
        lbl = Label(window, text=f"{pc_points} points", font=("Courier", 12))
        lbl.place(x=180, y=160)
        lbls.append(lbl)

    get_winner(my_points, pc_points)


def get_winner(my_points, pc_points):
    global bet
    global gain
    global ratio

    if pc_points > 21:
        # если у PC перебор
        lbl = Label(window, text="Too many", font=("Courier", 12))
        lbl.place(x=180, y=190)
        lbls.append(lbl)

    elif pc_points >= 17:
        # определение победителя
        # и расчет выигрыша игрока в зависимости от расклада
        if my_points > pc_points:
            '''if blackjack is True:
                ratio = 2
            elif five_cards is True:
                ratio = 3
            elif six_cards is True:
                ratio = 4
            elif seven_3 is True:
                ratio = 5
            else:
                ratio = 1'''
            #show_total_score()

        elif my_points == pc_points:
            # при равном кол-ве очков ставка увеличивается в 2 раза
            gain = 0
            bet *= 2
            ratio = 0
            lbl = Label(window, text='No one won. Double the bet.', font=("Courier", 12) )
            lbl.place(x=30, y=190)
            # вывод ставки на экран
            show_bet()
            # кнопка Play again активна
            btn_clear.config(state='normal')
            # собираю все lbl
            lbls.append(lbl)

        else:
            # если у игрока меньше очков
            # расчет проигрыша игрока в зависимости от расклада
            if pc_points == 21 and len(pc_cards) == 2:
                lbl = Label(window, text="Blackjack", font=("Courier", 12))
                lbl.place(x=180, y=190)
                lbls.append(lbl)
                ratio = -2
            elif len(pc_cards) == 5 and pc_points <= 21:
                lbl = Label(window, text="5 cards", font=("Courier", 12))
                lbl.place(x=180, y=190)
                lbls.append(lbl)
                ratio = -3
            elif len(pc_cards) >= 6 and pc_points <= 21:
                lbl = Label(window, text="6 cards", font=("Courier", 12))
                lbl.place(x=180, y=190)
                lbls.append(lbl)
                ratio = -4
            elif len(pc_cards) == 3:
                count_7 = 0
                for i in range(3):
                    for k in pc_cards[i]:
                        if k[0] == '7':
                            count_7 += 1
                if count_7 == 3:
                    lbl = Label(window, text="7 7 7", font=("Courier", 12))
                    lbl.place(x=180, y=190)
                    lbls.append(lbl)
                    ratio = -5
                else:
                    ratio = -1
            else:
                ratio = -1

    show_total_score()

    btn_clear.config(state='normal')
    btn_take.config(state='disabled')


def show_total_score():
    # вывод баланса игрока
    global best_balance
    global ratio
    global best_player
    global player_name
    global deal_count

    get_balance()

    show_balance()
    show_bet()
    show_gain()
    show_deal_count()

    # кнопка Enough становится неактивной
    btn_enough_disabled()

    deal_count += 1

    # если денег меньше 0$ - конец игры
    if balance < 0:
        game_over()

    # определяю если текущий баланс лучще рекордного баланса
    if balance > best_balance:
        best_balance_record()


def get_balance():
    global balance
    global gain
    global ratio
    gain = ratio * bet
    balance += gain


def play_again(lbls):
    # новая раздача
    global my_cards
    global pc_cards
    global ratio
    global deal_count
    # карты игрока и PC обнуляются
    my_cards = []
    pc_cards = []
    # стираю с экрана карты с предыдущей раздачи
    for lbl in lbls:
        lbl.destroy()
    # кнопка Take card активна
    btn_take.config(state='normal')
    ratio = 1


def best_balance_record():
    global best_balance
    global best_player
    # инициализация наибольшего баланса
    best_balance = balance
    best_player = player_name
    best_balance_date = f"{datetime.strftime(datetime.now(),'%d.%m.%y')}"
    # запись в файл лучшего баланса (даже если потом все было проиграно)
    filename = 'record.json'
    with open(filename, 'w') as f:
        json.dump(best_balance, f)
    # запись в файл имя игрока с лучшим балансом
    filename = 'best_player.json'
    with open(filename, 'w') as f:
        json.dump(f"{best_player} {best_balance_date}", f)
    # заново загружаю данные о лучшем балансе и игроке
    # лучший показатель баланса, даже если игрок потом все проиграл
    filename = 'record.json'
    with open(filename) as f:
        best_balance = json.load(f)
    # имя игрока с наибольшим достигнутым кол-вом $
    filename = 'best_player.json'
    with open(filename) as f:
        best_player = json.load(f)


def biggest_win_record():
    # инициализация наибольшего выигрыша
    global biggest_win_date
    biggest_win = balance
    biggest_win_player = player_name
    biggest_win_date = f"{datetime.strftime(datetime.now(),'%d.%m.%y')}"
    # запись в файл наибольшего выигрыша
    filename = 'biggest_win.json'
    with open(filename, 'w') as f:
        json.dump(biggest_win, f)
    # запись в файл игрока с наивысшем выигрышем
    filename = 'biggest_win_player.json'
    with open(filename, 'w') as f:
        json.dump(f"{biggest_win_player} {biggest_win_date}", f)



def btn_enough_disabled():
    # кнопка Enough - игроку больше не нужно карт, ход переходит к PC
    btn_enough = Button(window, text="Enough", font=("Courier", 12), width=16, command=get_pc_cards)
    btn_enough.place(x=160, y=110, width=140)
    btn_enough.config(state='disabled')


def btn_take_disabled():
    btn_take.config(state='disabled')


def btn_clear_disabled():
    btn_clear = Button(window, text="Play again", font=("Courier", 12), width=16,
                       command=lambda: play_again(lbls))
    btn_clear.place(x=310, y=110, width=140)
    btn_clear.config(state='disabled')


def show_bet():
    # вывод на экран текущей ставки
    lbl = Label(window, text="bet", font=("Courier", 10))
    lbl.place(x=175, y=50)
    lbl = Label(window, text=f"{bet}", font=("Courier", 18))
    lbl.place(x=175, y=70)


def show_gain():
    # показываю выигрыш на прошлой раздаче
    lbl = Label(window, text="gain", font=("Courier", 10))
    lbl.place(x=90, y=50)
    lbl = Label(window, text=f"{gain}$", font=("Courier", 18))
    lbl.place(x=90, y=70, width=40)

def show_deal_count():
    # показываю кол-во раздач
    lbl = Label(window, text="deal", font=("Courier", 10))
    lbl.place(x=250, y=50)
    lbl = Label(window, text=f"{deal_count}", font=("Courier", 18))
    lbl.place(x=250, y=70)

def show_balance():
    # показываю баланс игрока (сколько денег)
    lbl = Label(window, text="money", font=("Courier", 10))
    lbl.place(x=10, y=50)
    total_balance = Label(window, text=f"{balance}$", font=("Courier", 18))
    total_balance.place(x=10, y=70, width=40)


def game_over():
    # конец игры, когда у игрока заканчиваются деньги
    global game_active

    game_active = False

    lbl = Label(window, text="You don't have any more money", font=("Courier", 11))
    lbl.place(x=90, y=240)
    lbl = Label(window, text="GAME OVER", font=("Courier", 40))
    lbl.place(x=80, y=280)

    btn_clear_disabled()
    btn_take_disabled()


def update_time():
    global game_time
    global game_active
    if game_active is True:
        game_time += timedelta(seconds=1)
        time_lbl_sec.config(text=f"{game_time}")
        window.after(1000, update_time)
    else:
        time_lbl_sec.config(text=f"{game_time}")
        window.after(1000, update_time)


def update_global_time():
    time_lbl.config(text=f"{datetime.now():%H:%M:%S}", font=("Courier", 10))
    window.after(10, update_global_time)


def close():
    global balance
    global player_name
    # вывод окна с запросом выхода из игры
    if balance > 0:
        if messagebox.askokcancel("Exit",
            f"{player_name}, you have {balance}$\nDo you really want to quit?"):
            if balance > biggest_win:
                biggest_win_record()

            window.destroy()
    else:
        window.destroy()



window = Tk()
window.protocol("WM_DELETE_WINDOW", close)
window.title(f"Welcome to Oriono's Blackjack! Now is {datetime.now():%d}"
             f" of {datetime.now():%B} {datetime.now():%Y}")
window.geometry("460x560")
window.resizable(0, 0)

# показываю лучший баланс и имя игрока внизу игрового экрана
lbl = Label(window, text=f"Biggest balance: "
                         f"{best_player} {best_balance}$", font=("Courier", 10))
lbl.place(x=10, y=530)

# показываю лучший выигрыш и имя игрока с лучшим выигрышем
lbl = Label(window, text=f"Biggest win: {biggest_win_player} "
                         f"{biggest_win}$", font=("Courier", 10))
lbl.place(x=10, y=510)

# показываю текущее время
time_lbl = Label(window, font=("Courier", 10))
time_lbl.place(x=370, y=530)
# показываю время игры
time_lbl_sec = Label(window, font=("Courier", 12))
time_lbl_sec.place(x=360, y=15)

# кнопка Take card - взять еще карту игроку
btn_take = Button(window, text="Take card", font=("Courier", 12), width=16, command=get_my_cards)
btn_take.place(x=10, y=110, width=140)
btn_take.config(state='disabled')

# кнопка Play again - карты обнуляются, новая сдача
btn_clear = Button(window, text="Play again", font=("Courier", 12), width=16,
                   command=lambda: play_again(lbls))
btn_clear.place(x=310, y=110, width=140)
btn_clear.config(state='disabled')

# текущее время
update_global_time()
# кнопка Enough неактивна
btn_enough_disabled()
# ввод имени игрока
init_name()
# общий счет всей игры
show_total_score()
# главный цикл игры
window.mainloop()