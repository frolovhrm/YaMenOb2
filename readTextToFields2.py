import datetime
import re

error_log = ''

def readTextToFields2(fields, str_line):
    """ Парсим строку, достаем данные по полям"""
    fields.error_log[0] = 2

    def getfloat(str):
        # print(str)
        new_str = str.replace(',‚', ',')
        new_str = new_str.replace('‚', '.')
        new_str = new_str.replace(',', '.')
        new_str = new_str.replace('Р', '')
        new_str = new_str.replace('>', '')
        new_str = new_str.replace('<', '')
        new_str = new_str.replace('»', '')
        new_str = new_str.replace('«', '')
        new_str = new_str.replace('›', '')


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
                fields.error_log[10] = 1

        return result

    # print(str_line)
    position = 0
    bed_words = ['История', 'Отмена', 'Обновлен', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь', 'Поездка', 'попали', 'этот', 'Оцените',
                 'качества', 'следующем', 'Доступно', 'комплименты', 'приоритет', 'транзакции']

    while position < len(str_line):
        atention = ''

        if position + 3 > len(str_line):
            # print('первышен размер строки')
            break

        """ Неверный скрин """
        for i in bed_words:
            if str_line[position] == i:
                atention = 'atention'
                # print(f'atention {i}')
                break
        if atention == 'atention':
            break

        if str_line[position] == 'За' and str_line[position + 1] == 'неделю':
            break

        if str_line[position] == 'За' and str_line[position + 2] == 'неделю':
            break

        if str_line[position] == 'Сегодня':
            if str_line[position + 2] == '0, 00':
                break
            if str_line[position + 2] == '0,00Р':
                break
            if str_line[position + 2] == '0,00?':
                break
            if str_line[position + 2] == '0,00?Р':
                break

        """ Заказов """
        if str_line[position] == 'заказов' or str_line[position] == 'заказа':
            if str_line[position - 1] != "для":
                if str_line[position - 1] != 'стоимости':
                    # print('orders')
                    try:
                        fields.orders = int(str_line[position - 1])
                    except ValueError:
                        # print(f'Error orders new - {str_line[position - 1]} - {fields.name} - {str_line}')
                        fields.error_log[7] = 1

                    # print(f'orders - {fields.orders}')
            position += 1
            continue

        """ Активность, Рейтинг, Уровень """
        if str_line[position] == 'Самозанятый':
            # print('Activ, grait, rait')
            try:
                fields.activ = int(str_line[position + 1])
            except:
                # print(f'Activ - {fields.name} - {str_line[position + 1]} - {str_line}')
                fields.error_log[1] = 1



            fields.rait = float(str_line[position + 2])
            if str_line[position + 3] == 'Серебро':
                fields.grate = 4
            if str_line[position + 3] == 'Бронза':
                fields.grate = 3
            if str_line[position + 3] == 'Золото':
                fields.grate = 2
            if str_line[position + 3] == 'Платина':
                fields.grate = 1
            # print('Activ - ', fields.activ, 'grait - ', fields.grate, 'rait - ', fields.rait)
            position += 1
            continue

        if str_line[position] == 'Сегодня':
            """ Всего выручка """
            # print('All')

            if len(str_line[position + 2]) == 1:  # если сиввол только один, добавляем из следующей позиции
                all_profit_str = str_line[position + 2] + str_line[position + 3]
                # print(f'All profit new{all_profit_str}')
            else:
                all_profit_str = str_line[position + 2]
                # print(f'All profit new (else) {all_profit_str}')

            try:
                fields.all_profit = getfloat(all_profit_str)
                # print(f'All profit new (try) {fields.all_profit}')
            except:
                # print(f"Ошибка All_profit_new {all_profit_str} - {fields.name} - {str_line}")
                fields.error_log[4] = 1
            # print(f'All_profit - {fields.all_profit}')
            position += 1
            continue

        """ Выручка карта """
        if str_line[position] == 'По':
            # print('Cart')
            try:
                if len(str_line[position + 2]) == 1:  # если сиmвол только один, добавляем из следующей позиции
                    card_profit_str = str_line[position + 2] + str_line[position + 3]
                else:
                    card_profit_str = str_line[position + 2]
            except:
                fields.error_log[6] = 1
                position += 1
                continue


            try:
                fields.card_profit = getfloat(card_profit_str)
            except:
                # print(f"Ошибка card_profit_new - {card_profit_str}")
                fields.error_log[6] = 1

            # print('Card - ', fields.card_profit)
            position += 1
            continue

        """ Выручка наличные """
        if str_line[position] == 'Наличными':
            if str_line[position + 1] != 'или':
                # print('Cash')
                if len(str_line[position + 1]) == 1:  # если сиввол только один, добавляем из следующей позиции
                    cash_profit_str = str_line[position + 1] + str_line[position + 2]
                else:
                    cash_profit_str = str_line[position + 1]

                try:
                    fields.cash_profit = getfloat(cash_profit_str)
                except:
                    # print(f'Ошибка cash_profit_new {str_line[position]}')
                    fields.error_log[5] = 1


            # print(f'cash_profit - {fields.cash_profit}')
            position += 1
            continue

        """ Комиссия """
        if str_line[position] == 'Сервис':
            # print('Comission')

            if len(str_line[position + 2]) == 1:  # если сиввол только один, добавляем из следующей позиции
                commission_str = str_line[position + 2] + str_line[position + 3]
            else:
                commission_str = str_line[position + 2]

            try:
                fields.commission = getfloat(commission_str)
            except:
                # print(f"Ошибка comission new - {commission_str} - {fields.name} - {str_line}")
                fields.error_log[8] = 1
            # print(f'Comission - {fields.commission}')
            position += 1
            continue

        """ Баланс """
        if str_line[position] == 'Баланс':
            # print('Balance')
            if len(str_line[position + 1]) == 1:  # если сиввол только один, добавляем из следующей позиции
                balance_str = str_line[position + 1] + str_line[position + 2]
                # print(f'Balance new{balance_str}')
            else:
                balance_str = str_line[position + 1]
                # print(f'Balance (else) new{balance_str}')

            try:
                fields.balance = getfloat(balance_str)
                # print(f'Balance (else) new{fields.balance}')
            except:
                # print(f"Ошибка balance new - {balance_str} - {fields.name}  - {str_line}")
                fields.error_log[9] = 1

            # print(f'Balance - {fields.balance}')
        position += 1
