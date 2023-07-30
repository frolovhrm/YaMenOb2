import datetime
import re

error_log = ''


def readTextToFields3(fields, str_line):
    """ Парсим строку, достаем данные по полям"""
    fields.error_log[0] = 3

    # print(f"read3 {str_line}")

    def getfloat(str_ex):
        # print(str)
        new_str = str_ex.replace(',‚', ',')
        # print(new_str)
        new_str = new_str.replace('‚', '.')
        # print(new_str)
        new_str = new_str.replace(',', '.')
        # print(new_str)
        new_str = new_str.replace('Р', '')
        # print(new_str)
        new_str = new_str.replace('>', '')
        # print(new_str)
        new_str = new_str.replace('<', '')
        # print(new_str)
        new_str = new_str.replace('»', '')
        # print(new_str)
        new_str = new_str.replace('«', '')

        if new_str.isdigit():
            result = float(new_str)
            # print(f'getfloat 5.1 - {result}')
        else:
            try:
                new_str_num = re.findall(r'\d*\.\d\d', new_str)
                result = float(new_str_num[0])
                # print(f'getfloat 5.2 - {result}')
            except:
                # print(f'Ошибка функции getFloat new - {new_str} -< {str_line} >- {fields.name}')
                fields.error_log[11] = 1

        return result

    # print(str_line)
    position = 0
    while position < len(str_line):

        """ Активность, Рейтинг, Уровень """
        if str_line[position] == 'Самозанятый':
            # print('Activ, grait, rait')
            try:
                fields.activ = int(str_line[position + 1])
            except:
                # print(f'Activ - {fields.name} - {str_line[position + 1]} - {str_line}')
                fields.error_log[1] = 1

            fields.rait = float(str_line[position + 2])

            if str_line[position + 3] == 'Бронза':
                fields.grate = 4
            if str_line[position + 3] == 'Серебро':
                fields.grate = 3
            if str_line[position + 3] == 'Золото' or 'Золот':
                fields.grate = 2
            if str_line[position + 3] == 'Платина':
                fields.grate = 1
            # print('Activ - ', fields.activ, 'grait - ', fields.grate, 'rait - ', fields.rait)
            position += 1

        """ Заказов 1, Доход 1, Баланс 1"""
        if str_line[position] == 'заказов' or str_line[position] == 'заказа':
            if str_line[position - 5] == 'Сегодня':
                try:
                    fields.orders = int(str_line[position - 1])
                except ValueError:
                    # print(f'Error orders new3 - {str_line[position - 1]} - {fields.name} - {str_line}')
                    fields.error_log[7] = 1

                all_profit_str = str_line[position + 1]
                balance_str = str_line[position + 2]
                # print(all_profit_str, balance_str)

                try:
                    fields.all_profit = getfloat(all_profit_str)
                    # print(f'All profit new3 (try) {fields.all_profit}')
                except:
                    # print(f"Ошибка All_profit_new3 {all_profit_str} - {fields.name} - {str_line}")
                    fields.error_log[4] = 1

                try:
                    fields.balance = getfloat(balance_str)
                    # print(f'Balance new3 (try) {fields.balance}')
                except:
                    # print(f"Ошибка Balance3 {balance_str} - {fields.name} - {str_line}")
                    fields.error_log[10] = 1
            position += 1
            continue

        """ Заказов 2, Доход 2"""
        if str_line[position] == 'Доход':
            if str_line[position + 3] == 'заказов':
                try:
                    fields.orders = int(str_line[position + 2])
                except ValueError:
                    # print(f'Error orders new3.2 - {str_line[position - 1]} - {fields.name} - {str_line}')
                    fields.error_log[7] = 1

                all_profit_str = str_line[position + 1]
                try:
                    fields.all_profit = getfloat(all_profit_str)
                    # print(f'All profit new3 (try) {fields.all_profit}')
                except:
                    # print(f"Ошибка All_profit_new3.1 {all_profit_str} - {fields.name} - {str_line}")
                    fields.error_log[4] = 1
            position += 1
            continue

        """ Наличные"""
        if str_line[position] == 'Наличными':
            cash_profit_str = str_line[position + 1]
            try:
                fields.cash_profit = getfloat(cash_profit_str)
                # print(f'Cash profit new3 (try) {fields.cash_profit}')
            except:
                # print(f"Ошибка Cash profit new3 {cash_profit_str} - {fields.name} - {str_line}")
                fields.error_log[5] = 1
            position += 1
            continue

        """ Карта"""
        if str_line[position] == 'Картой':
            card_profit_str = str_line[position + 1]
            try:
                fields.card_profit = getfloat(card_profit_str)
                # print(f'Cash profit new3 (try) {fields.cash_profit}')
            except:
                # print(f"Ошибка Card profit new3 {card_profit_str} - {fields.name} - {str_line}")
                fields.error_log[6] = 1
            position += 1
            continue

        """ Комиссия"""
        if str_line[position] == 'Комиссии':
            commision_profit_str = str_line[position + 2]
            try:
                fields.commission = getfloat(commision_profit_str)
                # print(f'Commission new3 (try) {fields.cash_profit}')
            except:
                # print(f"Ошибка Commission new3 {commision_profit_str} - {fields.name} - {str_line}")
                fields.error_log[8] = 1
            position += 1
            continue

        """ Чаевые"""
        if str_line[position] == 'Чаевые':
            tips_profit_str = str_line[position + 1]
            try:
                fields.tips = getfloat(tips_profit_str)
                # print(f'Commission new3 (try) {fields.cash_profit}')
            except:
                # print(f"Ошибка Commission new3 {tips_profit_str} - {fields.name} - {str_line}")
                fields.error_log[11] = 1
            position += 1
            continue

        position += 1

    # print(fields.activ, fields.rait, fields.grate, fields.orders, fields.all_profit, fields.cash_profit, fields.card_profit, fields.balance, fields.tips)
