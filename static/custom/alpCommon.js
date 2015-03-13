/**
 * 这是做全局设定，在head-v1.vm中引入
 * TODO 将库文件在这里import，并合并
 */

var ALP = {};

jQuery(document).ready(function(){
	var nav = jQuery('#alp-nav');
	
	//设置导航
	nav.find('li').removeClass('current');
	if (typeof _APP != 'undefined' ) {
		nav.find('li[name=' + _APP + ']').addClass('current');
		try {nav.find('a[id=' + _APP + 'Link]').attr('target', '_self');}catch(e){}
	}

	if (window.main) {
		window.main();
    }
	try {
		ALP.Util.tracelog.initAliclick();
	} catch (e) {
	}
});

ALP.Import = function(filePath,charSet){
	var alpRoot = 'http://img.s.aliimg.com/alp/js/';
	if(typeof(charSet)!='string') charSet='utf-8';
	var src = '';
	if (filePath.match(/\.js$/i)) {
		src = (filePath.indexOf('http') == 0) ? filePath : alpRoot + filePath;
		document.write('<script charset="'+charSet+'" type="text/javascript" src="' + src + '"></scr' + 'ipt>');
	}
};

//ALP.Import = function() {
//    for (var i = 0; i < arguments.length; i++) {
//        var file = arguments[i];
//        if (file.match(/\.js$/i)) 
//            document.write('<script type="text/javascript" src="' + _ROOT + file +'"></script>');
//        else 
//            document.write('<style type="text/css">@import "' + file + '" ;</style>');
//    }
//};