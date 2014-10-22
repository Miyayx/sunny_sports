jQuery(function($) {
	$('.nav li a').click(function() {
		a = $(this).attr('data-url');
		var v = $(".page-content-area");
		v.css("opacity", .25);
		var p = $('<div style="position: fixed; z-index: 2000;" class="ajax-loading-overlay"><i class="ajax-loading-icon fa fa-spin ' + 'fa-spinner fa-2x orange' + '"></i> ' + "</div>").insertBefore(v);
		f = v.offset();
		p.css({
			top: f.top,
			left: f.left
		});
		$.ajax({
			url: a
		}).complete(function() {
			v.css("opacity", 1),
			v.prevAll(".ajax-loading-overlay").remove()
		}).error(function(){
        
        }).done(function(data){
            v.html(data);
        });
    });
});

