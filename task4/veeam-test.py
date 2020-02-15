"""
Напишите прототип тестовой системы, состоящей из двух тест-кейсов.
Каждый тест-кейс имеет свой номер (tc_id) и название (name); кроме того, каждый тест-кейс
определяет отдельные методы (или функции, в зависимости от избранной модели
реализации) для подготовки (prep), выполнения (run) и завершения (clean_up) тестов.
Метод execute задаёт общий порядок выполнения тест-кейса и обрабатывает
исключительные ситуации.
Тест-кейс 1: Список файлов
 [prep] Если текущее системное время, заданное как целое количество секунд от
начала эпохи Unix, не кратно двум, то необходимо прервать выполнение тест-кейса.
 [run] Вывести список файлов из домашней директории текущего.
 [clean_up].
Тест-кейс 2: Случайный файл
 [prep] Если объем оперативной памяти машины, на которой исполняется тест,
меньше одного гигабайта, то необходимо прервать выполнение тест-кейса.
 [run] Создать файл /tmp/test размером 1024 КБ с случайным содержимым.
 [clean_up] Удалить файл /tmp/test.
Все этапы выполнения тест-кейса, а также исключительные ситуации должны быть
задокументированы в лог-файле или в стандартном выводе.
"""


import os
import datetime
import random
import psutil


class TestCase(object):

    def __init__(self, tc_id=0, name='parent_case'):
        self.tc_id = tc_id
        self.name = name

    def prep(self):
        pass

    def run(self):
        pass

    def clean_up(self):
        pass

    def execute(self):
        try:
            prep = self.prep()
            if prep:
                result = prep
            else:
                result = self.run()
            self.clean_up()
        except Exception as e:
            result = e

        return result


class Case1(TestCase):

    def __init__(self):
        super().__init__()
        self.tc_id = 1
        self.name = 'file_list'

    def prep(self):
        timestamp = round(datetime.datetime.now().timestamp())
        if timestamp % 2:
            log(f'id: {self.tc_id} | prep:fail')
            return f'preparation_failed on {timestamp} stamp'
        log(f'id: {self.tc_id} | prep:success')

    def run(self):
        dir_list = os.listdir(os.getcwd())
        log(f'id: {self.tc_id} | run:success')
        return dir_list


class Case2(TestCase):

    def __init__(self):
        super().__init__()
        self.tc_id = 2
        self.name = 'random_file'

    def prep(self):

        virtual_memory = psutil.virtual_memory().total
        if virtual_memory < 1073741824:
            log(f'id: {self.tc_id} | prep:fail')
            return f'preparation_failed on {virtual_memory} memory size'
        log(f'id: {self.tc_id} | prep:success')

    def run(self):

        test_file_size = 1048576
        if 'tmp' not in os.listdir(os.getcwd()):
            os.mkdir('tmp')
        with open('tmp/test', 'w') as file:
            for i in range(test_file_size):
                file.write(str(random.randint(0, 9)))
        log(f'id: {self.tc_id} | run:success')
        return 'OK'

    def clean_up(self):
        if 'tmp' in os.listdir(os.getcwd()):
            if 'test' in os.listdir('tmp'):
                os.remove('tmp/test')
                os.rmdir('tmp')
        log(f'id: {self.tc_id} | clean:success')


def log(*args):
    with open('log.txt', 'a') as log:
        x = datetime.datetime.now()
        for arg in args:
            log.write(x.strftime("%x") + ' ' + x.strftime("%X") + ' | ' + arg + '\n')
            print(x.strftime("%x") + ' ' + x.strftime("%X") + ' | ' + arg)

if __name__ == '__main__':
    for case in Case1, Case2:
        test = case()
        test_result = test.execute()
        print(f'\nSUMMARY\nCase id: {test.tc_id}\nCase name: {test.name}\nResult: {test_result}\n')
