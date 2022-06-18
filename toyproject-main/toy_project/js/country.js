$('.js-click-modal').click(function(){
  $('.container').addClass('modal-open');
  $('.infoArea').hide();
});

$('.js-close-modal').click(function(){
  $('.container').removeClass('modal-open');
  $('.infoArea').show();
});