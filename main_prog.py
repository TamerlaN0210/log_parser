from db_creator import DbCreator
from log_parser import Parser

if __name__ == '__main__':
    print('Для обработки логов требуется подключиться к вашей БД MySQL.',
          'Для этого введите через пробел ip базы данных, имя пользователя, пароль', sep='\n')
    data = input().split(' ')
    db_ip = data[0]
    db_username = data[1]
    db_password = data[2]
    print('Вы ввели ip: {}, имя: {}, пароль: {}'.format(db_ip, db_username, db_password))
    # Cоздание БД, затем её структуры
    my_db_creator = DbCreator()
    my_db_creator.create(db_ip, db_username, db_password)
    db_name = my_db_creator.get_db_name()
    # Парсинг логов
    myparser = Parser()
    myparser.connect_to_bd(db_ip, db_username, db_password, db_name)
    myparser.read()
    #todo: 3. Сопоставление ip к стране

