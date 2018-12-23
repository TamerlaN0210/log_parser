import mysql.connector
import requests
from time import sleep


class IpCompare:
    def __init__(self, mydb, max_ip=100, pause_time=60):
        self.mydb = mydb
        self.max_ip = max_ip
        self.pause_time = pause_time
        self.mycursor = mydb.cursor(buffered=True)

    def compare(self):
        mycursor = self.mycursor
        querry = ('SELECT `id`, `adress1`,`adress2`,`adress3`,`adress4` FROM ip')
        mycursor.execute(querry)
        ip_list = list()
        for (id, adress1, adress2, adress3, adress4) in mycursor:
            ip_list.append({'query': '.'.join([str(adress1), str(adress2), str(adress3), str(adress4)]),
                            'fields': 'country,countryCode,query'})
        print('Считано {} ip адресов. Сопоставление ip к стране займет около {} минут.'.
              format(len(ip_list),
                     len(ip_list) // self.max_ip))
        k = 0
        ip_country = list()
        file = open('ip_country.txt', 'w')
        file.close()

        while k < len(ip_list) // self.max_ip + 1:
            ip_list_temp = ip_list[self.max_ip*k: self.max_ip*(k+1)]
            k += 1
            print(ip_list_temp)
            response = requests.post('http://ip-api.com/batch', json=ip_list_temp)
            ip_country = ip_country + response.json()
            print(response.json())
            self.set_country(response.json())
            sleep(self.pause_time)

    #запись в бд

    def set_country(self, ip_country):
        file = open('ip_country.txt', 'a')
        for elem in ip_country:
            if 'country' in elem:
                querry = 'UPDATE `ip` SET `country`=\'{}\', `country_code`=\'{}\' ' \
                         'WHERE `adress1`=\'{}\' AND `adress2`=\'{}\' AND `adress3`=\'{}\' AND `adress4`=\'{}\'' \
                    .format(str(elem.get('country')), str(elem.get('countryCode')),
                            str(elem.get('query').split('.')[0]), str(elem.get('query').split('.')[1]),
                            str(elem.get('query').split('.')[2]), str(elem.get('query').split('.')[3]))
                file.write('|'.join([elem.get('query'), elem.get('country'), elem.get('countryCode'), '\n']))
            else:
                querry = 'UPDATE `ip` SET `country`=\'undetermined\', `country_code`=\'undetermined\' ' \
                         'WHERE `adress1`=\'{}\' AND `adress2`=\'{}\' AND `adress3`=\'{}\' AND `adress4`=\'{}\'' \
                    .format(str(elem.get('query').split('.')[0]), str(elem.get('query').split('.')[1]),
                            str(elem.get('query').split('.')[2]), str(elem.get('query').split('.')[3]))
        file.close()
            #self.mycursor.execute(querry)
            #self.mydb.commit()


if __name__ == '__main__':
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="logs_data")
    ip_compare = IpCompare(mydb, max_ip=100, pause_time=70)
    ip_compare.compare()
