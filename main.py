import os
import re

import pandas as pd
from tabulate import tabulate

from PhoneBook import Color as C
from PhoneBook import PhoneBook


def start_input_checks(mode: str, ii: str = None, _s: str = None, _n: str = None, _pn: str = None, _bd: str = None,
                       surname: str = None, name: str = None, arr_phone: list = None, b_day: str = None):
    """
    Contains infinite loops to give user chance to input correct values.
    :param mode: depends on a func, which is called
    :param ii: incorrect input message
    :param _s: surname helping message
    :param _n: name helping message
    :param _pn: phone number helping message
    :param _bd: b-day helping message
    :return:  correct values (surname/ name/ arr_phone/ b_day:)
    """
    mobile_phone = ''
    work_phone = ''
    home_phone = ''

    if mode == 'add' or mode == 'change':
        while True:
            s, n, arr_pn, bd = check_correct_input(mode=mode, surname=surname, name=name, arr_phone=arr_phone,
                                                   b_day=b_day)
            if s and n and all(arr_pn) and bd:
                break
            else:
                print(ii)
                if not s:
                    surname = input(f'{_s}>> ').capitalize().strip()
                if not n:
                    name = input(f'{_n}>> ').capitalize().strip()
                if not all(arr_pn):  # check if all vals in arr are true
                    if len(arr_pn) > 1:
                        print('Example: 89XXXXXXXXX or - ')
                        if not arr_pn[0]:
                            mobile_phone = 'M ' + input(f'MOBILE phone: ').replace('+7', '8').strip()
                        if not arr_pn[1]:
                            work_phone = 'W' + input(f'WORK phone: ').replace('+7', '8').strip()
                        if not arr_pn[2]:
                            home_phone = 'H' + input(f'HOME phone: ').replace('+7', '8').strip()
                        arr_phone.clear()
                        arr_phone.extend([mobile_phone, work_phone, home_phone])
                    else:
                        phone_number = input(f'{_pn}>> ').replace('+7', '8').strip()
                        arr_phone.clear()
                        arr_phone.append(phone_number)

                if not bd:
                    b_day = input(f'{_bd}B-day: ').strip()
                    if b_day == '':
                        b_day = '-'
                    b_day = standardize_bday(b_day)
        return surname, name, arr_phone, b_day
    elif mode.split(' ')[0] == 'del' or mode == 'get_age':
        if mode == 'get_age' or mode.split(' ')[1] == '1':
            while True:
                s, n = check_correct_input(mode=mode, surname=surname, name=name)
                if s and n:
                    break
                else:
                    print(ii)
                    if not s:
                        surname = input(f'{_s}>> ').capitalize().strip()
                    if not n:
                        name = input(f'{_n}>> ').capitalize().strip()
            return surname, name
        elif mode.split(' ')[1] == '2':
            while True:
                arr_pn = check_correct_input(mode=mode, arr_phone=arr_phone)
                if all(arr_pn):
                    break
                else:
                    print(ii)
                    if not all(arr_pn):
                        phone_number = input(f'{_pn}>> ').replace('+7', '8').strip()
                        arr_phone.clear()
                        arr_phone.append(phone_number)
            return arr_phone[0]


def check_number(arr_phone: list, mode: str = None) -> list:
    """
    Additional func, checks correct input of phone
    :param arr_phone: it can be one or several phones (mobile/home/work)
    :param mode: in SEARCH & CHANGE funcs number can be skip and put "-"
    :return: array of boolean values
    """
    arr_pn = list()

    if len(arr_phone) == 1:  # 1 number
        split_num = arr_phone[0].split(' ')
        if len(split_num) == 1 and mode != 'search' and mode != 'change':
            print(f'{C.WARNING}>> Your input: {split_num[0]}.{C.ENDC}')
            return [False]
        else:
            if re.search(r'-', split_num[0]):
                return [True]
        if not re.search(r'[MWHmwh]', (arr_phone[0].split(' '))[0]):
            return [False]
        if (arr_phone[0].split(' '))[1] == '-':  # only 1 number can't be "-"
            print(f"{C.WARNING}>> !!! {(arr_phone[0].split(' '))[0]} phone CAN'T be '-' !!!\n{C.ENDC}")
            return [False]
        if re.search(r'\+[0-689][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', split_num[0]):
            return [False]

    pn = True
    for phone in arr_phone:  # 3 numbers
        mode_phone = phone.split(' ')
        if len(mode_phone) == 1:
            return [False]
        if mode_phone[1] == '-':
            pn = True
            arr_pn.append(pn)
            continue
        if not re.search(r'[MWHmwh]', mode_phone[0]):
            pn = False
        if len(mode_phone[1]) != 11:
            pn = False
        if re.search(r'\+[0-689][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', mode_phone[1]):
            pn = False
        arr_pn.append(pn)
    return arr_pn


