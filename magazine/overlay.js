/* Translated pages keep the English page image (photos, logo, rules) and
   replace only the text, in the same rectangles. */
window.MagOverlay={paint:function(layer,n,ctx){
  var M=ctx.M,P=ctx.P,L=ctx.L,esc0=ctx.esc;
  /* Phone numbers keep their digit order inside right-to-left text. */
  function esc(s){return esc0(s).replace(/((?:[A-Za-z]+ )?\+?\d[\d ()\/+\-]{7,}\d)/g,"<span dir='ltr' style='unicode-bidi:isolate'>$1</span>");}
  var t=P[String(n)]||{};
  function box(x,y,w,h,cls,html){
    var d=document.createElement("div");
    d.className="ov "+cls;
    d.style.left=(x*100)+"%";
    d.style.top=(y*100)+"%";
    d.style.width=(w*100)+"%";
    d.style.height=(h*100)+"%";
    d.innerHTML=html;
    layer.appendChild(d);
  }
  var rtl=document.documentElement.dir==="rtl";
  var src="/magazine/p/"+(n<10?"0":"")+n+".jpg";
  /* Re-place a photo cut from the printed page: source rectangle (sx,sy,sw,sh) shown at x,y with width w. */
  function pic(sx,sy,sw,sh,x,y,w){
    var h=w*sh/sw, d=document.createElement("div");
    d.className="ov pic";
    d.style.left=(x*100)+"%"; d.style.top=(y*100)+"%"; d.style.width=(w*100)+"%"; d.style.height=(h*100)+"%";
    var im=document.createElement("img");
    im.src=src; im.alt=""; im.draggable=false;
    im.style.width=(100/sw)+"%"; im.style.height=(100/sh)+"%";
    im.style.left=(-sx/sw*100)+"%"; im.style.top=(-sy/sh*100)+"%";
    d.appendChild(im); layer.appendChild(d); return h;
  }
  function ps(a){return (a||[]).map(function(p){return "<p>"+esc(p)+"</p>";}).join("");}
  function ul(a){return "<ul>"+(a||[]).map(function(s){return "<li>"+esc(s)+"</li>";}).join("")+"</ul>";}
  function pairs(items){
    return "<ul>"+(items||[]).map(function(it){return "<li><b>"+esc(it.t||"")+"</b> "+esc(it.d||"")+"</li>";}).join("")+"</ul>";
  }
  function opener(y){
    var feats=ul(t.feature);
    box(0,y,1,1-y,"c","<p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2><div class='split'><p class='stand'>"+esc(t.stand||"")+"</p><div><p><b>"+esc(L.above||"")+"</b> "+esc(t.cap||"")+"</p><p class='k'>"+esc(L.feature||"")+"</p>"+feats+"</div></div>");
  }
  function storyBelow(y,html){box(0.04,y,0.92,0.98-y,"c",html);}
  function caps(list){return (list||[]).map(function(c){return "<p>"+esc(c)+"</p>";}).join("");}
  function days(list){
    return "<ol class='days'>"+(list||[]).map(function(d){
      return "<li><div class='k'>"+esc(L.day||"")+" "+esc(d.n)+"</div><div><b>"+esc(d.title)+"</b><div class='k'>"+esc(d.route||"")+"</div><p>"+esc(d.text||"")+"</p>"+(d.stay?"<p><b>"+esc(L.overnight||"")+"</b> "+esc(d.stay)+"</p>":"")+"</div></li>";
    }).join("")+"</ol>";
  }
  if(n===1){
    box(0.04,0.116,0.92,0.042,"c center","<div class='k'>"+esc(t.kicker||"")+"</div>");
    box(0.02,0.156,0.96,0.096,"c center","<div class='mast'>"+esc(M.brand||"")+"</div>");
    box(0.06,0.250,0.88,0.036,"c center","<div class='k'>"+esc(t.sub||"")+"</div>");
    var cols=(t.cols||[]).map(function(c){return "<div><b>"+esc(c.t)+"</b><span>"+esc(c.d)+"</span></div>";}).join("");
    box(0,0.801,1,0.199,"n center","<h2>"+esc(t.headline||"")+"</h2><p class='k'>"+esc(t.deck||"")+"</p><div class='q4'>"+cols+"</div><p class='k' style='margin-top:.35em'>"+esc(t.credit||"")+"</p>");
  }else if(n===2){
    box(0,0.70,1,0.30,"n","<p class='k'>"+esc(t.issue||"")+"</p><h2>"+esc(t.title||"")+"</h2><div class='split'><p class='stand'>"+esc(t.text||"")+"</p><p><b>"+esc(L.above||"")+"</b> "+esc(t.cap||"")+"</p></div>");
  }else if(n===3){
    /* Whole page re-laid: title, then the founder photo and the letter side by side from the same line. */
    box(0,0,1,0.955,"c","");
    box(0.06,0.02,0.88,0.15,"c bot","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2><div class='rule'></div>");
    var px=rtl?0.06:0.66, tx=rtl?0.36:0.06;
    var ph=pic(0.695,0.245,0.235,0.24,px,0.19,0.28);
    box(px,0.19+ph+0.008,0.28,0.07,"c","<p>"+esc(t.cap||"")+"</p>");
    box(tx,0.19,0.58,0.72,"c top",ps(t.paras)+"<p class='sig'><b>"+esc(t.sign||"")+"</b><br>"+esc(t.role||"")+"</p>");
  }else if(n===4){
    var items=(t.items||[]).map(function(it){return "<li><b>"+esc(it.n)+"</b><span><b>"+esc(it.t)+"</b> <i>"+esc(it.d)+"</i></span></li>";}).join("");
    box(0.035,0.02,0.555,0.96,"c","<p class='k'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2><ol class='toc'>"+items+"</ol>");
    box(0.615,0.485,0.37,0.49,"c","<p>"+esc(t.fig||"")+"</p>"+(t.pub||[]).map(function(p){return "<p>"+esc(p)+"</p>";}).join(""));
  }else if(n===5){
    box(0.06,0.02,0.88,0.15,"c center","<p class='k'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2>");
    var places=(t.places||[]).map(function(it){return "<li><b>"+esc(it.t)+"</b> "+esc(it.d)+"</li>";}).join("");
    box(0.05,0.80,0.9,0.18,"c","<ul class='cols'>"+places+"</ul><p>"+esc(t.note||"")+"</p>");
  }else if(n===6||n===10||n===14||n===22||n===28){
    opener(0.50);
  }else if(n===7){
    box(0.03,0.045,0.62,0.522,"c","<div class='cols'>"+ps(t.paras)+"</div>");
    box(0.66,0.012,0.31,0.035,"c","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p>");
    box(0.645,0.325,0.34,0.245,"c","<p>"+esc((t.caps||[])[0]||"")+"</p><div class='box'><p class='k'>"+esc(L.miss||"")+"</p>"+pairs(t.miss)+"</div>");
    box(0.04,0.872,0.475,0.055,"c","<p>"+esc((t.caps||[])[1]||"")+"</p>");
    box(0.515,0.872,0.455,0.055,"c","<p>"+esc((t.caps||[])[2]||"")+"</p>");
    box(0.04,0.93,0.92,0.045,"c","<p class='k'>"+esc(t.promo||"")+"</p>");
  }else if(n===8){
    box(0.58,0.03,0.39,0.52,"c","<p class='k'>"+esc(t.kicker||"")+"</p>"+ps(t.paras));
    box(0.02,0.555,0.54,0.06,"c","<p>"+esc((t.caps||[])[0]||"")+"</p>");
    box(0.05,0.835,0.28,0.1,"c","<p>"+esc((t.caps||[])[1]||"")+"</p>");
    box(0.35,0.835,0.27,0.1,"c","<p>"+esc((t.caps||[])[2]||"")+"</p>");
    box(0.64,0.835,0.32,0.1,"c","<p>"+esc((t.caps||[])[3]||"")+"</p>");
    if(t.promo) box(0.04,0.915,0.92,0.045,"c","<p class='k'>"+esc(t.promo)+"</p>");
  }else if(n===9){
    box(0.06,0.02,0.88,0.15,"c","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2>");
    box(0.05,0.50,0.9,0.46,"c","<p>"+esc((t.caps||[])[0]||"")+"</p><div class='cols3'>"+ps(t.paras)+"</div>");
  }else if(n===11){
    var rows=(t.rows||[]).map(function(r){return "<tr><td>"+esc(r.s)+"</td><td>"+esc(r.w)+"</td></tr>";}).join("");
    box(0.04,0.02,0.92,0.61,"c","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><div class='cols'>"+ps(t.paras)+"</div><h2>"+esc(t.tableTitle||"")+"</h2><table><thead><tr><td>"+esc((t.tableHead||[])[0]||"")+"</td><td>"+esc((t.tableHead||[])[1]||"")+"</td></tr></thead><tbody>"+rows+"</tbody></table>");
    box(0.56,0.64,0.4,0.28,"c","<p class='stand'>"+esc(t.quote||"")+"</p><p>"+esc(t.quoteBy||"")+"</p>");
    box(0.06,0.875,0.48,0.08,"c","<p>"+esc((t.caps||[])[0]||"")+"</p>");
  }else if(n===12){
    box(0.05,0.46,0.9,0.5,"c","<p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2><div class='split'><div>"+ps(t.paras)+"</div><div class='box'><p class='k'>"+esc(t.sideTitle||"")+"</p>"+pairs(t.side)+"</div></div>");
  }else if(n===13){
    box(0.05,0.015,0.9,0.15,"c bot","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2>");
    box(0.05,0.445,0.9,0.045,"c","<p>"+esc((t.caps||[])[0]||"")+"</p>");
    box(0.05,0.49,0.46,0.465,"c",ps(t.paras));
    box(0.51,0.865,0.45,0.085,"c","<p>"+esc((t.caps||[])[1]||"")+"</p>");
  }else if(n===15){
    box(0.05,0.02,0.9,0.44,"c","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><div class='split'><div>"+ps(t.paras)+"</div><div class='box'><p class='k'>"+esc(t.sideTitle||"")+"</p>"+pairs(t.side)+"</div></div>");
    box(0.06,0.80,0.88,0.16,"c","<p>"+esc((t.caps||[])[0]||"")+"</p><p class='k'>"+esc(t.promo||"")+"</p>");
  }else if(n===16){
    box(0.05,0.41,0.9,0.55,"c","<p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2><div class='cols3'>"+ps(t.paras)+"</div><p>"+esc((t.caps||[])[0]||"")+"</p>");
  }else if(n===17){
    var ev=(t.events||[]).map(function(e){return "<li><b>"+esc(e.y)+"</b><span>"+esc(e.t)+"</span></li>";}).join("");
    box(0.05,0.02,0.9,0.94,"c","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2><ol class='days ev'>"+ev+"</ol><p>"+esc(t.note||"")+"</p>");
  }else if(n===18||n===25){
    var sky=n===18?"rgba(96,140,208,.62)":"rgba(100,140,196,.62)";
    box(0,0.02,n===18?1:0.79,0.215,"sky big","<p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2>");
    layer.lastChild.style.background=sky;
    box(0,0.842,1,0.158,"n","<div class='split'><p class='stand'>"+esc(t.stand||"")+"</p><p><b>"+esc(L.above||"")+"</b> "+esc(t.cap||"")+"</p></div>");
  }else if(n===19){
    box(0.05,0.02,0.9,0.5,"c","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><div class='split'><div>"+ps(t.paras)+"</div><div class='box'><p class='k'>"+esc(t.sideTitle||"")+"</p>"+pairs(t.side)+"</div></div>");
    box(0.06,0.855,0.88,0.12,"c","<p>"+esc((t.caps||[])[0]||"")+"</p><p class='k'>"+esc(t.promo||"")+"</p>");
  }else if(n===20){
    box(0.05,0.67,0.9,0.28,"c","<div class='split'><div><p class='stand'>"+esc(t.quote||"")+"</p><p>"+esc(t.quoteBy||"")+"</p></div><p>"+esc((t.caps||[])[0]||"")+"</p></div>");
  }else if(n===21){
    box(0.04,0.012,0.93,0.19,"c bot","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2>");
    box(0.04,0.205,0.47,0.745,"c",ps(t.paras));
    box(0.515,0.595,0.45,0.25,"c","<p>"+esc((t.caps||[])[0]||"")+"</p><div class='box'><p class='k'>"+esc(L.miss||"")+"</p>"+pairs(t.miss)+"</div>");
  }else if(n===23){
    box(0.05,0.02,0.9,0.46,"c","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><div class='cols3'>"+ps(t.paras)+"</div>");
    box(0.06,0.84,0.88,0.12,"c","<p>"+esc((t.caps||[])[0]||"")+"</p>");
  }else if(n===24){
    box(0.04,0.012,0.645,0.37,"c","<p class='k'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p>"+ps(t.paras));
    box(0.50,0.375,0.49,0.055,"c","<p>"+esc((t.caps||[])[0]||"")+"</p>");
    box(0.04,0.44,0.92,0.22,"c","<p class='k'>"+esc(t.sideTitle||"")+"</p><div class='cols3'>"+pairs(t.side)+"</div>");
    box(0.05,0.875,0.46,0.07,"c","<p>"+esc((t.caps||[])[1]||"")+"</p>");
    box(0.51,0.875,0.44,0.07,"c","<p>"+esc((t.caps||[])[2]||"")+"</p>");
  }else if(n===26){
    box(0.05,0.38,0.9,0.58,"c","<p>"+esc((t.caps||[])[0]||"")+"</p><div class='split'><div>"+ps(t.paras)+"</div><div class='box'><p class='k'>"+esc(t.sideTitle||"")+"</p>"+pairs(t.side)+"</div></div>");
  }else if(n===27){
    box(0.78,0.012,0.19,0.035,"c","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p>");
    box(0.05,0.43,0.9,0.045,"c","<p>"+esc((t.caps||[])[0]||"")+"</p>");
    box(0.05,0.475,0.46,0.43,"c",ps(t.paras));
    box(0.52,0.772,0.44,0.07,"c","<p>"+esc((t.caps||[])[1]||"")+"</p>");
    box(0.04,0.915,0.92,0.045,"c","<p class='k'>"+esc(t.promo||"")+"</p>");
  }else if(n===29){
    box(0.75,0.012,0.22,0.035,"c","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p>");
    box(0.05,0.045,0.46,0.41,"c","<p class='k'>"+esc(t.kicker||"")+"</p>"+ps(t.paras));
    box(0.52,0.44,0.44,0.045,"c","<p>"+esc((t.caps||[])[0]||"")+"</p>");
    box(0.05,0.84,0.9,0.05,"c","<p>"+esc((t.caps||[])[1]||"")+"</p>");
  }else if(n===30){
    box(0.05,0.02,0.9,0.32,"c","<p class='k'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><div class='cols3'>"+ps(t.paras)+"</div>");
    box(0.05,0.64,0.5,0.05,"c","<p>"+esc((t.caps||[])[0]||"")+"</p>");
    box(0.58,0.64,0.36,0.05,"c","<p>"+esc((t.caps||[])[1]||"")+"</p>");
    box(0.58,0.685,0.38,0.07,"c","<p>"+esc((t.caps||[])[2]||"")+"</p>");
  }else if(n===31){
    box(0,0,1,0.39,"n mid big","<p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2><p class='stand'>"+esc(t.deck||"")+"</p>");
    box(0.05,0.41,0.9,0.55,"c","<div class='split'><div>"+ps(t.paras)+"</div><div class='box'><p class='k'>"+esc(L.miss||"")+"</p>"+pairs(t.miss)+"</div></div><p class='k'>"+esc(t.promo||"")+"</p>");
  }else if(n===32){
    box(0.05,0.43,0.9,0.52,"c","<p>"+esc((t.caps||[])[0]||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2><div class='split'><div>"+ps(t.paras)+"</div><div class='box'><p class='k'>"+esc(t.sideTitle||"")+"</p>"+pairs(t.side)+"</div></div>");
  }else if(n===33){
    box(0.04,0.012,0.93,0.19,"c bot","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2>");
    box(0.04,0.205,0.47,0.53,"c",ps(t.paras));
    box(0.515,0.42,0.45,0.055,"c","<p>"+esc((t.caps||[])[0]||"")+"</p>");
    box(0.515,0.708,0.45,0.035,"c","<p>"+esc((t.caps||[])[1]||"")+"</p>");
    box(0.04,0.745,0.92,0.215,"c","<div class='box'><p class='k'>"+esc(t.sideTitle||"")+"</p><div class='q4i'>"+pairs(t.side)+"</div></div><p class='k' style='margin-top:.6em'>"+esc(t.promo||"")+"</p>");
  }else if(n===34||n===36){
    box(0.05,0.02,0.9,0.94,"c","<p class='k'>"+esc(t.kicker||"")+"</p><p class='k'>"+esc(t.tour||"")+"</p><h2>"+esc(t.title||"")+"</h2><p class='stand'>"+esc(t.deck||"")+"</p>"+days(t.days));
  }else if(n===35||n===37){
    box(0,0.42,1,0.255,"n","<div class='split'><div><p class='k'>"+esc(L.included||"")+"</p>"+ul(t.included)+"</div><div><p class='k'>"+esc(L.excluded||"")+"</p><p>"+esc(t.excluded||"")+"</p><p class='k'>"+esc(L.good||"")+"</p><p>"+esc(t.good||"")+"</p></div></div>");
    box(0.04,0.675,0.74,0.27,"n","<p><b>"+esc(L.scan||"")+"</b><br>"+esc(t.url||"")+"<br><span dir='ltr'>"+esc(t.phone||"")+"</span></p>");
  }else if(n===38){
    var groups=(t.groups||[]).map(function(g){
      return "<div><h3>"+esc(g.h)+"</h3>"+(g.items||[]).map(function(it){return "<p><b>"+esc(it.t)+"</b> "+esc(it.d)+"</p>";}).join("")+"</div>";
    }).join("");
    box(0.05,0.03,0.9,0.92,"c","<p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2><div class='cols3'>"+groups+"</div><p><b>"+esc(t.noteTitle||"")+"</b> "+esc(t.note||"")+"</p>");
  }else if(n===39){
    box(0.04,0.012,0.93,0.29,"c","<p class='k run' style='text-align:end'>"+esc(t.run||"")+"</p><p class='k'>"+esc(t.kicker||"")+"</p><h2>"+esc(t.title||"")+"</h2><p class='stand'>"+esc(t.intro||"")+"</p>");
    var cx=[0.085,0.375,0.66];
    (t.cards||[]).forEach(function(c,i){
      if(i>2) return;
      box(cx[i],0.305,0.265,0.19,"c","<p><b class='big'>"+esc(c.days)+"</b></p><h3>"+esc(c.title)+"</h3><p>"+esc(c.text)+"</p>");
      box(cx[i],i===1?0.598:0.618,0.265,i===1?0.056:0.038,"c center","<p class='k'>"+esc(c.scan||"")+"</p>");
    });
    box(0.04,0.665,0.92,0.25,"c","<div class='split'><div><p class='k'>"+esc(t.howTitle||"")+"</p><p>"+esc(t.how||"")+"</p></div><div><p class='k'>"+esc(t.contactTitle||"")+"</p>"+(t.lines||[]).map(function(l){return "<p>"+esc(l)+"</p>";}).join("")+"</div></div>");
    box(0.04,0.915,0.92,0.045,"c","<p class='k'>"+esc(t.promo||"")+"</p>");
  }else if(n===40){
    box(0.06,0.545,0.88,0.24,"c center","<h2>"+esc(t.title||"")+"</h2><p>"+esc(t.text||"")+"</p>");
    box(0.27,0.81,0.5,0.125,"c","<p><b>"+esc(t.url||"")+"</b><br>"+esc(t.email||"")+"<br><span dir='ltr'>"+esc(t.phone||"")+"</span><br>"+esc(t.service||"")+"<br>"+esc(t.address||"")+"</p>");
    box(0.76,0.915,0.21,0.03,"c center","<p class='k'>"+esc(t.scan||"")+"</p>");
    box(0.06,0.952,0.88,0.045,"c center","<p class='k'>"+esc(t.credit||"")+"</p>");
  }
}};
