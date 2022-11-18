function deliverytime(clicked_name) {
  var choose = document.getElementsByName(clicked_name)[0];
  var dtime =choose.value;
  choose.style.backgroundColor = blue;
  

  $('input[name=dtime]').attr('value',dtime);          
}    