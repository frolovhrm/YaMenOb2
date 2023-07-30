import json
import os
import datetime
import sqlite3 as sq
import pytesseract
import logging
import cv2

from tqdm import tqdm
from dotenv import load_dotenv

from creat_ob_2_db import createNewBase
from readTextToFields import readTextToFields
from readTextToFields2 import readTextToFields2
from readTextToFields3 import readTextToFields3
from analitic_new import *

load_dotenv()
base_name = os.getenv('BASE_NAME')
base_name = 'yamen_ob_2.db'

tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
screenshot_path = 'C:\\Python projects\\Screenshort\\'
logging.basicConfig(filename='log_file.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('This is a log massage.')


def not_readed_files_in_base():
    with sq.connect(base_name) as con:  # Проверяем количество доступных для расшифровки файлов
        cursor = con.cursor()
        cursor.execute("SELECT COUNT (readed) FROM Screen WHERE readed = '0' AND usable = '1'")
        count = cursor.fetchone()
        count_files = count[0]
        checkwell()
        print(f'Всего файлов пригодных для расшифровки в базе - {count_files}')
        return count_files


class ScreenRead:
    def __int__(self):
        self.screen_id = ''
        self.name = ''
        self.usable = 1
        self.readed = 0
        self.error_log = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Сохраняем код ошибки при заспознавании данных
        """ Разряды лога 
                    0 - версия парсера
                    1 - activ
                    2 - rait
                    3 - grate
                    4 - all_profit
                    5 - cash_profit
                    6 - card_profit
                    7 - orders
                    8 - commission
                    9 - balance
                    10 - error function getFloat 
                    11 - tips 
                    """

    # Отбираем подходящие файлы для сканирования и складываем их имена в базу
    def find_new_files(self):
        count = 0
        for adress, dirs, files in os.walk(
                screenshot_path):
            print(f'В указанной папаке найдено файлов - {len(files)} \nПроверяем файлы и добавляем новые в базу ...')
            for file in tqdm(files):
                screen.name = ("'" + file + "'")
                with sq.connect(base_name) as con:
                    cursor = con.cursor()
                    cursor.execute(f"SELECT name FROM Screen WHERE  name = {screen.name}")
                    if cursor.fetchone() is None:
                        if 'yandex.taximeter' in screen.name:
                            cursor = con.cursor()
                            cursor.execute(
                                f"INSERT INTO Screen VALUES(null, {screen.name}, 1, 0, "
                                f"null, null)")
                            count += 1
        print(f'... найдено подходящих для дальнейшей работы и добавленно в базу - {count} файлов \n')


class Fields(ScreenRead):
    def __init__(self):
        super().__int__()
        self.id = 0  # 1
        self.date = 'null'  # 2
        self.time = 'null'  # 3
        self.date_time = 'null'  # 4
        self.activ = 0  # 5
        self.rait = 0  # 6
        self.grate = 0  # 7
        self.all_profit = 0.0  # 8
        self.cash_profit = 0.0  # 9
        self.card_profit = 0.0  # 10
        self.orders = 0  # 11
        self.commission = 0.0  # 12
        self.balance = 0.0  # 13
        self.tips = 0.0  # 14
        self.name = ""  # 15
        self.verified = False  # 16

    def readImagetoText(self):
        """ Переводит картинку в строку текста"""
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        fileneme = fields.name.replace("'", '')
        screenshotname = screenshot_path + fileneme
        image = cv2.imread(screenshotname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        config = r'--oem 3 --psm 6'
        string = pytesseract.image_to_string(gray, lang='rus', config=config)
        return string

    def name_to_date(self):
        """ Из имени файла достаем дату """
        datetime_str = fields.name.split('_')
        datetimeplus = datetime_str[1]
        datetime_split = datetimeplus.split('-')
        datetime_split.pop(-1)
        date_time_str = ' '.join(datetime_split)
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
        return date_time_obj

    def make_null_fields(self):
        fields.activ = 0.0
        fields.rait = 0.0
        fields.grate = 0
        fields.all_profit = 0.0
        fields.cash_profit = 0.0
        fields.card_profit = 0.0
        fields.orders = 0
        fields.commission = 0
        fields.balance = 0.0
        fields.tips = 0.0

    def getNewFile(self):
        with sq.connect(base_name) as con:  # Расшифровываем и раскладываем по полям базы
            cursor = con.cursor()
            cursor.execute(
                "SELECT id, name FROM Screen WHERE readed = '0' AND usable = '1' LIMIT 1")  # Получаем первую запись из базы
            fields.error_log = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            getfilename = cursor.fetchone()
            fields.name = getfilename[1]
            screen.screen_id = getfilename[0]
            string = Fields.readImagetoText(fields)
            print(string)
            # bed_word = (">", "?", "'", "›", "‹", "<", "‹", "/n")
            # for one_piece in bed_word:
            #     stringforbase = string.replace(one_piece, '')
            #
            #
            #
            #
            #
            stringforbase = string.replace('?', ' ')  # Готовим строку без лишних символов
            stringforbase = stringforbase.replace("'", ' ')
            stringforbase = "'" + stringforbase + "'"
            cursor.execute(f"UPDATE Screen SET strline = {stringforbase}  WHERE id = {screen.screen_id}")
            string_split = string.split()
            # print(string_split)
            return string_split

createNewBase()
screen = ScreenRead()

ScreenRead.find_new_files(screen)

notReadedFilesInBase_count = not_readed_files_in_base()

# listNotParsFile = []

fields = Fields()

question = 0

if notReadedFilesInBase_count > 0:
    try:
        question = int(input('Сколько файлов расшифровать? - '))
    except ValueError:
        print('... ввод не корректен,\nКонец ')
        quit()

    if question == 0:
        quit()

    if question <= notReadedFilesInBase_count:

        # tqdm
        for i in tqdm(range(question)):
            Fields.make_null_fields(fields)  # Сбрасываем значение полей на ноль
            string_split = Fields.getNewFile(fields)  # Выбираем файл для расшифровки, и переводим его в сплит строку

            datetime_obj = Fields.name_to_date(fields.name)  # выделяем дату и время из имени
            fields.date_time = datetime_obj
            fields.date = str(datetime_obj.date())
            fields.time = str(datetime_obj.time())

            # Расшифровываем и раскладываем по полям
            if '2021-07-01' < fields.date < '2022-04-04':
                # print(1)
                readTextToFields(fields, string_split)
            if '2022-04-03' < fields.date < '2023-04-08':
                # print(2)
                readTextToFields2(fields, string_split)
            if '2023-04-07' < fields.date:
                # print(3)
                readTextToFields3(fields, string_split)

            # форматируем данные для базы
            error_log_dump = json.dumps(fields.error_log)
            error_log_dump = "'" + error_log_dump + "'"

            # пишем поля в базу
            with sq.connect(base_name) as con:
                cursor = con.cursor()
                cursor.execute(f"UPDATE Screen SET errors_log = {error_log_dump}  WHERE id = {screen.screen_id}")
                fields.name = ("'" + fields.name + "'")

                # если данные не найдены пишем в базу '0'
                if fields.all_profit + fields.cash_profit + fields.card_profit < 1:
                    cursor.execute(
                        f"UPDATE Screen SET usable = 0  WHERE name = {fields.name}")
                else:
                    list_filds = [fields.date, fields.time, fields.date_time, fields.activ, fields.rait, fields.grate,
                                  fields.all_profit, fields.cash_profit, fields.card_profit,
                                  fields.orders, fields.commission, fields.balance, fields.tips,
                                  str(fields.name), fields.verified]
                    cursor.execute("INSERT INTO Fields VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   list_filds)
                    fields.name = fields.name.replace("'", "")
                    cursor.execute('UPDATE Screen SET readed = ? WHERE name = ?', (True, fields.name))

print(f'Готово! \n ')

# not_readed_files_in_base()
# checkwell()
#
# question = input('Проверить базу на наличие задвоенных данных и сформировать окончательную таблицу (д\y - да) - ')
# if question == 'y' or question == 'д':
#     checkduble()
