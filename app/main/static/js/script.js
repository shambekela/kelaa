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
		if(option.option == 'delete'){
			$('#channel-option-modal-label span.content').text('Delete Channel') 
			$(delet + ' .delete-title').text(option.title) // set channel name
			$('.delete-channel-key').val(option.key) // set delete form key
			$(delet).removeClass('d-none'); // show update section in modal
			$(edit).addClass('d-none'); // hide update section in modal
		}

		// if update option is selected.
		else if (option.option == 'edit'){
			$('#channel-option-modal-label span.content').text('Edit Channel')
			$('.update-channel-key').val(option.key) // set update form key
			$('.update-channel-title').val(option.title) // set update form title
			$('.update-channel-description').val(option.description) // set update form description
			$(edit).removeClass('d-none'); // show update section in modal
			$(delet).addClass('d-none'); // hide delete section in modal
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
	$('#delete-channel-form').on('submit', function(event) {
		event.preventDefault();

		// delete the selected channel
		$.ajax({
			url: '/delete_channel',
			type: 'POST',
			data: $(this).serialize(),
		})
		.done(function() {
			window.location.reload()
		})
		.fail(function() {
			alert("error");
		})
	});

	// question options

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

}());
