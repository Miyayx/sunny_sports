jQuery(function($) {
	//editables on first profile page
	$.fn.editable.defaults.mode = 'inline';
	$.fn.editableform.loading = "<div class='editableform-loading'><i class='ace-icon fa fa-spinner fa-spin fa-2x light-blue'></i></div>";
	$.fn.editableform.buttons = '<button type="submit" class="btn btn-info editable-submit"><i class="ace-icon fa fa-check"></i></button>' + '<button type="button" class="btn editable-cancel"><i class="ace-icon fa fa-times"></i></button>';

	//editables 
	//text editable
	$('#name').editable({
		url: '/post',
		type: 'text',
		name: 'name',
		validate: function(v) {
			if ($.trim(v) == '') {
				return '姓名为必填项';
			}
		}
	});

	$('#sex').editable({
		source: [{
			value: 0,
			text: '男'
		},
		{
			value: 1,
			text: '女'
		}]
	});
	$('#birth').editable({
		type: 'adate',
		name: 'birth',
		datepicker: {
			//datepicker plugin options
			format: 'yyyy-mm-dd',
			viewformat: 'yyyy-mm-dd',
			weekStart: 1,
			language: "zh-CN" //要引用 bootstrap-datepicker.zh-CN.js
		},
        combodate:{
            minYear:1945,
			format: 'yyyy-mm-dd',
			viewformat: 'yyyy-mm-dd',
        }
	});

	$('#email').editable({
		type: 'text',
		name: 'email',
		validate: function(v) {
                v = $.trim(v);
			if ($.trim(v) == '') {
				return '邮箱为必填项';
			}
			if (!isEmail($.trim(v))) return '请输入正确的邮件地址';
			if (! ($(this).text() == $.trim(v) || $(this)[0].value == v)) {
				if (emailExists($.trim(v))) return '邮箱地址已注册';
			}

		}
	});

	$('#phone').editable({
		type: 'text',
		name: 'phone',
		validate: function(v) {
                v = $.trim(v);
			if (v == '') {
				return '手机号码为必填项';
			}
			if (!isPhoneNum(v)) {
				return '请输入正确的手机号码';
			}
			if (! ($(this).text() == v || $(this)[0].value == v)) {
				if (phoneExists($.trim(v))) return '手机号码已注册';
			}
		}
	});

	$('#identity').editable({
		type: 'text',
		name: 'identity',
        display: function(v){
        if(v.length)
            $(this).html(v.replace(v.substring(3,15), "**********"));
        },
		validate: function(v) {
			if ($.trim(v) == '') return '身份证号为必填项';
			if (!(isIdCardNo($.trim(v)) || isHKIdCardNo($.trim(v)))) return '请正确输入您的身份证号码';
			if (! ($(this).text() == v || $(this)[0].value == v || isHKIdCardNo($.trim(v)))) {
            var b = v.substring(6,10)+"-"+v.substring(10,12)+"-"+v.substring(12,14);
            $('#birth').editable('setValue', moment(b));
            }
            
		}
	});

});

