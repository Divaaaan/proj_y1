import pygsheets
import datetime

gc = pygsheets.authorize(
    client_secret='client_secret_636982354700-htd4geok3m5qjjijti6gdjq05e3bu66n.apps.googleusercontent.com.json')
sh = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1Quj8PNN0YpoSMJxc9WZI0vhTJhjM_1YF51DBbW4YSCs/edit#gid=2030006626')


def get_number():
    pr = sh.worksheet_by_title('доступ')
    out_list = [i[0] for i in pr.get_values_batch('A')[0][1:]]
    return out_list


# def add_id(phone_number, id):
#     usefull_list = sh[2].get_values_batch(('C'))[0][1:]
#     for i in range(len(usefull_list)):
#         if usefull_list[i][0] == phone_number and usefull_list[i][1] != str(id):
#             sh[2].update_value(f'D{i + 2}', id)
#             break


# def get_name_from_file(id):
#     usefull_list = sh[2].get_values_batch(('B'))[0][1:]
#     for i in usefull_list:
#         if str(id) == i[2]:
#             return i[0]


def get_all_list():
    pr = sh.worksheet_by_title('проект')
    return pr.get_all_values(returnas='matrix')


def push_data(data: list = None):
    pr = sh.worksheet_by_title('проект')
    today = datetime.date.today()
    list = pr.get_values_batch('B')[0]
    ans = []
    for i in range(len(list)):
        extra_list = []
        for j in range(len(list[i])):
            if list[i][j] != '':
                extra_list.append(list[i][j])
        if len(extra_list) != 0:
            ans.append(extra_list)
    ln = len(list) + 1
    pr.update_value((ln, 1 + 1), '.'.join(map(str, [today.day, today.month, today.year])))
    pr.update_value((ln, 2 + 1), data[0])
    pr.update_value((ln, 3 + 1), data[1])
    pr.update_value((ln, 5 + 1), data[2])
    if data[3] != '':
        pr.update_value((ln, 4 + 1), f'{data[3]}')
    last = pr.get_value((ln - 1, 6 + 1))
    if last == '':
        last = int(list[1][1])
    else:
        last = int(last.replace(u'\xa0', u'')[:-3])
    if data[0] == 'Поступление':
        last += int(data[1])
    else:
        last -= int(data[1])
    pr.update_value((ln, 6 + 1), str(last))
    return last


def push_balance(data, sum):
    pr = sh.worksheet_by_title('проект')
    list = pr.get_values_batch('B')[0]
    ans = []
    for i in range(len(list)):
        extra_list = []
        for j in range(len(list[i])):
            if list[i][j] != '':
                extra_list.append(list[i][j])
        if len(extra_list) != 0:
            ans.append(extra_list)
    list = ans
    ln = len(list)
    print(list)
    for i in range(ln - 1, -1, -1):
        if list[i] != [] and list[i][0] == data:
            pr.update_value((i + 1, 7 + 1), sum)
            return 1
    return 0


def get_list_of_points():
    pr = sh.worksheet_by_title('справочник статей')
    list = pr.get_all_values(returnas='matrix')[1:]
    ans = []
    for i in range(len(list)):
        extra_list = []
        for j in range(len(list[0])):
            if list[i][j] != '':
                extra_list.append(list[i][j])
        if len(extra_list) != 0:
            ans.append(extra_list)
    return ans[1:]


def get_list_of_actions():
    list = get_list_of_points()
    ans = []
    for i in list:
        if i[2] not in ans:
            ans.append(i[2])
    return ans


def get_names_of_exact_actions(type, action):
    list = get_list_of_points()
    ans = []
    for i in list:
        if i[1] == type and i[2] == action:
            ans.append(i[0])
    return ans
