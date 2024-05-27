from pprint import pprint
from typing import List, Union, NoReturn, AnyStr
import re, csv

def read_contacts_book(file_name: AnyStr) -> List:
    """
    читаем адресную книгу в формате CSV в список contacts_list
    :param file_name: имя CSV-файла
    :return: список контактов
    """
    with open(file_name, encoding="utf-8") as f:
      rows = csv.reader(f, delimiter=",")
      contacts_list = list(rows)
    return contacts_list

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

def get_parsed_contacts(data: List) -> List:
    """
    разделение контактной информации средствами регулярных выражений
    :param data: считанные контактные данные
    :return: упорядоченные контактные данные
    """
    symbol_separator = ';'
    exploresd_string = ''
    for data_unit in data:
        exploresd_string += ','.join(data_unit) + '\n'

    template = r"^(?P<last_name>[А-ЯЁ][а-яё]*).*?(?P<first_name>[А-ЯЁ][а-яё]*)[\W\s]*([А-ЯЁ][а-яё]+)?[\W\s]*(ФНС|Минфин)?"\
               "\W([–\А-ЯЁа-яёAETOPAHKXCMeyopkc\s-]*)?"\
               "\W(?:(\+7|8)-?\s*-?\(?(\d{3,})\)?[\s*-]?(\d+)[\s-]?(\d{2})[\s-]?(\d{2})[\s-]?[\W\s]*?\(?(?:доб[\.]?\s*)?(\d+)?\)?)?"\
               "[\W*\s*]([-\w@\.]*)?.*$"

    pattern = re.compile(template, re.M)
    parsed_text_list = pattern.findall(exploresd_string)
    return parsed_text_list

def same_info_unit(record_1: List, record_2: List, index: int) -> bool:
    """
    сравнение двух записей контактной информации на идентичность информационного поля, определяемого параметром index
    :param record_1:
    :param record_2:
    :param index: индекс сравниваемых полей
    :return: true/false если поля идентичны/отличаются
    """
    result = False
    if record_1[index] and record_2[index]:
        result = True if record_1[index] == record_2[index] else False
    else:
        result = True
    return result

def search_same_person(book: List, target_record: List) -> int:
    """
    поиск в телефонной книге абонента с контактной информацией, идентичной текущей записи
    :param book: телефонная книга
    :param target_record: текущая запись
    :return: индекс найденной записи ( -1: если запись не найдена)
    """
    result = -1
    for i, record in enumerate(book):
        if record[0] == target_record[0] and record[1] == target_record[1]:
            if (same_info_unit(record, target_record, 2) and
                    same_info_unit(record, target_record, 5) and
                    same_info_unit(record, target_record, 6)):
                result = i
                break
    return result

def fillup_phone_book(header: List, parsed_data: List) -> List:
    """
    заполнение адресной книги корректными данными
    :param header: имена полей структуры
    :param parsed_data: список отпарсенных данных
    :return: список адресной книги
    """
    phone_book = []
    phone_book.append(header)

    for row_tuple in parsed_data:
        phone_record = []
        phone_record.append(row_tuple[0]) # фамилия
        phone_record.append(row_tuple[1]) # имя
        phone_record.append(row_tuple[2]) # отчество
        phone_record.append(row_tuple[3]) # организация
        phone_record.append(row_tuple[4]) # должность
        phone_record.append('+7(' + row_tuple[6] + ')' + # номер телефона
                            row_tuple[7] + '-' + row_tuple[8] + '-' + row_tuple[9] +
                            (' доб.' + row_tuple[10] if row_tuple[10] else '') if row_tuple[6] and row_tuple[7] and row_tuple[8] and row_tuple[9] else ''
                            )
        phone_record.append(row_tuple[11]) # электронный адрес
        record_index = search_same_person(phone_book, phone_record)
        if record_index < 0:
            phone_book.append(phone_record)
        else:
            for i in range(len(phone_book[record_index])):
                if not phone_book[record_index][i] and phone_record[i]:
                    phone_book[record_index][i] = phone_record[i]

    return phone_book

def get_correct_data() -> List:
    """
    упорядочиваем данные согласно заданной структуре:
    lastname,firstname,surname,organization,position,phone,email

    :return: список контктов согласно заданной структуре
    """
    raw_data = read_contacts_book("phonebook_raw.csv")
    header_list = raw_data.pop(0)
    parsed_contacts_list = get_parsed_contacts(raw_data)
    ordered_data_list = fillup_phone_book(header_list, parsed_contacts_list)
    return ordered_data_list

# TODO 2: сохраните получившиеся данные в другой файл
def save_correct_data(file_name: AnyStr, correct_data: List) -> NoReturn:
    """
    код для записи файла в формате CSV
    :param file_name: имя CSV-файла
    :param correct_data: список контктов согласно заданной структуре
    :return: None
    """
    with open(file_name, "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(correct_data)


if __name__ == "__main__":
    save_correct_data("phonebook.csv", get_correct_data())
