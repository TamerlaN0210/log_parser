<?
include 'settings.php';
$mysqli = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
if ($mysqli->connect_errno) {
	echo "Не удалось подключиться к MySQL: (".$mysqli->connect_errno.") ".$mysqli->connect_error;
}
$section = $_GET['section'];
$query = "SELECT section, count(section) AS 'sum'
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
							           AND sections.name = '{$section}')  # находим id корзин с указанной категорией товаров
							   AND table1.section <> '{$section}'
							   GROUP BY section
							   ORDER BY `sum`  DESC
							   LIMIT 1";
$res = $mysqli->query($query);
$row = $res->fetch_assoc();
echo $row['section'];
?>