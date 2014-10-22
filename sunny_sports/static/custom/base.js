jQuery(function($) {

	var updateBreadcrumbs = function(a) {
		var t = "",
		i = $(".breadcrumb");
		if (i.length > 0 && i.is(":visible")) {
			i.find("> li:not(:first-child)").remove();
			var s = 0;
			a.parents(".nav li").each(function() {
				var a = $(this).find("> a"),
				n = a.clone();
				n.find("i,.fa,.glyphicon,.ace-icon,.menu-icon,.badge,.label").remove();
				var r = n.text();
				n.remove();
				var o = a.attr("href");
				if (0 == s) {
					var l = $('<li class="active"></li>').appendTo(i);
					l.text(r),
					t = r
				} else {
					var l = $("<li><a /></li>").insertAfter(i.find("> li:first-child"));
					l.find("a").attr("href", o).text(r)
				}
				s++
			})
		}
	}

	$('.nav-list li a').click(function() {

		a = $(this);
		url = $(this).attr('data-url');
		var v = $(".page-content-area");
		v.css("opacity", .25);
		var p = $('<div style="position: fixed; z-index: 2000;" class="ajax-loading-overlay"><i class="ajax-loading-icon fa fa-spin ' + 'fa-spinner fa-2x orange' + '"></i> ' + "</div>").insertBefore(v);
		f = v.offset();
		p.css({
			top: f.top,
			left: f.left
		});
		$.ajax({
			url: url
		}).complete(function() {
			v.css("opacity", 1),
			v.prevAll(".ajax-loading-overlay").remove()
		}).error(function() {

		}).done(function(data) {
			//inside the function when ajax content is loaded
			//somehow get a reference to our newly clicked(selected) element's parent "LI"
			var new_active = $(a).parent();

			//remove ".active" class from all (previously) ".active" elements
			$('.nav-list li.active').removeClass('active');

			//add ".active" class to our newly selected item and all its parent "LI" elements
			new_active.addClass('active').parents('.nav-list li').addClass('active');

			//you can also update breadcrumbs:
			var breadcrumb_items = [];
			//$(this) is a reference to our clicked/selected element
			$(this).parents('.nav-list li').each(function() {
				var link = $(this).find('> a');
				var text = link.text();
				var href = link.attr('href');
				breadcrumb_items.push({
					'text': text,
					'href': href
				});
			})
			//now we have a breadcrumbs list and can replace breadcrumbs area
			$('#breadcrumbs').html(updateBreadcrumbs(a));

			v.html(data);

		});
	});
});

