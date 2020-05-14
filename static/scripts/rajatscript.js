var x = document.getElementById("sidenav");

var y= document.getElementById("three");

var z=document.getElementById("cross");

y.onclick=	function() {
    x.style.width= "220px";
   
}

z.onclick=function () {
   x.style.width = "0";

}



window.onclick = function(event) {
    if (event.target == x) {
        x.style.width = "0";
    }
}