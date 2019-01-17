import mysql.connector
import requests
from time import sleep


class IpCompare:
    def __init__(self, host, user, password, database, max_ip=100, pause_time=60):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.max_ip = max_ip
        self.pause_time = pause_time

    def get_ip(self) -> list:
        '''Возвращает список словарей вида [{ip: 0.0.0.0},{{ip: 0.0.0.0},...]'''
        connector = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                            database=self.database)
        cursor = connector.cursor()
        querry = 'SELECT `adress1`,`adress2`,`adress3`,`adress4` FROM ip'
        cursor.execute(querry)
        ip_list = list()
        for (adress1, adress2, adress3, adress4) in cursor:
            ip_list.append({'ip': '.'.join([str(adress1), str(adress2), str(adress3), str(adress4)])})
        connector.close()
        return ip_list

    def create_ip_country_file(self, file_name):
        ip_list = self.get_ip()
        for elem in ip_list:
            elem['query'] = elem.pop('ip')
            elem.update({'fields': 'country,countryCode,query'})
        print('Считано {} ip адресов. Создание файла {} займет около {} минут.'.
              format(len(ip_list), file_name, len(ip_list) // self.max_ip))
        ip_country = list()
        # создаем новый или очищаем имеющийся файл
        file = open(file_name, 'w')
        file.close()
        k = 0
        while k < len(ip_list) // self.max_ip + 1:
            ip_list_temp = ip_list[self.max_ip * k: self.max_ip * (k + 1)]
            k += 1
            response = requests.post('http://ip-api.com/batch', json=ip_list_temp)
            ip_country = ip_country + response.json()
            file = open(file_name, 'a')
            for elem in response.json():
                if 'country' in elem:
                    file.write('|'.join([elem.get('query'), elem.get('country'), elem.get('countryCode'), '\n']))
            file.close()
            print('Обработано {} IP из {}'.format(self.max_ip * (k + 1), len(ip_list)))
            sleep(self.pause_time)

    def compare(self, option: str):
        '''type: 'web' or 'file' '''
        if option == 'web':
            ip_list = self.get_ip()
            for elem in ip_list:
                elem['query'] = elem.pop('ip')
                elem.update({'fields': 'country,countryCode,query'})
            print('Считано {} ip адресов. Сопоставление ip к стране займет около {} минут.'.
                  format(len(ip_list), len(ip_list) // self.max_ip))
            ip_country = list()
            k = 0
            while k < len(ip_list) // self.max_ip + 1:
                ip_list_temp = ip_list[self.max_ip*k: self.max_ip*(k+1)]
                k += 1
                response = requests.post('http://ip-api.com/batch', json=ip_list_temp)
                ip_country = ip_country + response.json()
                self.set_country_from_web(response.json())
                sleep(self.pause_time)
        elif option == 'file':
            file_name = input('Введите имя файла или полный путь до него: ')
            self.set_country_from_file(file_name)

    def set_country_from_web(self, ip_country):
        connector = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                            database=self.database)
        cursor = connector.cursor()
        for elem in ip_country:
            if 'country' in elem:
                querry = 'UPDATE `ip` SET `country`=\'{}\', `country_code`=\'{}\' ' \
                         'WHERE `adress1`=\'{}\' AND `adress2`=\'{}\' AND `adress3`=\'{}\' AND `adress4`=\'{}\'' \
                    .format(str(elem.get('country')), str(elem.get('countryCode')),
                            str(elem.get('query').split('.')[0]), str(elem.get('query').split('.')[1]),
                            str(elem.get('query').split('.')[2]), str(elem.get('query').split('.')[3]))
            else:
                querry = 'UPDATE `ip` SET `country`=\'undetermined\', `country_code`=\'undetermined\' ' \
                         'WHERE `adress1`=\'{}\' AND `adress2`=\'{}\' AND `adress3`=\'{}\' AND `adress4`=\'{}\'' \
                    .format(str(elem.get('query').split('.')[0]), str(elem.get('query').split('.')[1]),
                            str(elem.get('query').split('.')[2]), str(elem.get('query').split('.')[3]))
            cursor.execute(querry)
            connector.commit()
        connector.close()

    def set_country_from_file(self, ip_country_file: str):
        is_file_correct = False
        while not is_file_correct:
            try:
                file = open(ip_country_file, 'r')
                is_file_correct = True
            except IOError:
                ip_country_file = input('Неправильно задан путь, либо файла по такому пути не существует. '
                                        'Введите правильный путь:')
                is_file_correct = False

        print('Началось сопоставление.')
        ip_country = list()
        for line in file:
            data = line.split('|')
            ip = data[0].split('.')
            ip_country.append({'ip1': ip[0], 'ip2': ip[1], 'ip3': ip[2], 'ip4': ip[3],
                               'country': data[1], 'countryCode': data[2]})
        connector = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                            database=self.database)
        cursor = connector.cursor(buffered=True)
        for elem in ip_country:
            query = 'UPDATE `ip` SET `country`=\'{}\', `country_code`=\'{}\' ' \
                    'WHERE `adress1`=\'{}\' AND `adress2`=\'{}\' AND `adress3`=\'{}\' AND `adress4`=\'{}\''. \
                format(elem.get('country'), elem.get('countryCode'),
                       elem.get('ip1'), elem.get('ip2'), elem.get('ip3'), elem.get('ip4'))
            cursor.execute(query)
            connector.commit()
        print('Сопоставление успешно завершено.')
        # для неопределенных ip
        query = 'UPDATE `ip` SET `country`=\'undetermined\', `country_code`=\'undetermined\' ' \
                'WHERE `country`=\'\' AND `country_code`=\'\''
        cursor.execute(query)
        connector.commit()
        connector.close()



if __name__ == '__main__':
    ip_compare = IpCompare(host="localhost", user="root", password="", database="delete_this", max_ip=100, pause_time=62)
    ip_compare.compare('file')
    #ip_compare.create_ip_country_file('test.txt')
