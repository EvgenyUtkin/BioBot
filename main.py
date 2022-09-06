import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from config import main_token

vk_session = vk_api.VkApi(token = main_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }

f = open('date_lesson.txt', 'r')
l = [line.strip() for line in f]
dl = l[0]
f.close()


keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('Настройка даты', 'secondary')],
        [get_but('Привет', 'primary'), get_but('Список', 'primary')],
        [get_but('Создать урок', 'positive'), get_but('Удалить урок', 'negative')],
        [get_but('Запись (Письм)', 'positive'), get_but('Отмена (Письм)', 'negative')],
        [get_but('Запись (Устн)', 'positive'), get_but('Отмена (Устн)', 'negative')],
        [get_but('Запись (Доска)', 'positive'), get_but('Отмена (Доска)', 'negative')]
    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

def sender(id, text):
    vk_session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : keyboard})


dates = []
l = []





for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if True:
                msg = event.text
                user_id = event.user_id
                chat_id = user_id
                user_get = vk.users.get(user_ids=(user_id))
                user_get = user_get[0]
                first_name = user_get['first_name']
                last_name = user_get['last_name']
                full_name = first_name + " " + last_name

                f = open('date_lesson.txt', 'r')
                date = [line.strip() for line in f][0]
                f.close()

                f = open('db.txt', 'r')
                l = [line.strip() for line in f]
                N = len(l) // 15
                dates = [l[15 * i + 1] for i in range(N)]
                f.close()

                if date in dates:
                    flag = 1
                else:
                    flag = 0


                W = []
                O = []
                B = []
                if (flag):
                    num = 0
                    while dates[num] != date:
                        num += 1
                    for i in range(4):
                        if l[15 * num + 3 + i][2:] != "":
                            W.append(l[15 * num + 3 + i][2:])
                    for i in range(4):
                        if l[15 * num + 8 + i][2:] != "":
                            O.append(l[15 * num + 8 + i][2:])
                    for i in range(1):
                        if l[15 * num + 13 + i][2:] != "":
                            B.append(l[15 * num + 13 + i][2:])

                if msg == 'Начать':
                    sender(chat_id, 'Начинаю')

                if msg == 'Привет':
                    sender(chat_id, f'Привет, {first_name}!')

                if msg == 'Настройка даты':
                    sender(chat_id, f'Текущая дата: {date}\nЧтобы поменять дату, введите новую в формате ДД.ММ.ГГГГ')

                if msg.count('.') == 2:
                    f = open('date_lesson.txt', 'w')
                    f.write(msg+'\n')
                    f.close()
                    sender(chat_id, f'Готово!\nНовая дата: {msg}')

                if msg == 'Список':
                    if not flag:
                        sender(chat_id, f"Ошибка: урок на {date} ещё не создан.")
                    else:
                        ans = ""
                        ans += date + '\n'
                        ans += "Письменно:" + '\n'
                        for i in range(4):
                            if i < len(W):
                                ans += f"{i + 1}. {W[i]}" + '\n'
                            else:
                                ans += f"{i + 1}. -" + '\n'
                        ans += "Устно:" + '\n'
                        for i in range(4):
                            if i < len(O):
                                ans += f"{i + 1}. {O[i]}" + '\n'
                            else:
                                ans += f"{i + 1}. -" + '\n'
                        ans += "У доски:" + '\n'
                        for i in range(1):
                            if i < len(B):
                                ans += f"{i + 1}. {B[i]}" + '\n'
                            else:
                                ans += f"{i + 1}. -" + '\n'
                        sender(chat_id, ans)

                update = 1

                if msg == 'Создать урок':
                    if flag:
                        sender(chat_id, f"Урок на {date} уже создан.")
                    #elif chat_id != 309167010:
                        #sender(chat_id, 'Создавать уроки может только Женя (пока что)')
                    else:
                        update = 0
                        l.append("=====")
                        l.append(date)
                        l.append("W")
                        l.append("1.")
                        l.append("2.")
                        l.append("3.")
                        l.append("4.")
                        l.append("O")
                        l.append("1.")
                        l.append("2.")
                        l.append("3.")
                        l.append("4.")
                        l.append("B")
                        l.append("1.")
                        l.append("=====")
                        sender(chat_id, f"Урок на {date} успешно создан. Записывайтесь скорее!")

                if msg == 'Удалить урок':
                    if not flag:
                        sender(chat_id, f"Урок на {date} уже удалён или не создан.")
                    elif chat_id != 309167010:
                        sender(chat_id, 'Удалять уроки может только Женя (пока что)')
                    else:
                        update = 0
                        for i in range(15):
                            l.pop(15 * num)
                        sender(chat_id, f"Урок на {date} успешно удалён.")

                if msg == 'Запись (Письм)':
                    if (not flag):
                        sender(chat_id, f"Ошибка: урок на {date} ещё не создан.")
                        continue
                    if len(W) == 4:
                        sender(chat_id, f"Увы, места для письменной работы {date} заняты.")
                    else:
                        if full_name in W:
                            sender(chat_id, f"Вы уже записаны на письменную работу {date}.")
                        else:
                            W.append(full_name)
                            sender(chat_id, f"Вы успешно записаны на письменную работу {date}.")

                if msg == 'Запись (Устн)':
                    if (not flag):
                        sender(chat_id, f"Ошибка: урок на {date} ещё не создан.")
                        continue
                    if len(O) == 4:
                        sender(chat_id, f"Увы, места для устной работы {date} заняты.")
                    else:
                        if full_name in O:
                            sender(chat_id, f"Вы уже записаны на устную работу {date}.")
                        else:
                            O.append(full_name)
                            sender(chat_id, f"Вы успешно записаны на устную работу {date}.")

                if msg == 'Запись (Доска)':
                    if (not flag):
                        sender(chat_id, f"Ошибка: урок на {date} ещё не создан.")
                        continue
                    if len(B) == 1:
                        sender(chat_id, f"Увы, места для работы у доски {date} заняты.")
                    else:
                        if full_name in B:
                            sender(chat_id, f"Вы уже записаны на работу у доски {date}.")
                        else:
                            B.append(full_name)
                            sender(chat_id, f"Вы успешно записаны на работу у доски {date}.")

                if msg == 'Отмена (Письм)':
                    if (not flag):
                        sender(chat_id, f"Ошибка: урок на {date} ещё не создан.")
                        continue
                    if full_name in W:
                        W.remove(full_name)
                    sender(chat_id, f"Вы отписались от письменной работы {date}.")

                if msg == 'Отмена (Устн)':
                    if (not flag):
                        sender(chat_id, f"Ошибка: урок на {date} ещё не создан.")
                        continue
                    if full_name in O:
                        O.remove(full_name)
                    sender(chat_id, f"Вы отписались от устной работы {date}.")

                if msg == 'Отмена (Доска)':
                    if (not flag):
                        sender(chat_id, f"Ошибка: урок на {date} ещё не создан.")
                        continue
                    if full_name in B:
                        B.remove(full_name)
                    sender(chat_id, f"Вы отписались от работы у доски {date}.")

                if (flag and update):
                    for i in range(4 - len(W)):
                        W.append("")
                    for i in range(4 - len(O)):
                        O.append("")
                    for i in range(1 - len(B)):
                        B.append("")
                    for i in range(4):
                        l[15*num+3+i] = f"{i+1}.{W[i]}"
                    for i in range(4):
                        l[15*num+8+i] = f"{i+1}.{O[i]}"
                    for i in range(1):
                        l[15*num+13+i] = f"{i+1}.{B[i]}"




                f = open('db.txt', 'w')
                for line in l:
                    f.write(line + '\n')
                f.close()



