<?
include 'settings.php';
$mysqli = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
if ($mysqli->connect_errno) {
	echo "Не удалось подключиться к MySQL: (".$mysqli->connect_errno.") ".$mysqli->connect_error;
}
$time1 = $_GET["time1"];
$time2 = $_GET["time2"];
$query = "SELECT COUNT(id_carts) as carts_num
		  FROM(SELECT actions.id_carts, actions.datetime, carts.is_payed, COUNT(actions.id_carts)
		  FROM actions LEFT JOIN carts
		  ON actions.id_carts = carts.id
		  WHERE carts.is_payed = False
		  AND actions.datetime > '{$time1}'
		  AND actions.datetime <= '{$time2}'
		  GROUP BY actions.id_carts) AS T";
$res = $mysqli->query($query);
$row = $res->fetch_assoc();
echo $row["carts_num"];
?>