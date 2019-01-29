(function(){
	$('.main-card').on('mouseenter', function(event) {
		$(this).find('.ellipsis').removeClass('d-none');
	});

	$('.main-card').on('mouseleave', function(event) {
		$(this).find('.ellipsis').addClass('d-none');
	});
}())