def standardize_bday(b_day: str) -> str:
    """
    If user enter: 1.12.2000 (01.12.2000 is correct) or 1.3.2001 (01.03.2001 is correct)
    :param b_day: input b-day
    :return: correct b-day
    """
    if b_day != '-':
        date = b_day.split('.')
        day = date[0]
        month = date[1]
        year = date[2]
        if len(day) == 1 and day != '-':
            day = '0' + day
        if day != '-' and len(month) == 1:
            month = '0' + month
        return day + '.' + month + '.' + year
    else:
        return b_day


def check_correct_input(mode: str, surname: str = None, name: str = None, arr_phone: list = None, b_day: str = None):
    """
    Additional func, checks correct input of all params
    :param mode: depends on a func, which is called
    :return:  array of boolean values 
    """""
    if mode == 'add':
        s = re.search(r'[A-Z][A-Za-z0-9 ]*', surname)
        n = re.search(r'[A-Z][A-Za-z0-9 ]*', name)

        arr_pn = check_number(arr_phone)

        bd = re.search(r'[0-9][0-9]\.[0-9][0-9]\.[1-9][0-9][0-9][0-9]', b_day) or re.search(r'-', b_day)
        return s, n, arr_pn, bd

    elif mode == 'search' or mode == 'change':
        s = re.search(r'[A-Z\-][A-Za-z0-9 ]*', surname)
        n = re.search(r'[A-Z\-][A-Za-z0-9 ]*', name)

        arr_pn = check_number(arr_phone, mode)

        bd = re.search(r'[0-9][0-9]\.[0-9][0-9]\.[1-9][0-9][0-9][0-9]', b_day) or re.search(r'-', b_day) or re.search(
            r'[0-9][0-9]*', b_day)
        return s, n, arr_pn, bd

    elif mode.split(' ')[0] == 'del':
        if mode.split(' ')[1] == '1':
            s = re.search(r'[A-Z][A-Za-z0-9 ]*', surname)
            n = re.search(r'[A-Z][A-Za-z0-9 ]*', name)
            return s, n
        elif mode.split(' ')[1] == '2':
            arr_pn = check_number(arr_phone)
            return arr_pn
    elif mode == 'get_age':
        s = re.search(r'[A-Z][A-Za-z0-9 ]*', surname)
        n = re.search(r'[A-Z][A-Za-z0-9 ]*', name)
        return s, n


def check_empty(df, helping_message2: str) -> bool:
    """
    Checks if Phone Book is empty.
    :param df: pandas DataFrame (contains Phone Book)
    :param helping_message2: list of available funcs
    :return: true-empty
    """
    if df.empty:
        print(helping_message2)
        return True
    else:
        return False


