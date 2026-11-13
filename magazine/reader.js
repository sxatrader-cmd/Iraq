/* Renders a translated MESOPOTAMIA issue inside the same page-flip viewer.
   Photographs are cropped from the English press pages so the pictures stay. */
(function(){
var LANGS=[
  ["ar","العربية"],["ckb","کوردی"],["en","English"],["tr","Türkçe"],["ru","Русский"],
  ["de","Deutsch"],["fr","Français"],["es","Español"],["it","Italiano"],["el","Ελληνικά"],
  ["cs","Čeština"],["pl","Polski"],["zh","简体中文"],["zh-tw","繁體中文"],["ja","日本語"],
  ["fa","فارسی"],["ms","Bahasa Melayu"],["id","Bahasa Indonesia"],["th","ไทย"],["hi","हिन्दी"],
  ["ur","اردو"],["ta","தமிழ்"],["fi","Suomi"],["sv","Svenska"],["da","Dansk"],
  ["no","Norsk"],["sk","Slovenčina"],["hr","Hrvatski"],["ro","Română"],["nl","Nederlands"],
  ["ka","ქართული"],["ko","한국어"],["pt","Português"],["vi","Tiếng Việt"],["hu","Magyar"]
];
var RTL={ar:1,ckb:1,fa:1,ur:1};
function hrefOf(code){return code==="en"?"/magazine/":"/"+code+"/magazine/";}
function homeOf(code){return code==="ar"?"/":code==="en"?"/en/":"/"+code+"/";}
var M=window.MAG;
if(!M){document.body.textContent="Magazine translation missing.";return}
document.documentElement.lang=M.lang;
document.documentElement.dir=M.dir||(RTL[M.lang]?"rtl":"ltr");
if(M.metaTitle) document.title=M.metaTitle;
var md=document.querySelector('meta[name="description"]');
if(md&&M.metaDesc) md.setAttribute("content",M.metaDesc);
var L=M.label||{}, P=M.pages||{}, ui=M.ui||{};
var rtl=document.documentElement.dir==="rtl";

var BOX={
1:[[0,0.28,1,0.80]],
2:[[0,0,1,0.70]],
3:[[0.62,0.20,0.96,0.50]],
4:[[0.62,0.08,1,0.50]],
5:[[0.07,0.18,0.93,0.78]],
6:[[0,0,1,0.50]],
7:[[0.64,0.05,1,0.33],[0.07,0.57,0.50,0.88],[0.51,0.57,1,0.88]],
8:[[0,0,0.58,0.56],[0.07,0.62,0.34,0.84],[0.35,0.62,0.63,0.84],[0.64,0.63,0.94,0.84]],
9:[[0.07,0.15,0.93,0.50]],
10:[[0,0,1,0.50]],
11:[[0.07,0.63,0.56,0.88]],
12:[[0,0,1,0.46]],
13:[[0.07,0.15,0.94,0.46],[0.52,0.50,0.94,0.88]],
14:[[0,0,1,0.52]],
15:[[0.07,0.46,0.94,0.80]],
16:[[0,0,1,0.40]],
18:[[0,0,1,0.82]],
19:[[0.07,0.52,0.94,0.86]],
20:[[0,0,1,0.67]],
21:[[0.52,0.16,0.94,0.62]],
22:[[0,0,1,0.50]],
23:[[0.07,0.48,0.94,0.84]],
24:[[0.50,0.05,1,0.38],[0.06,0.65,0.49,0.88],[0.50,0.65,0.94,0.88]],
25:[[0,0,1,0.82]],
26:[[0,0,1,0.37]],
27:[[0.07,0.06,0.94,0.43],[0.52,0.47,0.94,0.76]],
28:[[0,0,1,0.50]],
29:[[0.52,0.05,1,0.45],[0.07,0.49,0.94,0.85]],
30:[[0.06,0.34,0.50,0.64],[0.52,0.34,0.94,0.64],[0.06,0.67,0.58,0.92]],
32:[[0,0.02,1,0.42]],
33:[[0.52,0.16,0.95,0.44],[0.52,0.46,0.95,0.72]],
35:[[0,0,1,0.42]],
37:[[0,0,1,0.42]],
40:[[0,0,1,0.52]]
};

function el(tag,cls,html){
  var n=document.createElement(tag);
  if(cls) n.className=cls;
  if(html!=null) n.innerHTML=html;
  return n;
}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function crop(n,i,alt){
  var box=(BOX[n]||[])[i]; if(!box) return null;
  var x0=box[0],y0=box[1],x1=box[2],y1=box[3];
  var aw=((x1-x0)/(y1-y0))*(1075/1521);
  var d=el("div","crop");
  d.style.setProperty("--fx",String(x1-x0));
  d.style.setProperty("--ar",String(aw));
  var img=document.createElement("img");
  img.src="/magazine/p/"+(n<10?"0":"")+n+".jpg";
  img.alt=alt||M.brand||"";
  img.decoding="async";
  /* Map the printed crop onto the box. The box aspect matches the crop, so this does not stretch. */
  img.style.width=(100/(x1-x0))+"%";
  img.style.height=(100/(y1-y0))+"%";
  img.style.left=(-x0/(x1-x0)*100)+"%";
  img.style.top=(-y0/(y1-y0)*100)+"%";
  img.style.maxWidth="none";
  d.appendChild(img);
  return d;
}
function paras(list,drop){
  var w=el("div","paras"+(list&&list.length>4?" cols":""));
  (list||[]).forEach(function(t,i){
    var p=el("p",drop&&i===0?"drop":"");
    p.textContent=t;
    w.appendChild(p);
  });
  return w;
}
function folio(n,end){
  var s=el("p","folio"+(end?" end":""));
  s.textContent=end?(M.brand+"  ·  "+n):(n+"  ·  "+M.brand);
  return s;
}
function cap(text){
  if(!text) return el("p","cap","");
  var p=el("p","cap");
  var i=text.indexOf(" ");
  if(i>0&&i<28){
    p.innerHTML="<b>"+esc(text.slice(0,i))+"</b> "+esc(text.slice(i+1));
  }else p.textContent=text;
  return p;
}
function pairs(list){
  var ul=el("ul");
  (list||[]).forEach(function(it){
    var li=el("li");
    li.innerHTML="<b>"+esc(it.t||it.h||"")+"</b><span>"+esc(it.d||"")+"</span>";
    ul.appendChild(li);
  });
  return ul;
}
function aside(title,list){
  var a=el("aside","aside box");
  if(title) a.appendChild(el("h3","",esc(title)));
  a.appendChild(pairs(list));
  return a;
}

function pageCover(t){
  var s=el("article","sheet cover");
  var top=el("div","cover-top");
  top.appendChild(el("p","kicker",esc(t.kicker)));
  top.appendChild(el("h1","brand",esc(M.brand)));
  var rule=el("hr","rule"); rule.style.margin="0.5em auto"; rule.style.width="28%";
  top.appendChild(rule);
  top.appendChild(el("p","sub",esc(t.sub)));
  s.appendChild(top);
  var ph=crop(1,0,t.credit); if(ph) s.appendChild(ph);
  var foot=el("div","cover-foot");
  foot.appendChild(el("h1","",esc(t.headline)));
  foot.appendChild(el("p","deck",esc(t.deck)));
  var q=el("div","quad");
  (t.cols||[]).forEach(function(c){
    var d=el("div"); d.innerHTML="<b>"+esc(c.t)+"</b><span>"+esc(c.d)+"</span>"; q.appendChild(d);
  });
  foot.appendChild(q);
  foot.appendChild(el("p","credit",esc(t.credit)));
  s.appendChild(foot);
  return s;
}
function pageWelcome(t){
  var s=el("article","sheet"); s.style.padding="0"; s.style.gap="0";
  var ph=crop(2,0,t.cap); if(ph) s.appendChild(ph);
  var band=el("div","navy"); band.style.padding="4.5% 5.5% 4%"; band.style.flex="1"; band.style.display="flex"; band.style.flexDirection="column";
  band.appendChild(el("p","kicker",esc(t.issue)));
  band.appendChild(el("h1","",esc(t.title)));
  var row=el("div","split"); row.style.marginTop=".6em";
  var stand=el("p","stand"); stand.textContent=t.text; row.appendChild(stand);
  row.appendChild(cap((L.above?L.above+" ":"")+(t.cap||"")));
  band.appendChild(row);
  band.appendChild(folio(2,false));
  s.appendChild(band);
  return s;
}
function pageLetter(t){
  var s=el("article","sheet");
  s.appendChild(el("p","run",esc(t.run)));
  var row=el("div"); row.style.display="grid"; row.style.gridTemplateColumns="1.4fr .7fr"; row.style.gap="1em";
  var main=el("div");
  main.appendChild(el("p","kicker",esc(t.kicker)));
  main.appendChild(el("h1","",esc(t.title)));
  main.appendChild(el("hr","rule"));
  main.appendChild(paras(t.paras,true));
  var sign=el("p"); sign.style.marginTop=".8em";
  sign.innerHTML="<b>"+esc(t.sign)+"</b><br><span class='cap'>"+esc(t.role)+"</span>";
  main.appendChild(sign);
  row.appendChild(main);
  var side=el("div");
  var ph=crop(3,0,t.sign); if(ph) side.appendChild(ph);
  side.appendChild(cap(t.cap));
  row.appendChild(side);
  s.appendChild(row);
  s.appendChild(folio(3,true));
  return s;
}
function pageContents(t){
  var s=el("article","sheet");
  s.appendChild(el("p","run",esc(t.run)));
  var row=el("div"); row.style.display="grid"; row.style.gridTemplateColumns="1.35fr .75fr"; row.style.gap="1em"; row.style.minHeight="0"; row.style.flex="1";
  var main=el("div");
  main.appendChild(el("p","kicker",esc(t.kicker)));
  main.appendChild(el("h1","",esc(t.title)));
  main.appendChild(el("hr","rule"));
  var ul=el("ol","toc");
  (t.items||[]).forEach(function(it){
    var li=el("li");
    li.innerHTML="<span class='num'>"+esc(it.n)+"</span><span><b>"+esc(it.t)+"</b> <i>"+esc(it.d)+"</i></span>";
    ul.appendChild(li);
  });
  main.appendChild(ul);
  row.appendChild(main);
  var side=el("div");
  var ph=crop(4,0,t.fig); if(ph) side.appendChild(ph);
  side.appendChild(cap(t.fig));
  (t.pub||[]).forEach(function(line){ var p=el("p","cap"); p.textContent=line; side.appendChild(p); });
  row.appendChild(side);
  s.appendChild(row);
  s.appendChild(folio(4,false));
  return s;
}
function pageMap(t){
  var s=el("article","sheet");
  s.appendChild(el("p","run",esc(t.run)));
  s.appendChild(el("p","kicker",esc(t.kicker)));
  s.appendChild(el("h1","",esc(t.title)));
  s.appendChild(el("hr","rule"));
  var ph=crop(5,0,t.title); if(ph) s.appendChild(ph);
  var g=el("div","pills");
  (t.places||[]).forEach(function(it){
    var d=el("div"); d.innerHTML="<b>"+esc(it.t)+"</b>"+esc(it.d); g.appendChild(d);
  });
  s.appendChild(g);
  var note=el("p","cap"); note.textContent=t.note||""; s.appendChild(note);
  s.appendChild(folio(5,true));
  return s;
}
function pageOpener(n,t){
  var s=el("article","sheet"); s.style.padding="0"; s.style.gap="0";
  var ph=crop(n,0,t.cap); if(ph) s.appendChild(ph);
  var body=el("div"); body.style.padding="3.5% 5.5% 4%"; body.style.display="flex"; body.style.flexDirection="column"; body.style.gap=".4em"; body.style.flex="1";
  body.appendChild(el("p","kicker",esc(t.kicker)));
  body.appendChild(el("h1","",esc(t.title)));
  body.appendChild(el("hr","rule"));
  var row=el("div","split");
  var stand=el("p","stand"); stand.textContent=t.stand||""; row.appendChild(stand);
  var side=el("div","aside");
  if(t.cap) side.appendChild(cap((L.above?L.above+" ":"")+t.cap));
  if(t.feature&&t.feature.length){
    side.appendChild(el("h3","",esc(L.feature||"")));
    var ul=el("ul");
    t.feature.forEach(function(f){ul.appendChild(el("li", "", esc(f)))});
    side.appendChild(ul);
  }
  row.appendChild(side);
  body.appendChild(row);
  body.appendChild(folio(n, n%2===0));
  s.appendChild(body);
  return s;
}
function pageBleed(n,t){
  var s=el("article","sheet"); s.style.padding="0"; s.style.position="relative";
  var ph=crop(n,0,t.title); if(ph) s.appendChild(ph);
  var over=el("div"); over.style.position="absolute"; over.style.insetInlineStart="6%"; over.style.top="5%"; over.style.maxWidth="70%"; over.style.color="#fff"; over.style.textShadow="0 1px 8px rgba(0,0,0,.45)";
  over.appendChild(el("p","kicker",esc(t.kicker)));
  var h=el("h1"); h.style.color="#fff"; h.textContent=t.title; over.appendChild(h);
  s.appendChild(over);
  var band=el("div","navy"); band.style.padding="3.5% 5.5%"; band.style.display="flex"; band.style.flexDirection="column"; band.style.gap=".4em";
  var row=el("div","split");
  var stand=el("p","stand"); stand.textContent=t.stand||""; row.appendChild(stand);
  row.appendChild(cap((L.above?L.above+" ":"")+ (t.cap||"")));
  band.appendChild(row);
  band.appendChild(folio(n,true));
  s.appendChild(band);
  return s;
}
function photoGrid(n,t,from,to){
  var boxes=BOX[n]||[];
  var count=Math.max(0,(to==null?boxes.length:to)-from);
  if(!count) return null;
  var g=el("div","phrow");
  g.style.display="flex";
  g.style.flexWrap="wrap";
  g.style.alignItems="flex-start";
  g.style.justifyContent="space-between";
  g.style.gap=".45em";
  for(var i=from;i<(to==null?boxes.length:to);i++){
    var cell=el("div");
    var c=crop(n,i,(t.caps||[])[i]); if(c) cell.appendChild(c);
    if(t.caps&&t.caps[i]) cell.appendChild(cap(t.caps[i]));
    g.appendChild(cell);
  }
  return g;
}
function pageStory(n,t){
  var s=el("article","sheet");
  if(t.run) s.appendChild(el("p","run",esc(t.run)));
  if(t.kicker) s.appendChild(el("p","kicker",esc(t.kicker)));
  if(t.title){ s.appendChild(el("h1","",esc(t.title))); s.appendChild(el("hr","rule")); }
  if(t.deck){ var deck=el("p","stand"); deck.textContent=t.deck; s.appendChild(deck); }
  var boxes=BOX[n]||[];
  var start=0;
  if(t.photoTop && boxes.length){
    var g0=photoGrid(n,t,0,1); if(g0) s.appendChild(g0);
    start=1;
  }
  var row=el("div","split");
  var main=el("div");
  var list=t.paras||[];
  main.appendChild(paras(list, !!t.drop));
  if(list.length>=3 && !t.wide) main.querySelector(".paras").classList.add(list.length>5?"cols3":"cols");
  row.appendChild(main);
  if(t.side) row.appendChild(aside(t.sideTitle, t.side));
  else if(t.miss) row.appendChild(aside(L.miss, t.miss));
  else row.style.gridTemplateColumns="1fr";
  if((t.paras&&t.paras.length) || t.side || t.miss) s.appendChild(row);
  var rest=photoGrid(n,t,start,null); if(rest) s.appendChild(rest);
  if(t.quote){
    var q=el("p","quote"); q.textContent=t.quote; s.appendChild(q);
    if(t.quoteBy){ var by=el("p","cap"); by.textContent=t.quoteBy; s.appendChild(by); }
  }
  if(t.rows){
    s.appendChild(el("h2","",esc(t.tableTitle||"")));
    var table=el("table","table");
    table.innerHTML="<thead><tr><th>"+esc((t.tableHead&&t.tableHead[0])||"")+"</th><th>"+esc((t.tableHead&&t.tableHead[1])||"")+"</th></tr></thead>";
    var tb=document.createElement("tbody");
    t.rows.forEach(function(r){ var tr=document.createElement("tr"); tr.innerHTML="<td>"+esc(r.s)+"</td><td>"+esc(r.w)+"</td>"; tb.appendChild(tr); });
    table.appendChild(tb); s.appendChild(table);
  }
  if(t.promo){ var pr=el("p","promo"); pr.textContent=t.promo; s.appendChild(pr); }
  s.appendChild(folio(n, n%2===1));
  return s;
}
function pageTimeline(t){
  var s=el("article","sheet");
  s.appendChild(el("p","run",esc(t.run)));
  s.appendChild(el("p","kicker",esc(t.kicker)));
  s.appendChild(el("h1","",esc(t.title)));
  s.appendChild(el("hr","rule"));
  var ul=el("ol","events");
  (t.events||[]).forEach(function(ev){
    var li=el("li"); li.innerHTML="<b>"+esc(ev.y)+"</b><span>"+esc(ev.t)+"</span>"; ul.appendChild(li);
  });
  s.appendChild(ul);
  if(t.note){ var n=el("p","cap"); n.textContent=t.note; s.appendChild(n); }
  s.appendChild(folio(17,true));
  return s;
}
function pageItinerary(n,t){
  var s=el("article","sheet");
  s.appendChild(el("p","kicker",esc(t.kicker)));
  s.appendChild(el("p","route",esc(t.tour))); 
  var rt=s.querySelector(".route"); if(rt) rt.style.color="var(--gold)";
  s.appendChild(el("h1","",esc(t.title)));
  if(t.deck){ var d=el("p","stand"); d.textContent=t.deck; s.appendChild(d); }
  var ul=el("ol","days");
  (t.days||[]).forEach(function(day){
    var li=el("li");
    li.innerHTML="<div class='dn'>"+esc(L.day||"DAY")+"<br>"+esc(day.n)+"</div><div><h3>"+esc(day.title)+"</h3><p class='route'>"+esc(day.route||"")+"</p><p>"+esc(day.text||"")+"</p>"+(day.stay?"<p><b>"+esc(L.overnight||"")+"</b> "+esc(day.stay)+"</p>":"")+"</div>";
    ul.appendChild(li);
  });
  s.appendChild(ul);
  s.appendChild(folio(n,false));
  return s;
}
function pageIncluded(n,t){
  var s=el("article","sheet"); s.style.padding="0"; s.style.gap="0";
  var ph=crop(n,0,t.scan); if(ph) s.appendChild(ph);
  var band=el("div","navy"); band.style.padding="3.5% 5.5%"; band.style.flex="1"; band.style.display="flex"; band.style.flexDirection="column"; band.style.gap=".45em";
  var row=el("div","split");
  var inc=el("div"); inc.appendChild(el("h2","",esc(L.included||"")));
  var ul=el("ul"); (t.included||[]).forEach(function(x){ul.appendChild(el("li","",esc(x)))}); inc.appendChild(ul);
  row.appendChild(inc);
  var right=el("div");
  right.appendChild(el("h3","",esc(L.excluded||"")));
  var ex=el("p"); ex.textContent=t.excluded||""; right.appendChild(ex);
  right.appendChild(el("h3","",esc(L.good||"")));
  var g=el("p"); g.textContent=t.good||""; right.appendChild(g);
  row.appendChild(right);
  band.appendChild(row);
  var scan=el("p"); scan.innerHTML="<b>"+esc(L.scan||"")+"</b><br><a href='"+esc(homeOf(M.lang))+"' style='color:#fff'>"+esc(t.url||"iraq.fabletour.com")+"</a><br>"+esc(t.phone||"");
  band.appendChild(scan);
  band.appendChild(folio(n,true));
  s.appendChild(band);
  return s;
}
function pageGuide(t){
  var s=el("article","sheet");
  s.appendChild(el("p","kicker",esc(t.kicker)));
  s.appendChild(el("h1","",esc(t.title)));
  s.appendChild(el("hr","rule"));
  var g=el("div"); g.style.columnCount="3"; g.style.columnGap="1em"; g.style.fontSize=".92em";
  (t.groups||[]).forEach(function(gr){
    var b=el("div"); b.style.breakInside="avoid"; b.style.marginBottom=".7em";
    b.appendChild(el("h3","",esc(gr.h)));
    (gr.items||[]).forEach(function(it){
      var p=el("p"); p.innerHTML="<b>"+esc(it.t)+"</b> "+esc(it.d); b.appendChild(p);
    });
    g.appendChild(b);
  });
  s.appendChild(g);
  if(t.note){
    var note=el("div","note");
    note.innerHTML="<b>"+esc(t.noteTitle||"")+"</b> "+esc(t.note);
    s.appendChild(note);
  }
  s.appendChild(folio(38,false));
  return s;
}
function pageBooking(t){
  var s=el("article","sheet");
  s.appendChild(el("p","run",esc(t.run)));
  s.appendChild(el("p","kicker",esc(t.kicker)));
  s.appendChild(el("h1","",esc(t.title)));
  var intro=el("p","stand"); intro.textContent=t.intro||""; s.appendChild(intro);
  var cards=el("div","cards");
  var links=["/tours/iraq-6-day-tour/","/tours/iraq-7-day-tour/","/tours/iraq-9-day-tour/"];
  if(M.lang!=="ar"&&M.lang!=="en") links=links.map(function(u){return "/"+M.lang+u});
  if(M.lang==="en") links=links.map(function(u){return "/en"+u});
  (t.cards||[]).forEach(function(c,i){
    var d=el("div","cardm");
    d.innerHTML="<div class='num'>"+esc(c.days)+"</div><h3>"+esc(c.title)+"</h3><p>"+esc(c.text)+"</p><a href='"+esc(links[i]||homeOf(M.lang))+"'>"+esc(c.scan||L.scan||"")+"</a>";
    cards.appendChild(d);
  });
  s.appendChild(cards);
  var row=el("div","split");
  var how=el("div"); how.appendChild(el("h3","",esc(t.howTitle||""))); var hp=el("p"); hp.textContent=t.how||""; how.appendChild(hp);
  var contact=el("div"); contact.appendChild(el("h3","",esc(t.contactTitle||"")));
  (t.lines||[]).forEach(function(line){ var p=el("p","cap"); p.textContent=line; contact.appendChild(p); });
  row.appendChild(how); row.appendChild(contact); s.appendChild(row);
  if(t.promo){ var pr=el("p","promo"); pr.textContent=t.promo; s.appendChild(pr); }
  s.appendChild(folio(39,true));
  return s;
}
function pageClose(t){
  var s=el("article","sheet"); s.style.padding="0"; s.style.gap="0";
  var ph=crop(40,0,t.credit); if(ph) s.appendChild(ph);
  var body=el("div"); body.style.padding="4% 8%"; body.style.textAlign="center"; body.style.flex="1"; body.style.display="flex"; body.style.flexDirection="column"; body.style.justifyContent="center";
  body.appendChild(el("h1","",esc(t.title)));
  body.appendChild(el("hr","rule")); var rule=body.querySelector(".rule"); if(rule){rule.style.marginInline="auto"}
  var p=el("p"); p.textContent=t.text||""; body.appendChild(p);
  var row=el("div","logo-row"); row.style.justifyContent="center"; row.style.marginTop="1em";
  var img=document.createElement("img"); img.src="/logo.png"; img.alt="Fable Tour";
  var info=el("div"); info.style.textAlign="start";
  [t.url,t.email,t.phone,t.service,t.address].forEach(function(line){ if(line){ var q=el("p","cap"); q.textContent=line; info.appendChild(q);} });
  row.appendChild(img); row.appendChild(info); body.appendChild(row);
  var a=el("a"); a.href=homeOf(M.lang); a.textContent=t.scan||""; a.style.marginTop=".6em"; body.appendChild(a);
  var cr=el("p","credit"); cr.textContent=t.credit||""; cr.style.color="var(--gold)"; body.appendChild(cr);
  s.appendChild(body);
  return s;
}

function build(n){
  var t=P[String(n)]||P[n]||{};
  var sheet;
  if(n===1) sheet=pageCover(t);
  else if(n===2) sheet=pageWelcome(t);
  else if(n===3) sheet=pageLetter(t);
  else if(n===4) sheet=pageContents(t);
  else if(n===5) sheet=pageMap(t);
  else if(n===6||n===10||n===14||n===22||n===28) sheet=pageOpener(n,t);
  else if(n===18||n===25) sheet=pageBleed(n,t);
  else if(n===17) sheet=pageTimeline(t);
  else if(n===34||n===36) sheet=pageItinerary(n,t);
  else if(n===35||n===37) sheet=pageIncluded(n,t);
  else if(n===38) sheet=pageGuide(t);
  else if(n===39) sheet=pageBooking(t);
  else if(n===40) sheet=pageClose(t);
  else sheet=pageStory(n,t);
  var pg=el("div","pg");
  if(n===1||n===40) pg.setAttribute("data-density","hard");
  pg.appendChild(sheet);
  return pg;
}

function fit(){ /* pages are pinned to the book; long translations scroll inside the sheet */ }

var book=document.getElementById("book");
for(var i=1;i<=40;i++) book.appendChild(build(i));

document.getElementById("hint").textContent=ui.hint||"";
document.getElementById("load").textContent=M.brand||"MESOPOTAMIA";
[["first",ui.first],["prev",ui.prev],["next",ui.next],["snd",ui.sound],["fs",ui.full]].forEach(function(pair){
  var b=document.getElementById(pair[0]); if(b&&pair[1]) b.setAttribute("aria-label",pair[1]);
});
var sel=document.getElementById("magLang");
LANGS.forEach(function(pair){
  var o=document.createElement("option");
  o.value=pair[0]; o.textContent=pair[1];
  if(pair[0]===M.lang) o.selected=true;
  sel.appendChild(o);
});
sel.addEventListener("change",function(){ location.href=hrefOf(sel.value); });

var N=40, W=1075, H=1521;
var startPage=0;
try{ var qm=/[?#&]p=(\d+)/.exec(location.href); if(qm) startPage=Math.max(0, Math.min(N-1, (+qm[1])-1)); }catch(e){}
var pf=new St.PageFlip(book,{width:W,height:H,size:"stretch",minWidth:280,maxWidth:1300,minHeight:280,maxHeight:1840,
  showCover:true,maxShadowOpacity:.45,mobileScrollSupport:false,flippingTime:850,usePortrait:true,autoSize:true,drawShadow:true,startPage:startPage});
pf.loadFromHTML(book.querySelectorAll(".pg"));
var stage=document.getElementById("stage"), wrap=document.getElementById("wrap");
function doFit(){ book.querySelectorAll(".pg").forEach(fit); }
function fitStage(){
  var sw=stage.clientWidth-16, sh=stage.clientHeight-8;
  var wl=Math.min(sw, sh*2*W/H), portrait=wl<=680;
  var ratio=portrait?W/H:2*W/H;
  var w=portrait?Math.min(sw, sh*ratio, 680):wl;
  wrap.style.width=Math.floor(w)+"px"; wrap.style.height=Math.floor(w/ratio)+"px";
  try{pf.update()}catch(e){}
  setTimeout(doFit, 40);
}
window.addEventListener("resize", fitStage); fitStage(); setTimeout(fitStage, 200);

var ctx=null, soundOn=true;
function swish(){
  if(!soundOn) return;
  try{
    var AC=window.AudioContext||window.webkitAudioContext; if(!AC) return;
    if(!ctx) ctx=new AC(); if(ctx.state==="suspended") ctx.resume();
    var dur=.42, sr=ctx.sampleRate, buf=ctx.createBuffer(1, Math.floor(sr*dur), sr), ch=buf.getChannelData(0), last=0;
    for(var i=0;i<ch.length;i++){var t=i/ch.length, wh=Math.random()*2-1; last=(last+.12*wh)/1.12;
      var env=Math.pow(Math.sin(Math.PI*Math.min(1,t*1.15)),1.6)*(1-.35*t);
      ch[i]=(wh*.55+last*3.2)*env;}
    var s=ctx.createBufferSource(); s.buffer=buf;
    var bp=ctx.createBiquadFilter(); bp.type="bandpass"; bp.Q.value=.7;
    var t0=ctx.currentTime; bp.frequency.setValueAtTime(900,t0); bp.frequency.exponentialRampToValueAtTime(4200,t0+dur*.55);
    var g=ctx.createGain(); g.gain.value=.45;
    s.connect(bp); bp.connect(g); g.connect(ctx.destination); s.start();
  }catch(e){}
}
var count=document.getElementById("count"), hint=document.getElementById("hint"), prev=document.getElementById("prev"), next=document.getElementById("next"), first=document.getElementById("first");
function uiState(){var p=pf.getCurrentPageIndex(); count.textContent=(p+1)+" / "+N; prev.disabled=first.disabled=p<=0; next.disabled=p>=N-1;}
pf.on("flip",function(){uiState(); hint.style.opacity=0; setTimeout(doFit,30)});
pf.on("changeState",function(e){if(e.data==="flipping") swish()});
pf.on("init",function(){book.classList.add("ready"); document.getElementById("load").style.display="none"; uiState(); setTimeout(doFit,80)});
setTimeout(function(){book.classList.add("ready"); document.getElementById("load").style.display="none"; uiState(); doFit()}, 900);
function goNext(){pf.flipNext()}
function goPrev(){pf.flipPrev()}
prev.onclick=goPrev; next.onclick=goNext; first.onclick=function(){pf.flip(0)};
document.addEventListener("keydown",function(e){
  if(e.key==="ArrowRight") (rtl?goPrev:goNext)();
  if(e.key==="ArrowLeft") (rtl?goNext:goPrev)();
});
var snd=document.getElementById("snd");
snd.onclick=function(){soundOn=!soundOn; snd.setAttribute("aria-pressed", soundOn?"true":"false"); document.getElementById("w").style.display=soundOn?"":"none"; snd.style.opacity=soundOn?1:.55};
var fs=document.getElementById("fs");
fs.onclick=function(){
  var node=document.documentElement;
  if(window.self!==window.top){window.open(location.href,"_blank"); return}
  if(document.fullscreenElement) document.exitFullscreen();
  else if(node.requestFullscreen) node.requestFullscreen();
};
})();
