import pygsheets
import datetime


def get_number():
    gc = pygsheets.authorize(
        client_secret='client_secret_636982354700-htd4geok3m5qjjijti6gdjq05e3bu66n.apps.googleusercontent.com.json')

    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1nYwMu-a-oH1aYNb0AD9JWz5CZMcJmRLLVO-XYwlEOBs/edit#gid=504054376')
    out_list = [i[0] for i in sh[1].get_values_batch('A')[0][1:]]
    return out_list


def add_id(phone_number, id):
    gc = pygsheets.authorize(
        client_secret='client_secret_636982354700-htd4geok3m5qjjijti6gdjq05e3bu66n.apps.googleusercontent.com.json')
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/10UiBTQ6wrBeakOxmAMA8UC2mVWVw5wz9khrRCEnXXx0/edit#gid=870125800')
    usefull_list = sh[2].get_values_batch(('C'))[0][1:]
    for i in range(len(usefull_list)):
        if usefull_list[i][0] == phone_number and usefull_list[i][1] != str(id):
            sh[2].update_value(f'D{i + 2}', id)
            break


def get_name_from_file(id):
    gc = pygsheets.authorize(
        client_secret='client_secret_636982354700-htd4geok3m5qjjijti6gdjq05e3bu66n.apps.googleusercontent.com.json')
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/10UiBTQ6wrBeakOxmAMA8UC2mVWVw5wz9khrRCEnXXx0/edit#gid=870125800')
    usefull_list = sh[2].get_values_batch(('B'))[0][1:]
    for i in usefull_list:
        if str(id) == i[2]:
            return i[0]


def get_all_list():
    gc = pygsheets.authorize(
        client_secret='client_secret_636982354700-htd4geok3m5qjjijti6gdjq05e3bu66n.apps.googleusercontent.com.json')
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1nYwMu-a-oH1aYNb0AD9JWz5CZMcJmRLLVO-XYwlEOBs/edit#gid=2030006626')
    return sh[0].get_all_values(returnas='matrix')


def push_data(data: list = None):
    gc = pygsheets.authorize(
        client_secret='client_secret_636982354700-htd4geok3m5qjjijti6gdjq05e3bu66n.apps.googleusercontent.com.json')
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1nYwMu-a-oH1aYNb0AD9JWz5CZMcJmRLLVO-XYwlEOBs/edit#gid=2030006626')
    today = datetime.date.today()
    matrix = sh[0].get_values_batch('A')[0]
    ln = len(matrix) + 1
    sh[0].update_value((ln, 1), '.'.join(map(str, [today.day, today.month, today.year])))
    sh[0].update_value((ln, 2), data[0])
    sh[0].update_value((ln, 3), data[1])
    sh[0].update_value((ln, 5), data[2])
    if data[3] != '':
        sh[0].update_value((ln, 4), f'Поступление тип {data[3]}')
    last = sh[0].get_value((ln - 1, 6))
    last = int(last.replace(u'\xa0', u'')[:-3])
    if data[0] == 'Поступление':
        last += int(data[1])
    else:
        last -= int(data[1])
    sh[0].update_value((ln, 6), str(last))
    return last


def push_balance(data, sum):
    gc = pygsheets.authorize(
        client_secret='client_secret_636982354700-htd4geok3m5qjjijti6gdjq05e3bu66n.apps.googleusercontent.com.json')
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1nYwMu-a-oH1aYNb0AD9JWz5CZMcJmRLLVO-XYwlEOBs/edit#gid=2030006626')
    matrix = sh[0].get_values_batch('A')[0]
    ln = len(matrix)
    for i in range(ln - 1, -1, -1):
        if matrix[i][0] == data:
            sh[0].update_value((i + 1, 7), sum)
            return None
