var site = "http://itis.web";

$(document).ready(function($) {
	$(".section-choose").change( function(event) {
		var section = $(".section-choose").val();
		var section_together;
		var params = 'section=' + encodeURIComponent(section);
		var xhr = new XMLHttpRequest();
		xhr.open('GET', site + '/question4.php?' + params, true);
		xhr.send();
		xhr.onreadystatechange = function() {
			if(xhr.status != 200) {
				alert("Не удалось выполнить запрос.");
			}
			else {
				section_together = xhr.responseText;
				$("#ans4").text("Совместно с " + section + " чаще всего покупают " + section_together);
			}
		}
	});
	$("#count_cart").on('click', function(event) {
		var time1 = $("#time1").val();
		var time2 = $("#time2").val();
		var params = "time1=" + $("#time1").val() + "&time2=" + $("#time2").val();
		var xhr = new XMLHttpRequest();
		xhr.open('GET', site + '/question5.php?' + params, true);
		xhr.send();
		xhr.onreadystatechange = function() {
			if(xhr.status != 200) {
				alert("Не удалось выполнить запрос.");
			}
			else {
				$("#q5 div.answer").text("Неоплаченных корзин за данный период: " + xhr.responseText);
			}
		}
	});
});
