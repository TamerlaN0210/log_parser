<!DOCTYPE html>
<html>
<head>
	<title></title>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="questions.js"></script>
</head>
<body>
	<div class='question' id="q1">
		<b>1. Посетители из какой страны совершают больше всего действий на сайте?</b><br>
		<?
		include 'settings.php';
		$mysqli = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
		if ($mysqli->connect_errno) {
			echo "Не удалось подключиться к MySQL: (".$mysqli->connect_errno.") ".$mysqli->connect_error;
		}
		$res = $mysqli->query("SELECT `country`, COUNT(*) AS 'Count' FROM (SELECT `country` FROM `actions`, `ip`
							   WHERE `actions`.`ip` = `ip`.`id`) AS T
							   GROUP BY `country`
							   ORDER BY `Count` DESC
							   LIMIT 1");
		$row = $res->fetch_assoc();?>
		<div class="answer"><?
		echo $row['country'];?>
		</div>
	</div>
	<div class='question' id="q2">
		<b>2. Посетители из какой страны чаще всего интересуются товарами из определенных категорий?</b><br>
		<?
		$res = $mysqli->query("SELECT * FROM
								   (SELECT country, section, name, count(ip) as cnt
								   FROM actions, ip, sections
								   WHERE actions.ip = ip.id
								   AND actions.section =sections.id
								   AND actions.section is NOT NULL
								   GROUP BY ip.country, actions.section
								   ORDER BY cnt DESC, section DESC
								   LIMIT 5) AS T
							   ORDER BY section");?>
		<div class="answer"><?
		for ($row_no=0; $row_no < $res->num_rows; $row_no++) { 
			$res->data_seek($row_no);
			$row = $res->fetch_assoc();
			echo "<a> Товары категории: ".$row['name']." больше всего просматривали пользователи из страны ".$row['country']."</a><br>";
		}?>
		</div>
	</div>
	<div class="question" id="q3">
		<b>3. Какая нагрузка (число запросов) на сайт за астрономический час?</b><br>
		<?
		$res = $mysqli->query("SELECT AVG(hours) AS 'avg time'
							  FROM
							  (SELECT datetime, COUNT(*) AS 'hours'
							  FROM actions
							  GROUP BY day(datetime), hour(datetime)) as T");
		$row = $res->fetch_assoc();?>
		<div class="answer"><?
			echo "<a> Среднее число запросов за астрономический час: ".round($row['avg time']);?>
		</div>
	</div>
	<div class="question" id="q4">
		<b>4. Товары из какой категории чаще всего покупают совместно с товаром из заданной категории?</b>
		<select size='1' class="section-choose">
			<option selected disabled>Выберете интересующую вас категорию товаров</option>
			<?
			$res = $mysqli->query("SELECT * FROM `sections`");
			for ($row_no=0; $row_no < $res->num_rows; $row_no++) { 
				$res->data_seek($row_no);
				$row = $res->fetch_assoc();
				echo "<option class=\"option\" section_id={$row['id']}>{$row['name']}</option>";
			}?>
		</select>
		<br>
		<?
		$res = $mysqli->query("SELECT section, count(section) AS 'sum'
							   FROM (SELECT goods_in_carts.cart_id, sections.name as 'section'
							       FROM carts, goods_in_carts, goods, sections
							       WHERE goods_in_carts.good_id = goods.id
							       AND goods.section = sections.id
							       AND carts.id = goods_in_carts.cart_id
							       AND carts.is_payed = True) AS table1 # создаем таблицу с товарами, категориями и только оплачеными корзинами
							   WHERE table1.cart_id IN
							       (SELECT goods_in_carts.cart_id
							       FROM goods_in_carts, goods, sections
							       WHERE goods_in_carts.good_id = goods.id
							           AND goods.section = sections.id
							           AND sections.name = 'fresh_fish')  # находим id корзин с указанной категорией товаров
							   AND table1.section <> 'fresh_fish'
							   GROUP BY section
							   ORDER BY `sum`  DESC
							   LIMIT 1");	
		$row = $res->fetch_assoc();?>
		<div class="answer"><?
			echo "<a id='ans4'>Совместно с "." fresh_fish "."чаще всего покупают ".$row['section']."<a>";?>
		</div>
	</div>
	<div class="question" id="q5">
		<b>5. Сколько брошенных (не оплаченных) корзин имеется за определенный период?</b>
		<div>Начальное время</div>
		<input type="datetime" id="time1"  value="2018-08-01 00:00:00">
		<p></p>
		<div>Конечное время</div>
		<input type="datetime" id="time2"  value="2018-08-14 23:59:59">
		<br>
		<button id="count_cart">Посчитать неоплаченые корзины</button>
		<div class="answer"></div>
	</div>
</body>
</html>