var can = document.getElementsByName("arr")[0].value;
var i = 1;
var j = 1;


while(i<=34){
    if(can[i]==0){
        var str = 'time' + j;
        var target = document.getElementsByName(str)[0];
        target.disabled= true;
    }
    else{
        target.disabled=false;
    }
    i += 3;
    j += 1;
}



//can 1 4 7 10 13 16 19 22 25 28 31 34 