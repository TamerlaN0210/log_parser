import mysql.connector


main_url = 'https://all_to_the_bottom.com/'


class Parser:
    section_and_good = None
    ips = set()
    goods = set()
    sections = set()
    users = set()
    carts = set()
    mydb = None
    mycursor = None

    def __init__(self):
        print('parser was created')

    def parse(self, array: list, parse_type: str):
        query = str()
        if parse_type == 'watch':
            section_and_good = array[-1][len(main_url)::].split('/')  # "убираем" url и его остаток делим через слэши
            if section_and_good[0] != '':
                if section_and_good[0] not in Parser.sections:  # добавляем раздел, если такого не существует
                    Parser.sections.add(section_and_good[0])
                    query = str()
                    query = ''.join(['INSERT INTO `sections`(`name`) VALUES ("', section_and_good[0], '");'])
                    self.mycursor.execute(query)
                    self.mydb.commit()
            if len(section_and_good) > 1:
                if section_and_good[1] not in Parser.goods and section_and_good[1] != '':
                    #  добавляем товар, если такого не существует
                    Parser.goods.add(section_and_good[1])
                    query = str()
                    query = ''.join([query, 'INSERT INTO `goods`(`name`, `section`) VALUES ("', section_and_good[1],
                                     '", (SELECT `id` FROM `sections` WHERE `name` = "', section_and_good[0], '"));'])
                    self.mycursor.execute(query)
                    self.mydb.commit()
            ip = array[-2].split('.')  # делим ip на разряды
            if array[-2] not in Parser.ips:
                Parser.ips.add(array[-2])
                query = str()
                query = ''.join([query, 'INSERT INTO `ip`(`adress1`,`adress2`,`adress3`,`adress4`) VALUES ("',
                                 ip[0], '","', ip[1], '","', ip[2], '","', ip[3], '");'])
                self.mycursor.execute(query)
                self.mydb.commit()
            query = str()
            query = ''.join([query, 'INSERT INTO `actions`(`datetime`, `hash`, `ip`, `type`,`section`,`good`) VALUES ("',
                             ' '.join([array[2], array[3]]), '","', array[4], '",',
                             '(SELECT `id` FROM `ip` WHERE `adress1` = "', ip[0],
                             '" AND `adress2` = "', ip[1], '" AND `adress3` = "', ip[2],
                             '" AND `adress4` = "', ip[3], '"), "watch", '])
            if section_and_good[0] == '':  # если нет категории, т.е. главная страница сайта, то ставим NULL
                query = ''.join([query, 'NULL,'])
            else:
                query = ''.join([query, '(SELECT `id` FROM `sections` WHERE `name` = "', section_and_good[0], '"), '])
            if len(section_and_good) == 1:  # если просмотр категории без товара, то товар NULL
                query = ''.join([query, 'NULL);'])
            elif len(section_and_good) > 1 and section_and_good[1] == '':
                query = ''.join([query, 'NULL);'])
            elif len(section_and_good) > 1 and section_and_good[1] != '':
                query = ''.join([query, '(SELECT `id` FROM `goods` WHERE `name` = "', section_and_good[1], '"));'])
            self.mycursor.execute(query)
            self.mydb.commit()

        if parse_type == 'add':
            ip = array[-2].split('.')  # делим ip на разряды
            # разбираем параметры запроса из URL
            add_info = [item.split('=') for item in array[-1].split('?')[1].split('&')]
            # код ниже сопоставляет good.id и good.id_from_logs
            query = str()
            query = ''.join([query, 'SELECT `id` FROM `ip` WHERE `adress1` = "', ip[0],
                             '" AND `adress2` = "', ip[1], '" AND `adress3` = "', ip[2],
                             '" AND `adress4` = "', ip[3], '";'])
            self.mycursor.execute(query)
            self.mydb.commit()
            ip_id = str(self.mycursor.fetchone()[0])
            query = str()
            query = ''.join([query, 'SELECT `good` FROM `actions` WHERE `datetime` = (SELECT MAX(`datetime`) ',
                             'FROM `actions` WHERE `ip` = "', ip_id, '") AND `ip`= "', ip_id, '";'])
            self.mycursor.execute(query)
            self.mydb.commit()
            good_id = str(self.mycursor.fetchone()[0])
            query = str()
            query = ''.join([query, 'UPDATE `goods` SET `id_from_logs` = "', add_info[0][1], '" WHERE `id` = "', good_id, '";'])
            self.mycursor.execute(query)
            self.mydb.commit()
            # теперь добавляем товар в корзину
            if add_info[2][1] not in Parser.carts:
                Parser.carts.add(add_info[2][1])
                query = str()
                query = ''.join([query, 'INSERT INTO `carts`(`cart_id`) VALUES ("', add_info[2][1], '");'])
                self.mycursor.execute(query)
                self.mydb.commit()
            query = str()
            query = ''.join([query, 'INSERT INTO `goods_in_carts`(`cart_id`, `good_id`, `good_amount`) VALUES (',
                             '(SELECT `id` FROM `carts` WHERE `cart_id` = "', add_info[2][1], '"), ',
                             '(SELECT `id` FROM `goods` WHERE `id_from_logs` = "', add_info[0][1], '"), ',
                             '"', add_info[1][1], '");'])
            self.mycursor.execute(query)
            self.mydb.commit()
            # добавляем запись о самом действии
            query = str()
            query = ''.join([query, 'INSERT INTO `actions`(`datetime`,`hash`,`ip`,`type`,`id_goods_in_carts`) VALUES ("',
                             ' '.join([array[2], array[3]]), '","', array[4], '",',
                             '(SELECT `id` FROM `ip` WHERE `adress1` = "', ip[0],
                             '" AND `adress2` = "', ip[1], '" AND `adress3` = "', ip[2],
                             '" AND `adress4` = "', ip[3], '"), "add", ',
                             '(SELECT LAST_INSERT_ID()))'])
            self.mycursor.execute(query)
            self.mydb.commit()
            print('parser_add')
        if parse_type == 'pay':
            ip = array[-2].split('.')  # делим ip на разряды
            # разбираем параметры запроса из URL
            pay_info = [item.split('=') for item in array[-1].split('?')[1].split('&')]
            if pay_info[0][1] not in Parser.users:
                Parser.users.add(pay_info[0][1])
                query = ''.join(['INSERT INTO `users`(`user_id`) VALUES ("', pay_info[0][1], '");'])
                self.mycursor.execute(query)
                self.mydb.commit()
            query = ''.join(['UPDATE `carts` SET `user_id`=(SELECT `id` FROM `users` WHERE `user_id`= "', pay_info[0][1], '") WHERE `cart_id`="',
                             pay_info[1][1], '" AND `user_id` IS NULL;'])
            self.mycursor.execute(query)
            self.mydb.commit()
            query = ''.join(['INSERT INTO `actions`(`datetime`, `hash`, `ip`, `type`,`id_carts`) VALUES ("',
                             ' '.join([array[2], array[3]]), '","', array[4], '",',
                             '(SELECT `id` FROM `ip` WHERE `adress1` = "', ip[0],
                             '" AND `adress2` = "', ip[1], '" AND `adress3` = "', ip[2],
                             '" AND `adress4` = "', ip[3], '"), "pay", (SELECT `id` FROM `carts` WHERE `cart_id`="',
                             pay_info[1][1], '"));'])
            self.mycursor.execute(query)
            self.mydb.commit()
            #print('parser_pay')
        if parse_type == 'confirm_pay':
            ip = array[-2].split('.')  # делим ip на разряды
            cart_number = array[-1][len(main_url)::].split('/')[0].split('_')[2]
            query = ''.join(['UPDATE `carts` SET `is_payed`="1" WHERE `cart_id`="', cart_number, '";'])
            self.mycursor.execute(query)
            self.mydb.commit()
            query = ''.join(['INSERT INTO `actions`(`datetime`, `hash`, `ip`, `type`,`id_carts`) VALUES ("',
                             ' '.join([array[2], array[3]]), '","', array[4], '",',
                             '(SELECT `id` FROM `ip` WHERE `adress1` = "', ip[0],
                             '" AND `adress2` = "', ip[1], '" AND `adress3` = "', ip[2],
                             '" AND `adress4` = "', ip[3], '"), "check", (SELECT `id` FROM `carts` WHERE `cart_id`="',
                             cart_number, '"));'])
            self.mycursor.execute(query)
            self.mydb.commit()

    def read(self):
        print(self.mydb.is_connected())
        # todo поменять мое расположение файла на стандартный путь
        path_to_logs = 'logs/logs.txt'
        temp = input('Введите имя файла или полный путь до него: ')
        if temp != '':
            path_to_logs = temp
        file = open(path_to_logs)
        for line in file:
            temp = str.split(line)
            if temp[-1].find('success_pay_') != -1:
                self.parse(temp, 'confirm_pay')
            elif temp[-1].find('?') == -1:  # если -1, значит вхождения строки нет
                self.parse(temp, 'watch')
            elif temp[-1].find('cart?') != -1:
                self.parse(temp, 'add')
            elif temp[-1].find('pay?') != -1:
                self.parse(temp, 'pay')

    def connect_to_bd(self, db_ip, db_username, db_password, db_name):
        self.mydb = mysql.connector.connect(host=db_ip, user=db_username, password=db_password, database=db_name)
        self.mycursor = self.mydb.cursor(buffered=True)
