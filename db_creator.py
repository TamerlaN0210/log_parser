import mysql.connector


class DbCreator:
    __db_struct_creation_query = """SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE TABLE `actions` (
  `id` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  `hash` varchar(50) NOT NULL,
  `ip` int(11) NOT NULL,
  `type` set('watch','add','pay','confirm_pay') NOT NULL,
  `section` int(11) DEFAULT NULL,
  `good` int(11) DEFAULT NULL,
  `id_goods_in_carts` int(11) DEFAULT NULL,
  `id_carts` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `carts` (
  `id` int(11) NOT NULL,
  `cart_id` int(11) NOT NULL COMMENT 'id корзины в магазине',
  `is_payed` tinyint(1) NOT NULL DEFAULT '0',
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `goods` (
  `id` int(11) NOT NULL,
  `id_from_logs` int(11) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `section` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `goods_in_carts` (
  `id` int(11) NOT NULL,
  `cart_id` int(11) NOT NULL,
  `good_id` int(11) NOT NULL,
  `good_amount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `ip` (
  `id` int(11) NOT NULL,
  `adress1` tinyint(3) UNSIGNED NOT NULL,
  `adress2` tinyint(3) UNSIGNED NOT NULL,
  `adress3` tinyint(3) UNSIGNED NOT NULL,
  `adress4` tinyint(3) UNSIGNED NOT NULL,
  `country` varchar(50) NOT NULL,
  `country_code` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `sections` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `actions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ip` (`ip`),
  ADD KEY `good` (`good`),
  ADD KEY `section` (`section`),
  ADD KEY `id_carts` (`id_carts`),
  ADD KEY `id_goods_in_carts` (`id_goods_in_carts`);

ALTER TABLE `carts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cart_id` (`cart_id`),
  ADD KEY `user_id` (`user_id`);

ALTER TABLE `goods`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `id_from_logs` (`id_from_logs`),
  ADD KEY `section` (`section`);

ALTER TABLE `goods_in_carts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cart_id` (`cart_id`),
  ADD KEY `good_id` (`good_id`);

ALTER TABLE `ip`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `sections`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);
  
ALTER TABLE `actions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `carts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `goods`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `goods_in_carts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `ip`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `sections`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
  

ALTER TABLE `actions`
  ADD CONSTRAINT `actions_ibfk_1` FOREIGN KEY (`ip`) REFERENCES `ip` (`id`),
  ADD CONSTRAINT `actions_ibfk_2` FOREIGN KEY (`good`) REFERENCES `goods` (`id`),
  ADD CONSTRAINT `actions_ibfk_3` FOREIGN KEY (`section`) REFERENCES `sections` (`id`),
  ADD CONSTRAINT `actions_ibfk_4` FOREIGN KEY (`id_carts`) REFERENCES `carts` (`id`),
  ADD CONSTRAINT `actions_ibfk_5` FOREIGN KEY (`id_goods_in_carts`) REFERENCES `goods_in_carts` (`id`);

ALTER TABLE `carts`
  ADD CONSTRAINT `carts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `goods`
  ADD CONSTRAINT `goods_ibfk_1` FOREIGN KEY (`section`) REFERENCES `sections` (`id`);

ALTER TABLE `goods_in_carts`
  ADD CONSTRAINT `goods_in_carts_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `carts` (`id`),
  ADD CONSTRAINT `goods_in_carts_ibfk_2` FOREIGN KEY (`good_id`) REFERENCES `goods` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;"""

    def __init__(self):
        self.__db_name = None

    def get_db_name(self):
        return self.__db_name

    def create(self, host, user, password):
        db_name = input('Введите название на латинице для базы данных о логах: ')
        self.__db_name = db_name.replace(' ', '_')
        query = 'CREATE DATABASE {}'.format(self.__db_name)
        mydb = mysql.connector.connect(host=host, user=user, password=password)
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(query)
        mydb.commit()
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=self.__db_name)
        mycursor = mydb.cursor(buffered=True)
        # цикл ниже нужен для выполнения множественных запросов к базе
        for result in mycursor.execute(self.__db_struct_creation_query, multi=True):
            pass
        mydb.commit()
        mydb.close()
        print('Структура базы данных "{}" была создана'.format(db_name))
