$(document).ready(function() {

	var elistInit = function() {
		$("li").click(function() {
			var e = $(this).attr('data-id');
			var url;
			switch ($(this).parent().attr('id')) {
			case "person-elist":
				url = "admin/score_event_person";
				break;
			case "group-elist":
				url = "admin/score_event_group";
				break;
			case "group":
				url = "admin/score_group";
				break;
			default:
				return false;
			}

			window.location.href = "#page/" + url + "?event=" + e;

			//$.ajax({
			//  url:url+"?event="+e
			//  }).done(function(data){
			//    console.log(url);
			//    $('.page-content-area').html(data);
			//    window.location.href="#page/"+url;
			//    });
		});
	}
	elistInit();
});