def main():
    #### HELPING MESSAGES ####
    helping_message = f'''{C.HEADER}                                  *** A Phone Book usage instruction ***{C.ENDC}
                   {C.MENU}>> /show_all   Shows all notes from the phone book.
                   >> /search     Search in the phone book by a particular field of fields.
                   >> /add_note   Add a new note to the phone book.
                   >> /del_note   Deleting an entry from the directory by first and last name or by phone number.
                   >> /change_field   Change any field or fields(surname, name...) in a specific directory entry.
                   >> /get_age        Shows the age of a particular person.
                   >> /show_bday_boy  Shows all people who have a birthday in the next 30 days. 
                   >> /quit           Leave the phone book.
                   >> /help           Show helping message.{C.ENDC}'''

    helping_message2 = f'''{C.HEADER}             !!! This Phone Book is empty !!!
    {C.WARNING}*{C.ENDC} {C.MENU}Now you can use just "/add_note" and "/quit" functions.
        >> /add_note   Add a new note to the phone book.
        >> /quit       Leave the phone book.{C.ENDC}'''

    hm = f'see {C.MENU}/help{C.ENDC} for assistance.'

    continue_info = f'\n>> Enter any command or {hm}'

    incorrect_input = f'{C.WARNING}>> *** INCORRECT INPUT! ***\n{C.ENDC}'

    _surname = f'>> Enter {C.RULES}surname{C.ENDC} ({C.WARNING}*{C.ENDC} ONLY: latin letters, numbers and ' \
               f'spaces)\nExamples: Ivanov, Ivanov15 or Bulwer Lytton. \n '
    _name = f'>> Enter {C.RULES}name{C.ENDC} ({C.WARNING}*{C.ENDC} ONLY latin letters, numbers and spaces)\nExamples: ' \
            f'Ivan, Liya15 or Anna Sofia). \n '

    _phone_number = f'>> Enter {C.RULES}phone number{C.ENDC} (ONLY 11 numbers!)\nTo work with MOBILE phone, enter: ' \
                    f'{C.RULES}M{C.ENDC} 89XXXXXXXXX\nTo work with WORK phone, enter: {C.RULES}W{C.ENDC} ' \
                    f'89XXXXXXXXX\nTo work with HOME phone, enter: {C.RULES}H{C.ENDC} 89XXXXXXXXX\nTo work with ' \
                    f'SEVERAL numbers, enter {C.RULES}S{C.ENDC} and fill in open fields:\n' \
                    f'{C.RULES}S (+enter){C.ENDC} -> then enter {C.RULES}89XXXXXXXXX{C.ENDC} to the open gaps or {C.RULES}"-"{C.ENDC} to skip.\n '

    _b_day = f'>> Enter {C.RULES}b-day{C.ENDC}: (DAY.MONTH.YEAR) -> 01.05.2001  OR "-" to skip.\n'
    ##################################################################################################

    ##### FILES WORK ####
    file_name = 'phone_book.csv'
    f = os.path.abspath(file_name)
    df = pd.read_csv(f)
    ########################################

    if not check_empty(df, helping_message2):
        print(helping_message)
    user_data = ''

    df.set_index(['surname', 'name'], inplace=True)  # make name & surname as index

    pb = PhoneBook(df, file_name)

    ### THE MAIN WORK(loop) #####
    while True:
        if user_data == '/CHANGE':  # to change an existing note (after trying to add)
            user_data = '/change_field'
        else:
            user_data = input('>> ').strip()

        if user_data == '/help':  # HELP
            if not check_empty(pb.data, helping_message2):
                print(helping_message)
            continue
        ###########################################################################################################
        elif user_data == '/show_all':  # SHOW ALL
            pb.show_all_notes()
            print(continue_info)
            continue
        ###########################################################################################################
        elif user_data == '/search':  # SEARCH
            if check_empty(pb.data, helping_message2):
                print(continue_info)
                continue
            else:
                search_info = '>> Search by: "SURNAME" - "NAME" - "PHONE NUMBER(mobile, work, home)" - ' \
                              f'"B-DAY".\nIf you {C.RULES}DO NOT{C.ENDC} want to search by some of fields, put, pls: ' \
                              f'- .\n '
                print(search_info)

                _surname1 = f'>> Enter {C.RULES}full surname{C.ENDC} OR just the {C.RULES}1st letter{C.ENDC} OR' \
                            f' {C.RULES}-{C.ENDC} .\nExamples: Ivanov15, A or - .\n'
                _name1 = f'>> Enter {C.RULES}full name{C.ENDC} OR just the {C.RULES}1st letter{C.ENDC} OR ' \
                         f'{C.RULES}-{C.ENDC} .\nExamples: Ivan, L or -).\n'
                _phone_number1 = f'>> Enter {C.RULES}phone number{C.ENDC} (ONLY 11 numbers!):\nTo search by MOBILE ' \
                                 f'phone, enter: {C.RULES}M{C.ENDC} 89XXXXXXXXX\nTo search by WORK phone, enter: ' \
                                 f'{C.RULES}W{C.ENDC} 89XXXXXXXXX\nTo search by HOME phone, enter: ' \
                                 f'{C.RULES}H{C.ENDC} 89XXXXXXXXX\nOR "-" to skip'
                _b_day1 = f'>> Enter {C.RULES}full b-day{C.ENDC} OR just {C.RULES}a day{C.ENDC}: (DAY.MONTH.YEAR) -> ' \
                          f'01.05.2001  OR "-" to skip.\n '

                surname = input(f'{_surname1}>> ').capitalize().strip()
                name = input(f'{_name1}>> ').capitalize().strip()
                phone_number = input(f'{_phone_number1}>> ').replace('+7', '8').strip()
                arr_phone = [phone_number]
                b_day = input(f'{_b_day1}>> ').strip()
                if b_day == '':
                    b_day = '-'
                b_day = standardize_bday(b_day)

                mode = 'search'
                Flag = True
                while True:
                    s, n, arr_pn, bd = check_correct_input(mode, surname, name, arr_phone, b_day)
                    if surname == name == phone_number == b_day == '-':
                        print(f"{C.WARNING}You entered ALL '-'.\n{C.ENDC}")
                        Flag = False
                        break
                    elif s and n and all(arr_pn) and bd:
                        break
                    else:
                        print(incorrect_input)
                        if not s:
                            surname = input(f'{_surname1}>> ').capitalize().strip()
                        if not n:
                            name = input(f'{_name1}>> ').capitalize().strip()
                        if not all(arr_pn):
                            phone_number = input(f'{_phone_number1}>> ').replace('+7', '8').strip()
                            arr_phone.clear()
                            arr_phone.append(phone_number)
                        if not bd:
                            b_day = input(f'{_b_day1}>> ').strip()
                            if b_day == '':
                                b_day = '-'
                            b_day = standardize_bday(b_day)

                if Flag:
                    search_rez = pb.to_search(surname, name, phone_number, b_day)
                    print(tabulate(search_rez, tablefmt='fancy_grid'))
                print(f'\n>> Enter {C.MENU}/search{C.ENDC} again or', hm)
                continue
        ###########################################################################################################
        elif user_data == '/add_note':  # ADD NOTE
            add_info = '>> To ADD the Note, fill in the next fields, pls.'
            print(add_info)

            surname = input(f'{_surname}>> ').capitalize().strip()
            name = input(f'{_name}>> ').capitalize().strip()

            arr_phone = list()
            mobile_phone = ''
            work_phone = ''
            home_phone = ''
            phone_number = input(f'{_phone_number}>> ').replace('+7', '8').strip()
            if re.search(r'[Ss]', phone_number):
                Flag = True
                while Flag:
                    print('Example: 89XXXXXXXXX or "-" to skip')
                    mobile_phone = 'M ' + input(f'MOBILE phone: ').replace('+7', '8').strip()
                    work_phone = 'W ' + input(f'WORK phone: ').replace('+7', '8').strip()
                    home_phone = 'H ' + input(f'HOME phone: ').replace('+7', '8').strip()
                    if mobile_phone.split(' ')[1] == work_phone.split(' ')[1] == home_phone.split(' ')[1] == '-':
                        print(
                            f"{C.WARNING}>> !!! You entered ALL '-'.\n   Pls, enter MOBILE/WORK/HOME phone number.\n{C.ENDC}")
                    else:
                        Flag = False

                arr_phone.extend([mobile_phone, work_phone, home_phone])
            else:
                arr_phone.append(phone_number)

            b_day = input(f'{_b_day}>> ').strip()
            if b_day == '':
                b_day = '-'
            b_day = standardize_bday(b_day)

            mode = 'add'
            # start input checks
            surname, name, arr_phone, b_day = start_input_checks(mode=mode, ii=incorrect_input, _s=_surname, _n=_name,
                                                                 _pn=_phone_number,
                                                                 _bd=_b_day, surname=surname, name=name,
                                                                 arr_phone=arr_phone, b_day=b_day)

            hp_msg = f'{C.WARNING}This entry: {surname} {name} already exists in the phone book.\nYou can ' \
                     'change it or go back to the menu and enter another' \
                     f' command.{C.ENDC}\n'
            hp_msg2 = f'Enter {C.MENU}/change_field{C.ENDC} or {C.MENU}/return.{C.ENDC}\n'

            rez = pb.add_note(surname, name, arr_phone, b_day)  # func call
            if rez == 'exist':
                print(hp_msg, hp_msg2)
                user_data = input('>> ')
                while True:
                    if user_data == '/change_field':
                        user_data = '/CHANGE'
                        break
                    elif user_data == '/return':
                        print(continue_info)
                        break
                    else:  # if input smth wrong
                        print(f'{C.WARNING}Incorrect input!{C.ENDC}\n', hp_msg2)
                        user_data = input()
                continue
            else:
                print(continue_info)
                continue
        ###########################################################################################################
        elif user_data == '/del_note':  # DELETE NOTE
            if check_empty(pb.data, helping_message2):
                print(continue_info)
                user_data = input('>> ').strip()
            else:
                del_info = f'>> To {C.RULES}DELETE{C.ENDC} the Note, fill in the next fields, pls.\n' \
                           f'Delete by {C.RULES}SURNAME{C.ENDC} and {C.RULES}NAME{C.ENDC}, ' \
                           f'enter {C.RULES}"1"{C.ENDC}.\nDelete by {C.RULES}PHONE NUMBER{C.ENDC}, enter {C.RULES}"2"{C.ENDC}.\n'
                print(del_info)

                _phone_number2 = f'>> Enter {C.RULES}phone number{C.ENDC} (ONLY 11 numbers!)\nTo work with MOBILE phone, enter: ' \
                                 f'{C.RULES}M{C.ENDC} 89XXXXXXXXX\nTo work with WORK phone, enter: {C.RULES}W{C.ENDC} ' \
                                 f'89XXXXXXXXX\nTo work with HOME phone, enter: {C.RULES}H{C.ENDC} 89XXXXXXXXX\n'

                mode_del = input('1 or 2: >> ').strip()
                Flag = True
                while Flag:
                    if mode_del != '1' and mode_del != '2':
                        mode_del = input('1 or 2: >> ')
                    else:
                        Flag = False

                surname = None
                name = None
                phone_number = None
                mode = 'del'
                flag_exist = True
                if mode_del == '1':
                    surname = input(f'{_surname}>> ').capitalize().strip()
                    name = input(f'{_name}>> ').capitalize().strip()
                    mode_del = 'sn'
                    mode += ' 1'
                    surname, name = start_input_checks(mode, ii=incorrect_input, _s=_surname, _n=_name,
                                                       surname=surname, name=name)

                    existence = pb.to_search(surname, name, '-', '-')
                    if str(existence) == 'No such note.':  # if such note exist
                        flag_exist = False

                elif mode_del == '2':
                    phone_number = input(f'{_phone_number2}>> ').replace('+7', '8').strip()
                    arr_phone = [phone_number]
                    mode_del = 'num'
                    mode += ' 2'
                    phone_number = start_input_checks(mode, ii=incorrect_input, _pn=_phone_number2, arr_phone=arr_phone)

                    existence = pb.to_search('-', '-', phone_number, '-')
                    if str(existence) == 'No such note.':  # if such note exist
                        flag_exist = False

                if flag_exist:
                    pb.del_note(mode_del, surname, name, phone_number)
                    print(continue_info)
                    continue
                else:
                    print(f'{C.WARNING}No note with such data!{C.ENDC}')
                    print(continue_info)
                    continue
        ###########################################################################################################
        elif user_data == '/change_field':  # CHANGE FIELD
            if check_empty(pb.data, helping_message2):
                print(continue_info)
                continue
            else:
                change_info = '>> To CHANGE the Note, 1st of all, enter, pls, SURNAME and NAME.'
                print(change_info)

                surname = input(f'{_surname}\nOld surname: >> ').capitalize().strip()
                name = input(f'{_name}\nOld name: >> ').capitalize().strip()
                orig_surname = surname
                orig_name = name

                if pb.data.index.isin([(surname, name)]).any():  # if such person exists
                    print(f">> Enter, pls, a {C.RULES}NEW VALUE{C.ENDC} to the next fields, if u want to change them\n"
                          f"OR {C.RULES}'-'{C.ENDC} , if u {C.RULES}DON'T{C.ENDC} want to change them.")
                    surname = input(f'{_surname}\nNew surname or -: >> ').capitalize().strip()
                    name = input(f'{_name}\nNew name or -: >> ').capitalize().strip()
                    if pb.data.index.isin([(surname, name)]).any():
                        print(f'{C.WARNING}You try to change {C.ENDC}{orig_surname} {orig_name}{C.ENDC} {C.WARNING}to'
                              f' {C.ENDC}{surname} {name}{C.ENDC}{C.WARNING}.\n'
                              f'HOWEVER, {C.ENDC}{surname} {name}{C.ENDC}{C.WARNING} already exists!!!{C.ENDC}\n')
                        print(continue_info)
                        continue
                    else:
                        arr_phone = list()
                        mobile_phone = ''
                        work_phone = ''
                        home_phone = ''
                        phone_number = input(f'{_phone_number}\nNew number or S or -: >> ').replace('+7', '8').strip()
                        if re.search(r'[Ss]', phone_number):
                            Flag = True
                            while Flag:
                                print('Example: 89XXXXXXXXX or "-" to skip')
                                mobile_phone = 'M ' + input(f'MOBILE phone: ').replace('+7', '8').strip()
                                work_phone = 'W ' + input(f'WORK phone: ').replace('+7', '8').strip()
                                home_phone = 'H ' + input(f'HOME phone: ').replace('+7', '8').strip()
                                if mobile_phone.split(' ')[1] == work_phone.split(' ')[1] == home_phone.split(' ')[
                                    1] == '-':
                                    print(f"{C.WARNING}>> !!! You entered ALL '-'.\n   Pls, enter some phone number("
                                          f"MOBILE/WORK/HOME).{C.ENDC}\n")
                                else:
                                    Flag = False

                            arr_phone.extend([mobile_phone, work_phone, home_phone])
                        else:
                            arr_phone.append(phone_number)

                        b_day = input(f'{_b_day}\nNew b-day or -: >> ').strip()
                        if b_day == '':
                            b_day = '-'
                        b_day = standardize_bday(b_day)

                        mode = 'change'
                        _surname += 'New surname or -: >> '
                        _name += 'New name or -: >> '
                        _phone_number += 'New number or -: >> '
                        _b_day += 'New b-day or -: >> '
                        # start input checks
                        surname, name, arr_phone, b_day = start_input_checks(mode=mode, ii=incorrect_input, _s=_surname,
                                                                             _n=_name,
                                                                             _pn=_phone_number,
                                                                             _bd=_b_day, surname=surname, name=name,
                                                                             arr_phone=arr_phone, b_day=b_day)

                        pb.change_field(orig_surname, orig_name, surname, name, arr_phone, b_day)
                        print(continue_info)
                        continue
                else:
                    print(f"{C.WARNING}\n>> Such person ({surname} {name}) doesn't exist!{C.ENDC}")
                    print(continue_info)
                    continue
        ###########################################################################################################
        elif user_data == '/get_age':  # GET AGE
            if check_empty(pb.data, helping_message2):
                print(continue_info)
                continue
            else:
                get_age_info = '>> To GET AGE of a person, fill in the next fields, pls.'
                print(get_age_info)

                surname = input(f'{_surname}>> ').capitalize().strip()
                name = input(f'{_name}>> ').capitalize().strip()

                mode = 'get_age'

                surname, name = start_input_checks(mode, ii=incorrect_input, _s=_surname, _n=_name,
                                                   surname=surname, name=name)

                pb.get_age(surname, name)
                print(continue_info)
                continue
        ###########################################################################################################
        elif user_data == '/show_bday_boy':  # SHOW B-DAY BOY
            people = pb.show_bday_boy()
            for num, person in enumerate(people, start=1):
                print(num, '. ', person)
            print(continue_info)
            continue
        ###########################################################################################################
        elif user_data == '/quit':  # QUIT
            print(f'{C.HEADER}*** GOOD BYE! ***{C.ENDC}')
            break
        ###########################################################################################################
        else:  # if u enter wrong requirement
            print(f"{C.WARNING}*** There's NO such option! ***\n{C.ENDC}")
            print(continue_info)
            continue


if __name__ == '__main__':
    main()
