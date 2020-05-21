function changeImage(x) {
    for(i=1;i<5;i++){
        if(((document.getElementById(i).getAttribute("class"))=="active")&&i!=x)
            document.getElementById(i).setAttribute("class","not");
    }
    document.getElementById(x).setAttribute("class","active");
    var a=document.getElementById("image").getAttribute("name");
    document.getElementById("image").src="static/images/"+a+x+".png";
}
