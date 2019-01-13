from db_creator import DbCreator
from log_parser import Parser
from ip import IpCompare

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
    ip_compare = IpCompare(host=db_ip, user=db_username, password=db_password, database=db_name, max_ip=100,
                           pause_time=62)
    print('Требуется сопоставить к какой стране относиться IP адресс.')
    print('Нажмите 1 для сопоставления IP с помощью файла-словаря')
    print('Нажмите 2 для сопоставления IP с помощью API сайта "ip-api.com"')
    option = int(input())
    if option == 1:
        print('Вы выбрали сопоставление из файла-словаря')
        ip_compare.compare('file')
    elif option == 2:
        print('Вы выбрали сопоставление с помощью API сайта "ip-api.com"')
        ip_compare.compare('web')

