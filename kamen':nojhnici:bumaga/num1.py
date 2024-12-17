import random
import PySimpleGUI as sg

kamen = '/Users/mac/Documents/pycharm/RGZ/kamen.png'
noj = '/Users/mac/Documents/pycharm/RGZ/nojh.png'
bumaga = '/Users/mac/Documents/pycharm/RGZ/bumaga.png'
special_image = '/Users/mac/Documents/pycharm/RGZ/pashalka.png'

sg.theme('LightGray1')

options = ['Камень', 'Ножницы', 'Бумага']
paths = {'Камень': kamen, 'Ножницы': noj, 'Бумага': bumaga}

wins = 0
round_history = []
paper_counter = 0
special_image_shown = False

name_layout = [
    [sg.Text("Введите ваше имя:")],
    [sg.Input(key='-NAME-', size=(15, 1))],
    [sg.Button("Начать игру")]
]
name_window = sg.Window("Введите имя", name_layout)

while True:
    event, values = name_window.read()
    if event == sg.WINDOW_CLOSED:
        exit()
    elif event == "Начать игру":
        player_name = values['-NAME-'] if values['-NAME-'].strip() else "Вы"
        name_window.close()
        break

layout = [
    [sg.Text('Сделайте выбор:')],
    [sg.Image(filename=kamen, enable_events=True, key='Камень'),sg.Image(filename=noj, enable_events=True, key='Ножницы'),sg.Image(filename=bumaga, enable_events=True, key='Бумага')],
    [sg.Frame(player_name, [[sg.Image(key='-USER-', size=(100, 100))]], size=(150, 150), relief=sg.RELIEF_SUNKEN),sg.Frame('Противник', [[sg.Image(key='-COMP-', size=(100, 100))]], size=(150, 150), relief=sg.RELIEF_SUNKEN)],
    [sg.Frame('Результат игры:', [
    [sg.Text('Результат: ', font='Arial 20', size=(15, 1), justification='left', key='-RESULT-')]],size=(400, 50), relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Счёт побед игрока: 0', key='-SCORE-', justification='left', font='Arial 16', size=(25, 1))],
    [sg.Image(key='-SPECIAL-', visible=False, size=(200, 200))],
    [sg.Button('Показать итоги', size=(15, 1), font='Arial 14'), sg.Button('Выйти', size=(10, 1), font='Arial 14')]
]

window = sg.Window('Камень, ножницы, бумага', layout, size=(480, 500))

def win(player, comp):
    if player == comp:
        return 'ни туда ни сюда', 'gray'
    elif (player == 'Камень' and comp == 'Ножницы') or (player == 'Ножницы' and comp == 'Бумага') or (player == 'Бумага' and comp == 'Камень'):
        return 'ура', 'green'
    else:
        return 'Незадача', 'red'

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Выйти':
        break

    if event == 'Показать итоги':
        history_layout = [
            [sg.Text("История раундов:", font='Arial 16')],
            [sg.Multiline('\n'.join(round_history) if round_history else 'Пока нет завершенных раундов.',
                          size=(40, 15), disabled=True)],
            [sg.Button("Закрыть")]
        ]
        history_window = sg.Window("Итоги раундов", history_layout)
        while True:
            history_event, _ = history_window.read()
            if history_event == sg.WINDOW_CLOSED or history_event == "Закрыть":
                history_window.close()
                break

    if event in options:
        choice = event
        comp_choice = random.choice(options)

        window['-USER-'].update(paths[choice])
        window['-COMP-'].update(paths[comp_choice])

        if choice == 'Бумага':
            paper_counter += 1
            if paper_counter == 15 and not special_image_shown:
                window['-SPECIAL-'].update(filename=special_image, visible=True)
                special_image_shown = True
            elif paper_counter > 15 and special_image_shown:
                window['-SPECIAL-'].update(visible=False)
                special_image_shown = False
                paper_counter = 0

        result, color = win(choice, comp_choice)
        window['-RESULT-'].update(result, text_color=color)
        round_history.append(f'Результат: {result}')

        if result == 'ура':
            wins += 1
            window['-SCORE-'].update(f'Счёт побед игрока: {wins}')

window.close()