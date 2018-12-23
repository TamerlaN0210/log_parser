import mysql.connector


class IpFromFile:
    def __init__(self, connector: mysql.connector):
        self.connector = connector
        self.cursor = connector.cursor(buffered=True)

    def set_countries(self, ip_country: list):
        for elem in ip_country:
            query = 'UPDATE `ip` SET `country`=\'{}\', `country_code`=\'{}\' ' \
                    'WHERE `adress1`=\'{}\' AND `adress2`=\'{}\' AND `adress3`=\'{}\' AND `adress4`=\'{}\''.\
                format(elem.get('country'), elem.get('countryCode'),
                       elem.get('ip1'), elem.get('ip2'), elem.get('ip3'), elem.get('ip4'))
            print(query)
            self.cursor.execute(query)
            self.connector.commit()

        #для неопределенных ip
        query = 'UPDATE `ip` SET `country`=\'undetermined\', `country_code`=\'undetermined\' ' \
                'WHERE `country`=\'\' AND `country_code`=\'\''
        self.cursor.execute(query)
        self.connector.commit()


if __name__ == '__main__':
    file = open('ip_country.txt', 'r')
    ip_country = list()
    for line in file:
        data = line.split('|')
        ip = data[0].split('.')
        ip_country.append({'ip1': ip[0], 'ip2': ip[1], 'ip3': ip[2], 'ip4': ip[3],
                           'country': data[1], 'countryCode': data[2]})
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="logs_data")
    ip_from_file = IpFromFile(mydb)
    ip_from_file.set_countries(ip_country=ip_country)
    mydb.close()
    print('End')
