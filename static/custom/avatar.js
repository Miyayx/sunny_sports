// *** editable avatar *** //
try { //ie8 throws some harmless exceptions, so let's catch'em
	//first let's add a fake appendChild method for Image element for browsers that have a problem with this
	//because editable plugin calls appendChild, and it causes errors on IE at unpredicted points
	try {
		document.createElement('IMG').appendChild(document.createElement('B'));
	} catch(e) {
		Image.prototype.appendChild = function(el) {}
	}

	var last_gritter
	$('#avatar').editable({
		type: 'image',
		name: 'avatar',
		value: null,
		image: {
			//specify ace file input plugin's options here
			btn_choose: 'Change Avatar',
			droppable: true,
			maxSize: 110000,
			//~100Kb
			//and a few extra ones here
			name: 'avatar',
			//put the field name here as well, will be used inside the custom plugin
			on_error: function(error_type) { //on_error function will be called when the selected file has a problem
				if (last_gritter) $.gritter.remove(last_gritter);
				if (error_type == 1) { //file format error
					last_gritter = $.gritter.add({
						title: 'File is not an image!',
						text: 'Please choose a jpg|gif|png image!',
						class_name: 'gritter-error gritter-center'
					});
				} else if (error_type == 2) { //file size rror
					last_gritter = $.gritter.add({
						title: 'File too big!',
						text: 'Image size should not exceed 100Kb!',
						class_name: 'gritter-error gritter-center'
					});
				}
				else { //other error
				}
			},
			on_success: function() {
				$.gritter.removeAll();
			}
		},
		url: function(params) {
			// ***UPDATE AVATAR HERE*** //
			//for a working upload example you can replace the contents of this function with 
			//examples/profile-avatar-update.js
			var deferred = new $.Deferred

			var value = $('#avatar').next().find('input[type=hidden]:eq(0)').val();
			if (!value || value.length == 0) {
				deferred.resolve();
				return deferred.promise();
			}

			//dummy upload
			setTimeout(function() {
				if ("FileReader" in window) {
					//for browsers that have a thumbnail of selected image
					var thumb = $('#avatar').next().find('img').data('thumb');
					if (thumb) $('#avatar').get(0).src = thumb;
				}

				deferred.resolve({
					'status': 'OK'
				});

				if (last_gritter) $.gritter.remove(last_gritter);
				last_gritter = $.gritter.add({
					title: 'Avatar Updated!',
					text: 'Uploading to server can be easily implemented. A working example is included with the template.',
					class_name: 'gritter-info gritter-center'
				});

			},
			parseInt(Math.random() * 800 + 800))

			return deferred.promise();

			// ***END OF UPDATE AVATAR HERE*** //
		},

		success: function(response, newValue) {}
	})
} catch(e) {}

