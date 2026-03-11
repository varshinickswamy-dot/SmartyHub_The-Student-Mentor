let t=1500;
setInterval(()=>{
 if(t>0){
  t--;
  document.getElementById("timer").innerText=t;
 }
},1000);