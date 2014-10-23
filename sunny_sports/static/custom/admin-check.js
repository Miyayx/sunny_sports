//全选，反选
jQuery(function($) {
	showGroupDetail = function() {
		//show detail group info
		$('span.label').parents('td').click(function() {
			id_ = $(this).closest('table').attr('id');
			console.log(id_)
			checked = 0;
			if (id_ == "checked-table") {
				checked = 1;
			}

			$.get('/admin/group_detail?checked=' + checked, function(data) {
				bootbox.dialog({
					message: data,
					title: "参赛队详细信息",
					buttons: {
						success: {
							label: '<i class="ace-icon fa fa-check"></i>确认',
							className: "btn btn-info btn-sm",
						},
					},
				});
			});
		});
	}

	initMultiCheckBtn = function() {
		//确认框，判断是否有选项
		$('#multi-check').click(function() {
			checkedItems = [];

			$('#not-check-table').find('tr > td:first-child input[name="sub-box"]').each(function() {
				if (this.checked) {
					checkedItems.push($(this).closest('tr').find('td:nth-child(2)').text());
				}
			});

			//所有选中的item形成一个list，在box里显示用
			itemList = $('<ul></ul>');
			for (i = 0; i < checkedItems.length; i++) {
				item = $('<li>' + checkedItems[i] + '</li>');
				itemList.append(item);
			}

			bootbox.dialog({
				title: "是否确认以下参赛队审核通过？",
				message: itemList,
				buttons: {
					success: {
						label: '<i class="ace-icon fa fa-check"></i>确认',
						className: "btn btn-info btn-sm",
					},
					cancel: {
						label: '<i class="ace-icon fa fa-times"></i>取消',
						className: "btn btn-sm",
					}
				},
			});
		});
	}

	showGroupDetail();
	initMultiCheckBtn();

});

//inline scripts related to this page
//jQuery(function($) {
//	var oTable1 = $('#not-check-table')
//	//.wrap("<div class='dataTables_borderWrap' />")   //if you are applying horizontal scrolling (sScrollX)
//	.dataTable({
//		bAutoWidth: false,
//		"aoColumns": [{
//			"bSortable": false
//		},
//		null, null, null, null, null, {
//			"bSortable": false
//		}],
//		"aaSorting": [],
//
//		//,
//		//"sScrollY": "200px",
//		//"bPaginate": false,
//		//"sScrollX": "100%",
//		//"sScrollXInner": "120%",
//		//"bScrollCollapse": true,
//		//Note: if you are applying horizontal scrolling (sScrollX) on a ".table-bordered"
//		//you may want to wrap the table inside a "div.dataTables_borderWrap" element
//		//"iDisplayLength": 50
//	});
//	/**
//		var tableTools = new $.fn.dataTable.TableTools( oTable1, {
//			"sSwfPath": "../../copy_csv_xls_pdf.swf",
//	        "buttons": [
//	            "copy",
//	            "csv",
//	            "xls",
//				"pdf",
//	            "print"
//	        ]
//	    } );
//	    $( tableTools.fnContainer() ).insertBefore('#sample-table-2');
//		*/
//
//	$(document).on('click', 'th input:checkbox', function() {
//		var that = this;
//		$(this).closest('table').find('tr > td:first-child input:checkbox').each(function() {
//			this.checked = that.checked;
//			$(this).closest('tr').toggleClass('selected');
//		});
//	});
//
//	$('[data-rel="tooltip"]').tooltip({
//		placement: tooltip_placement
//	});
//	function tooltip_placement(context, source) {
//		var $source = $(source);
//		var $parent = $source.closest('table')
//		var off1 = $parent.offset();
//		var w1 = $parent.width();
//
//		var off2 = $source.offset();
//		//var w2 = $source.width();
//		if (parseInt(off2.left) < parseInt(off1.left) + parseInt(w1 / 2)) return 'right';
//		return 'left';
//	}
//})

