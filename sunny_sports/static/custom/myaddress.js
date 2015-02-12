// load city data
var citylist;
$.getJSON('../../static/custom/city.json', function(data) {
	citylist = data;
});
$('#province').editable({
	name: 'province',
	source: function() {
		a = Array();
		Object.keys(citylist).forEach(function(v) {
			a.push({
				text: v,
				value: v
			});
		});
		return a;
	}
});
$('#city').editable({
	name: 'city',
	source: function() {
		var k = $('#province').html().trim();
		if (k != "Empty") {
			var a = Array();
			Object.keys(citylist[k]).forEach(function(v, i) {
				a.push({
					value: v,
					text: v
				});
			});
			return a;
		} else {
			return {}
		}
	}
});
$('#dist').editable({
	name: 'dist',
	source: function() {
		var k = $('#province').html().trim();
		var j = $('#city').html().trim();
		if (k != "Empty" && j != "Empty") {
			var a = Array();
			citylist[k][j].forEach(function(v, i) {
				a.push({
					value: v,
					text: v
				});
			});
			return a;
		} else {
			return {}
		}
	}
});
$('#address').editable({
	type: 'text',
	name: 'address'
});
