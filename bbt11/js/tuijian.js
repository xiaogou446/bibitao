// JavaScript Document
var index=0;

function scrollimgs(){
	var images=document.getElementsByClassName("images");
	var lis=images[0].getElementsByTagName("li");
	var btn=document.getElementsByClassName("b-t-n");
	var dots= btn[0].getElementsByTagName("li");
	lis[index].className="";
	dots[index].className="";
	index++;
	if(index>=lis.length){
		index=0;
	}
	lis[index].className="current";
	dots[index].className="current";
	setTimeout("scrollimgs()",4000);
}

window.onload=function(){
	scrollimgs();
}

