(function(){
	/**
		Edit and delete option for home
	**/
	$('.main-card').on('mouseenter', function(event) {
		$(this).find('.ellipsis').removeClass('d-none');
	});

	$('.main-card').on('mouseleave', function(event) {
		$(this).find('.ellipsis').addClass('d-none');
	});	

	/**
		Edit and delete option for channel
	**/
	$('.question-card').on('mouseenter', function(event) {
		$(this).find('.question-card-option').removeClass('d-none');
	});

	$('.question-card').on('mouseleave', function(event) {
		$(this).find('.question-card-option').addClass('d-none');
	});


	$('.channel-option').on('click', function(){

		// get options for the channel selected.
		var option = {
			option: $(this).data('option'),
			key: $(this).data('key'),
			title: $(this).data('title'),
			description: $(this).data('desc')
		}

		var edit = '.modal-edit-option-content';
		var delet = '.modal-delete-option-content';

		// if delete option is selected.
		if (option.option == 'edit'){
			$('#channel-option-modal-label span.content').text('Edit Channel')
			$('.update-channel-key').val(option.key) // set update form key
			$('.update-channel-title').val(option.title) // set update form title
			$('.update-channel-description').val(option.description) // set update form description
		}
	})

	$('#edit-channel').on('submit', function(event) {
		event.preventDefault();
		// update the selected channel details.
		$.ajax({
			url: '/update_channel',
			type: 'POST',
			data: $(this).serialize(),
		})
		.done(function() {
			window.location.reload() // reload the page on successful update
		})
		.fail(function() {
			alert("error");
		})
	});

	// delete option handler
	$('.delete-channel').on('click', function(event) {
		event.preventDefault();

		key = $(this).data('key');
		title = $(this).data('title')

		$.confirm({
		    title: 'Delete channel - ' + title,
		    content: 'Are your sure ? all data related to this channel will be deleted forever.',
		    type: 'red',
		    buttons: {
		        delete: function () {
		            // delete the selected channel
					$.ajax({
						url: '/delete_channel',
						type: 'POST',
						data: {key: key},
					})
					.done(function() {
						$.alert({
							title: 'Done.',
							content: 'Deleted',
							buttons: {
								ok: function (){
									window.location.reload()
								}
							}
						})
					})
		        },
		        cancel: function () {
		        }
		    },
		    draggable: false
		});

	});

	// edit question
	$('.question-card-option a.question-edit').on('click', function(event) {
		event.preventDefault();
		/* Act on the event */

		var question = {
			key: $(this).data('key'),
			option: $(this).data('option')
		}

		$.ajax({
			url: '/question_option',
			type: 'POST',
			data: question
		})
		.done(function(resp) {
			$('.question-key-area').val(resp[0])
			$('.question-title-area').val(resp[1])
			$('.question-page-area').val(resp[2])
			$('.question-description-area').val(resp[3])
		})
		.fail(function() {
			window.location.reload()
		})
	});

	// edit question form handler
	$('#question-edit-form').on('submit', function(event) {
		event.preventDefault();
		$.ajax({
			url: '/update_question',
			type: 'POST',
			data: $(this).serialize(),
		})
		.done(function() {
			window.location.reload()
		})
		.fail(function() {
			console.log("error");
		});
	});

	// question options 
	$('.favourite-question').on('click',  function(event) {
		event.preventDefault();
		parent = $(this).parent()
		child = $(this).children('span')
		$.ajax({
			url: '/favourite_question',
			type: 'POST',
			data: {key: $(this).data('key')}
		})
		.done(function(resp) {
			if (resp) {
				child.empty().html('<i class="fas fa-star"></i>')
				parent.removeClass('d-none question-card-option');
			} else {
				child.empty().html('<i class="far fa-star"></i>')
				parent.addClass('question-card-option');
			}
		});

	});

	// channel options 

	// delete questions 
	$('.delete-question').on('click', function(event) {
		event.preventDefault();
		key = $(this).data('key');
		$.confirm({
		    title: 'Delete question',
		    content: 'Are you sure ?',
		    buttons: {
		        confirm: function () {
		            $.ajax({
		            	url: '/delete_question',
		            	type: 'POST',
		            	data: {key: key},
		            })
		            .done(function() {
		            	window.location.reload();
		            })
		            
		        },
		        cancel: function () {
		            
		        }
		    }
		});
	});

	// view answer in review modal
	$('.view-answer').on('click', function(event) {
		event.preventDefault();

		answer = $(this).data('answer');

		$.alert( answer );
	});

}());
