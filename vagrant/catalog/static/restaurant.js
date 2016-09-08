// $(function(){
//   $('.action').hover(function(){
//     $(this).show();
//   },
// function() {
//   $(this).hide();
// });
// });

$(document).ready(function(){
  $('.action').hide();
  $('.restaurant_items').hover(function(){
    $('.action').show();
  },
  function(){
    $('.action').hide();
  });
});
