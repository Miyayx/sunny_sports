function isEmail(email) {
    if (email.length == 0)
    return true;
	var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	return regex.test(email);
}

//jQuery.extend(jQuery.validator.messages, {
//    required: "必填",
//    remote: "请修正该字段",
//    email: "请输入正确格式的电子邮件",
//    url: "请输入合法的网址",
//    date: "请输入合法的日期",
//    dateISO: "请输入合法的日期 (ISO).",
//    number: "请输入合法的数字",
//    digits: "只能输入整数",
//    creditcard: "请输入合法的信用卡号",
//    equalTo: "请再次输入相同的值",
//    accept: "请输入拥有合法后缀名的字符串",
//    maxlength: jQuery.validator.format("请输入一个长度最多是 {0} 的字符串"),
//    minlength: jQuery.validator.format("请输入一个长度最少是 {0} 的字符串"),
//    rangelength: jQuery.validator.format("请输入一个长度介于 {0} 和 {1} 之间的字符串"),
//    range: jQuery.validator.format("请输入一个介于 {0} 和 {1} 之间的值"),
//    max: jQuery.validator.format("请输入一个最大为 {0} 的值"),
//    min: jQuery.validator.format("请输入一个最小为 {0} 的值")
//});
//$(document).ready(function () {
//    jQuery.validator.addMethod("isIdCardNo", function (value, element) {
//        return this.optional(element) || isIdCardNo(value);
//    }, "请正确输入您的身份证号码");
//});//增加身份证验证
function isIdCardNo(num) {
	var factorArr = new Array(7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1);
	var parityBit = new Array("1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2");
	var varArray = new Array();
	var intValue;
	var lngProduct = 0;
	var intCheckDigit;
	var intStrLen = num.length;
	var idNumber = num;
	// initialize
	if ((intStrLen != 15) && (intStrLen != 18)) {
		return false;
	}
	// check and set value
	for (i = 0; i < intStrLen; i++) {
		varArray[i] = idNumber.charAt(i);
		if ((varArray[i] < '0' || varArray[i] > '9') && (i != 17)) {
			return false;
		} else if (i < 17) {
			varArray[i] = varArray[i] * factorArr[i];
		}
	}
	if (intStrLen == 18) {
		//check date
		var date8 = idNumber.substring(6, 14);
		if (isDate8(date8) == false) {
			return false;
		}
		// calculate the sum of the products
		for (i = 0; i < 17; i++) {
			lngProduct = lngProduct + varArray[i];
		}
		// calculate the check digit
		intCheckDigit = parityBit[lngProduct % 11];
		// check last digit
		if (varArray[17] != intCheckDigit) {
			return false;
		}
	}
	else { //length is 15
		//check date
		var date6 = idNumber.substring(6, 12);
		if (isDate6(date6) == false) {
			return false;
		}
	}
	return true;
}

function isHKIdCardNo(num) {
     if (num.length == 0)
         return true;
     var regex = /^[A-Z]?[A-Z]{1}\d{6}\([0-9A]{1}\)$/;
     return regex.test(num);
 }

function isDate6(sDate) {
	if (!/^[0-9]{6}$/.test(sDate)) {
		return false;
	}
	var year, month, day;
	year = sDate.substring(0, 4);
	month = sDate.substring(4, 6);
	if (year < 1700 || year > 2500) return false
	if (month < 1 || month > 12) return false
	return true
}

/**
* 判断是否为“YYYYMMDD”式的时期
*/
function isDate8(sDate) {
	if (!/^[0-9]{8}$/.test(sDate)) {
		return false;
	}
	var year, month, day;
	year = sDate.substring(0, 4);
	month = sDate.substring(4, 6);
	day = sDate.substring(6, 8);
	var iaMonthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	if (year < 1700 || year > 2500) return false
	if (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0)) iaMonthDays[1] = 29;
	if (month < 1 || month > 12) return false
	if (day < 1 || day > iaMonthDays[month - 1]) return false
	return true
}

function isPhoneNum(phone) {
    if (phone.length == 0)
    return true;
	if (! (/^0?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/.test(phone))) return false;
	else return true;
}

function emailExists(v) {
	var flag = false;
	$.ajax({
		url: '/validate/email?email=' + $.trim(v),
		dataType: 'json',
		async: false,
		success: function(res) {
			if (res['exists']) {
				flag = true;
			}
		},
	});
	return flag ? true: false;
}

function nicknameExists(v) {
	var flag = false;
	$.ajax({
		url: '/validate/nickname?nickname=' + $.trim(v),
		dataType: 'json',
		async: false,
		success: function(res) {
			if (res['exists']) {
				flag = true;
			}
		},
	});
	return flag ? true: false;
}
function phoneExists(v) {
	var flag = false;
	$.ajax({
		url: '/validate/phone?phone=' + $.trim(v),
		dataType: 'json',
		async: false,
		success: function(res) {
			if (res['exists']) {
				flag = true;
			}
		},
	});
	return flag ? true: false;
}


function shortnameExists(v) {
	var flag = false;
	$.ajax({
		url: '/validate/shortname?shortname=' + $.trim(v),
		dataType: 'json',
		async: false,
		success: function(res) {
			if (res['exists']) {
				flag = true;
			}
		},
	});
	return flag ? true: false;
}

