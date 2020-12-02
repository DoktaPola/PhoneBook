import datetime
import re

import pandas as pd
from tabulate import tabulate


# COLOR SETTINGS
class Color:
    WARNING = '\033[95m'
    HEADER = '\033[93m'
    MENU = '\033[92m'
    RULES = '\033[94m'
    ENDC = '\033[0m'


class PhoneBook:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name

    def show_all_notes(self):
        """
        Shows all notes from the phone book.
        :return:
        """
        h = [self.data.index.names[0] + '/' + self.data.index.names[1]] + list(self.data.columns)
        print(tabulate(self.data, headers=h, tablefmt='fancy_grid'))

    def _check_data_search(self, dict1: dict, d):
        """
        Additional func, find data by pandas.loc
        :param dict1: saves values
        :param d:
        :return:
        """
        key, val = dict1.popitem()
        if (key == 'surname') and (len(val) == 1):  # surname by 1st letter
            data1 = d.loc[(d.index.get_level_values(key).str.startswith(val))]
        elif (key == 'name') and (len(val) == 1):  # name by 1st letter
            data1 = d.loc[(d.index.get_level_values(key).str.startswith(val))]
        elif (key == 'b_day') and (len(val) == 2):  # b_day by day
            data1 = d.loc[(d.b_day.str.startswith(val))]
        else:
            data1 = d.query(f"{key} == '{val}'")
        return data1

    def to_search(self, surname: str, name: str, phone_number: str, b_day: str):
        """
        Search in the phone book by a particular field of fields.
        :return: searched data or notification
        """
        d = self.data
        dict1 = dict()

        if surname != '-':
            dict1['surname'] = surname
        if name != '-':
            dict1['name'] = name
        if phone_number != '-':
            if re.search(r'[Mm]', phone_number):
                dict1['mobile_number'] = phone_number.split(' ')[1]
            elif re.search(r'[Ww]', phone_number):
                dict1['work_number'] = phone_number.split(' ')[1]
            elif re.search(r'[Hh]', phone_number):
                dict1['home_number'] = phone_number.split(' ')[1]
        if b_day != '-':
            dict1['b_day'] = b_day

        data1 = self._check_data_search(dict1, d)

        if data1.empty:
            return 'No such note.'

        while dict1:
            if data1.empty:
                return 'No such note.'
            else:
                data1 = self._check_data_search(dict1, data1)
        return data1

    def add_note(self, surname: str, name: str, arr_phone: list, b_day: str):
        """
        Add a new note to the phone book.
        :return: nothing, just update csv file
        """
        if self.data.index.isin([(surname, name)]).any():  # check if such note exists
            return 'exist'
        else:
            mobile_number = '-'
            work_number = '-'
            home_number = '-'
            if len(arr_phone) > 1:
                if arr_phone[0] != '-':
                    mobile_number = (arr_phone[0].split(' '))[1]
                if arr_phone[1] != '-':
                    work_number = (arr_phone[1].split(' '))[1]
                if arr_phone[2] != '-':
                    home_number = (arr_phone[2].split(' '))[1]
                new_row = {'surname': [surname], 'name': [name], 'mobile_number': [mobile_number],
                           'work_number': [work_number], 'home_number': [home_number], 'b_day': [b_day]}
            else:
                if re.search(r'[Mm]', arr_phone[0]):
                    mobile_number = (arr_phone[0].split(' '))[1]
                elif re.search(r'[Ww]', arr_phone[0]):
                    work_number = (arr_phone[0].split(' '))[1]
                elif re.search(r'[Hh]', arr_phone[0]):
                    home_number = (arr_phone[0].split(' '))[1]
                new_row = {'surname': [surname], 'name': [name], 'mobile_number': [mobile_number],
                           'work_number': [work_number], 'home_number': [home_number], 'b_day': [b_day]}

            df2 = pd.DataFrame(data=new_row)
            df2.set_index(['surname', 'name'], inplace=True)  # make name & surname as index
            self.data = pd.concat([self.data, df2])
            self.data.to_csv(self.file_name)
            self.show_all_notes()  # show changes

    def _get_permission(self, data1):
        """
        Get person's permission to delete a note.
        :param data1: contains rows to delete
        :return: y/n (yes/no)
        """
        if str(data1) != 'No such note.':
            h = [self.data.index.names[0] + '/' + self.data.index.names[1]] + list(self.data.columns)
            out = tabulate(data1, headers=h, tablefmt='fancy_grid')
            del_info = f">> Do you want to {Color.RULES}DELETE{Color.ENDC}\n{out}\n{Color.RULES}y/n{Color.ENDC}? >> "
            permission = input(del_info)
        else:
            out = data1
            del_info = f">> Do you want to {Color.RULES}DELETE{Color.ENDC}\n{out}\n{Color.RULES}y/n{Color.ENDC}?\n" \
                       f"{Color.RULES}ENTER 'n'{Color.ENDC}. >> "
            permission = input(del_info)
        while True:  # check correct input
            if permission != 'y' and permission != 'n':
                permission = input(del_info)
            else:
                return permission

    def _get_bool(self, surname_name):
        output = ''
        Flag = False
        if surname_name.strip().find(' ') == -1:
            return False, output
        if surname_name.find(',') == -1:  # only one person
            surname_name = surname_name.split(' ')
            if len(surname_name) == 2:
                Flag = True
            name = surname_name[1].capitalize().strip()
            surname = surname_name[0].capitalize().strip()
            output = surname + ' ' + name
            return Flag, output
        else:
            people = surname_name.split(',')
            for person in people:
                person = person.strip().split(' ')
                if len(person) == 2:
                    Flag = True
                name = person[1].capitalize().strip()
                surname = person[0].capitalize().strip()
                output += surname + ' ' + name + ','
            output = output[:-1]
            return Flag, output

    def _del_checks(self, info: str, surname_name):
        while True:
            Flag, output = self._get_bool(surname_name)

            if Flag:
                break
            else:
                print(f"{Color.WARNING}Incorrect input!{Color.ENDC}")
                print(info)
                surname_name = input(f'>> ').capitalize().strip()
        return output

    def del_note(self, mode: str, surname: str = None, name: str = None, phone_num: str = None):
        """
        Deleting an entry from the directory by first and last name or by a number.
        :param mode: delete by first, last name OR by number
        :return: nothing, just update csv file
        """
        if mode == 'sn':  # del by surname and name
            self.data = self.data.drop((surname, name))
            self.data.to_csv(self.file_name)
        elif mode == 'num':  # del by phone number
            data1 = self.to_search('-', '-', phone_num, '-')
            if data1.shape[0] == 1:  # if found ONE note
                permission = self._get_permission(data1)
                if permission == 'y':
                    self.data = self.data.drop(data1.index)
                    self.data.to_csv(self.file_name)
                elif permission == 'n':
                    return
            else:  # if found MANY notes
                h = [self.data.index.names[0] + '/' + self.data.index.names[1]] + list(self.data.columns)
                print(tabulate(data1, headers=h, tablefmt='fancy_grid'))
                info = f'>> Enter {Color.RULES}SURNAME{Color.ENDC} and {Color.RULES}NAME {Color.ENDC} of chosen ' \
                       f'notes.\nExample:\n{Color.RULES}*{Color.ENDC} Panina Polina (1 note to delete)\n{Color.RULES}*{Color.ENDC} ' \
                       f'Panina Polina, Ozhiganova Marina, ...(2+ notes to delete {Color.WARNING}!!! separated by ' \
                       f'COMMA !!!{Color.ENDC}\n'
                info2 = f' Or enter {Color.RULES}"all"{Color.ENDC} to delete all chosen notes.\n'
                indexes_del = input(f"{info + info2}>> ")

                if re.search(r'[Aa][Ll][Ll]*', indexes_del):  # del all found notes
                    permission = self._get_permission(data1)
                    if permission == 'y':
                        indexes = data1.index.values
                        for ind in indexes:
                            self.data = self.data.drop((ind[0], ind[1]))  # del
                        self.data.to_csv(self.file_name)
                        print(f'>> {Color.RULES}Done.{Color.ENDC}\n')
                    elif permission == 'n':
                        return
                else:
                    indexes = self._del_checks(info, indexes_del)  # ПРОВЕРКИ НА ВВОД ИМЕН /////////////////////

                    indexes = indexes.split(',')
                    for index in indexes:
                        surname = index.split(' ')[0]
                        name = index.split(' ')[1]

                        info = self.to_search(surname, name, '-', '-')
                        permission = self._get_permission(info)

                        if permission == 'y':
                            self.data = self.data.drop((surname, name))  # del
                            print(f'>> {Color.RULES}Done.{Color.ENDC}\n')
                        elif permission == 'n':
                            continue
                    self.data.to_csv(self.file_name)

    def change_field(self, orig_surname: str, orig_name: str, surname: str, name: str, arr_phone: list, b_day: str):
        """
        Change any field or fields(surname, name...) in a specific directory entry.
        :param orig_surname: initial surname in note
        :param orig_name: initial name in note
        :param surname: new one or "-"
        :param name: new one or "-"
        :param arr_phone: new one or "-"
        :param b_day: new one or "-"
        :return: nothing, just update csv file
        """

        if len(arr_phone) > 1:
            mobile_number = (arr_phone[0].split(' '))[1]
            work_number = (arr_phone[1].split(' '))[1]
            home_number = (arr_phone[2].split(' '))[1]
            if mobile_number != '-':
                self.data.at[(orig_surname, orig_name), 'mobile_number'] = mobile_number
            if work_number != '-':
                self.data.at[(orig_surname, orig_name), 'work_number'] = work_number
            if home_number != '-':
                self.data.at[(orig_surname, orig_name), 'home_number'] = home_number
        else:
            if re.search(r'[Mm]', arr_phone[0]):
                self.data.at[(orig_surname, orig_name), 'mobile_number'] = (arr_phone[0].split(' '))[1]
            elif re.search(r'[Ww]', arr_phone[0]):
                self.data.at[(orig_surname, orig_name), 'work_number'] = (arr_phone[0].split(' '))[1]
            elif re.search(r'[Hh]', arr_phone[0]):
                self.data.at[(orig_surname, orig_name), 'home_number'] = (arr_phone[0].split(' '))[1]

        if b_day != '-':
            self.data.at[(orig_surname, orig_name), 'b_day'] = b_day

        # work with multi-index
        d2 = self.to_search(orig_surname, orig_name, '-', '-')

        s_n = d2.index.values[0]
        s = s_n[0]
        n = s_n[1]
        m_n = 'M ' + d2.mobile_number.values[0]
        w_n = 'W ' + d2.work_number.values[0]
        h_n = 'H ' + d2.home_number.values[0]
        b_d = d2.b_day.values[0]
        arr_numbers = [m_n, w_n, h_n]
        mode = 'sn'  # deletion by surname and name
        self.del_note(mode, orig_surname, orig_name)  # dell old

        if surname != '-' and name != '-':  # change surname&name (the whole index)
            self.add_note(surname, name, arr_numbers, b_d)  # add new

        elif surname != '-' and name == '-':
            self.add_note(surname, n, arr_numbers, b_d)  # add new

        elif name != '-' and surname == '-':
            self.add_note(s, name, arr_numbers, b_d)  # add new

    def get_age(self, surname: str, name: str):
        """
        Shows the age of a particular person.
        :return: print age or notification
        """
        if self.data.index.isin([(surname, name)]).any():  # if such person exists
            data1 = self.data.loc[(surname, name)]

            if str(data1.b_day) == '-':
                print(f"{Color.WARNING}The phone book doesn't contain such a birthday record.{Color.ENDC}")
                return

            _b_day_date = data1.b_day.replace('.', ' ')

            b_day_date = datetime.datetime.strptime(_b_day_date, '%d %m %Y').date()
            today = datetime.date.today()

            years = today.year - b_day_date.year

            self.to_search(surname=surname, name=name, phone_number='-', b_day='-')
            print('Age: ', years)
        else:
            print(f'{Color.WARNING}There is no note with such surname and name: {surname} {name}.{Color.ENDC}')
            return

    def _get_name(self, orig_bday: str) -> str:
        """
        Get surname and name of a person by his b-day.
        :param orig_bday: b-day of a person
        :return: surname and name
        """
        data1 = self.to_search('-', '-', '-', orig_bday)
        s = ''
        s += data1.index.values[0][0] + ' ' + data1.index.values[0][1]
        return s

    def show_bday_boy(self) -> list:
        """
        Shows all people who have a birthday in the next 30 days.
        :return: list of surname+name
        """
        bday_boys = list()

        today = datetime.date.today()
        thirty_days = today + datetime.timedelta(days=30)

        today = str(today).split('-')
        today_month = today[1]
        today_day = today[2]
        thirty_days = str(thirty_days).split('-')
        thirty_d_month = thirty_days[1]
        thirty_d_day = thirty_days[2]

        b_days = self.data.b_day.values
        for b_day in b_days:
            if b_day != '-':
                orig_bday = b_day
                b_d = b_day.split('.')[::-1]
                b_d_month = b_d[1]
                b_d_day = b_d[2]

                if b_d_month == today_month:
                    if (b_d_day > today_day) and (b_d_day < thirty_d_day):
                        s = self._get_name(orig_bday)
                        bday_boys.append(s)
                elif b_d_month == thirty_d_month:
                    if b_d_day < thirty_d_day:
                        s = self._get_name(orig_bday)
                        bday_boys.append(s)
        return bday_boys
