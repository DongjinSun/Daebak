function deliverytime(clicked_name) {
  var choose = document.getElementsByName(clicked_name)[0];
  var dtime =choose.value;

  for(var i=1; i<=12; i++){
    var str = 'time' + i;
    var target = document.getElementsByName(str)[0];
    choose.style.backgroundColor='#585858';
  } 
  choose.style.backgroundColor='BE81F7';
  

  $('input[name=dtime]').attr('value',dtime);          
}    