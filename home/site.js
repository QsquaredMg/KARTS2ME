(function(){
  "use strict";
  var y=document.getElementById("yr"); if(y) y.textContent=new Date().getFullYear();
  var b=document.getElementById("burger"), d=document.getElementById("drawer");
  if(b&&d){
    b.addEventListener("click",function(){var o=d.classList.toggle("open"); b.setAttribute("aria-expanded",String(o)); b.setAttribute("aria-label",o?"Close menu":"Open menu");});
    d.addEventListener("click",function(e){ if(e.target.tagName==="A"){d.classList.remove("open"); b.setAttribute("aria-expanded","false");} });
    document.addEventListener("keydown",function(e){ if(e.key==="Escape"&&d.classList.contains("open")){d.classList.remove("open"); b.setAttribute("aria-expanded","false"); b.focus();} });
  }
  // reveal on scroll
  var rv=[].slice.call(document.querySelectorAll(".rv"));
  if("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){ if(e.isIntersecting){e.target.classList.add("in"); io.unobserve(e.target);} });},{threshold:.12,rootMargin:"0px 0px -40px 0px"});
    rv.forEach(function(el,i){ el.style.transitionDelay=((i%3)*70)+"ms"; io.observe(el); });
  } else rv.forEach(function(el){el.classList.add("in");});
  // sticky mobile CTA appears after hero
  var m=document.getElementById("mcta"), hero=document.querySelector(".hero");
  if(m&&hero){
    var f=function(){ var r=hero.getBoundingClientRect(); m.classList.toggle("show", r.bottom<80); };
    window.addEventListener("scroll",f,{passive:true}); f();
  }
})();
