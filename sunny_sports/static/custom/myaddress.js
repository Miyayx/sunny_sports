// load city data
var citylist;
$.getJSON('../../static/custom/city.json', function(data) {
    citylist = data;
});
$('#province').editable({
    name: 'province',
    //validate: function(v) {
    //    if ($.trim(v) == '') {
    //        return '必填项';
    //    }
    //},
    source: function() {
        var a = Array();
        for(var v in citylist){
            a.push({
                text: v,
                value: v
            });
        };
        return a;
    }
});
$('#city').editable({
    name: 'city',
    //validate: function(v) {
    //    if ($.trim(v) == '') {
    //        return '必填项';
    //    }
    //},
    source: function() {
        var k = $.trim($('#province').html());
        if (k != "Empty") {
            var a = Array();
            for(var v in citylist[k]){
                a.push({
                    value: v,
                    text: v
                });
            };
            return a;
        } else {
            return {}
        }
    }
});
$('#dist').editable({
    name: 'dist',
    //validate: function(v) {
    //    if ($.trim(v) == '') {
    //        return '必填项';
    //    }
    //},
    source: function() {
        var k = $.trim($('#province').html());
        var j = $.trim($('#city').html());
        if (k != "Empty" && j != "Empty") {
            var a = Array();
            for(var v in citylist[k][j]){
                a.push({
                    value: citylist[k][j][v],
                    text: citylist[k][j][v]
                });
            };
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

