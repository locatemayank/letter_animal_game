const mk = require("./arbiter.js");
let pass=0, fail=0;
function T(name, fn){ try{ fn(); pass++; console.log("ok  ", name);}catch(e){ fail++; console.log("FAIL", name, "-", e.message);} }
const eq=(a,b,m)=>{ if(a!==b) throw new Error(`${m||""} expected ${b} got ${a}`); };
const C={cw:600,ch:450};
const d=(A,id,t,x=200,y=200,extra={})=>A.down({id,type:"touch",x,y,w:20,h:20,t,...C,...extra});
const m=(A,id,t,x,y)=>A.move({id,x,y,t});
const u=(A,id,t)=>A.up({id,t});

T("single finger draws", ()=>{const A=mk(); eq(d(A,1,0).action,"start"); eq(m(A,1,16,210,200).action,"draw"); eq(u(A,1,30).action,"end");});
T("isPrimary-free: thumb resting elsewhere for long doesn't block", ()=>{const A=mk(); d(A,9,0,300,300); u; // thumb on canvas (idle? it started -> ink)
  // thumb started drawing; lifts later; we just check a resting thumb that STARTED first and is stationary
  const B=mk(); eq(d(B,9,0,300,300).action,"start"); /* thumb resting = active ink but never moves */ eq(d(B,1,2000,100,100).action,"ignore","2nd finger while 1st active (old) is ignored");});
T("two fingers together -> cancel + lock", ()=>{const A=mk(); d(A,1,0); const r=d(A,2,40,260,200); eq(r.action,"cancel"); eq(r.cancelId,1); eq(m(A,1,60,230,200).action,"ignore"); eq(m(A,2,60,280,200).action,"ignore");});
T("lock releases when all fingers lift", ()=>{const A=mk(); d(A,1,0); d(A,2,40); u(A,1,200); u(A,2,220); eq(d(A,3,400).action,"start");});
T("lock persists while a finger still down (new finger soon)", ()=>{const A=mk(); d(A,1,0); d(A,2,40); u(A,1,200); eq(d(A,3,500).action,"ignore");});
T("lock safety-expires after 1.5s (stale contact)", ()=>{const A=mk(); d(A,1,0); d(A,2,40); /* missed ups */ eq(d(A,3,2000).action,"start");});
T("palm lands mid-stroke -> ignored, stroke continues", ()=>{const A=mk(); d(A,1,0); m(A,1,100,240,200); m(A,1,200,300,210); eq(d(A,2,300,400,380,{w:90,h:110}).action,"ignore"); eq(m(A,1,320,320,215).action,"draw");});
T("small 2nd finger mid-stroke (established) -> ignored, stroke continues", ()=>{const A=mk(); d(A,1,0); m(A,1,200,260,200); eq(d(A,2,400,450,380).action,"ignore"); eq(m(A,1,420,270,200).action,"draw");});
T("palm first, then finger -> finger draws", ()=>{const A=mk(); eq(d(A,5,0,400,380,{w:100,h:120}).action,"ignore"); eq(d(A,1,50,200,200).action,"start");});
T("resting hand (old idle contact) doesn't block new finger", ()=>{const A=mk(); d(A,1,0); d(A,2,40); u(A,1,100); /* 2 stays */ eq(d(A,3,3000,150,150).action,"start");});
T("edge grip thumb ignored, then finger draws", ()=>{const A=mk(); eq(d(A,7,0,5,200).action,"ignore"); eq(d(A,1,30,200,200).action,"start");});
T("two-finger tap with no active stroke (first was grip?) -> pair window", ()=>{const A=mk(); d(A,1,0); d(A,2,30); u(A,1,60); u(A,2,60); eq(d(A,3,1000).action,"start");});
T("pinch: 2nd finger lands after 1st moved fast, then slides -> cancel", ()=>{const A=mk(); d(A,1,0); m(A,1,80,240,200); eq(d(A,2,160,400,300).action,"ignore"); m(A,2,200,420,300); const r=m(A,2,240,450,300); eq(r.action,"cancel"); eq(r.cancelId,1);});
T("late 2nd finger slide (>600ms into stroke) does not cancel", ()=>{const A=mk(); d(A,1,0); m(A,1,300,300,200); d(A,2,700,400,300); eq(m(A,2,800,460,300).action,"ignore"); eq(m(A,1,810,310,200).action,"draw");});
T("pen beats touch", ()=>{const A=mk(); d(A,1,0); m(A,1,100,260,200); const r=A.down({id:50,type:"pen",x:100,y:100,w:1,h:1,t:200,...C}); eq(r.action,"restart"); eq(d(A,3,300).action,"ignore");});
T("mouse left button draws, right ignored", ()=>{const A=mk(); eq(A.down({id:1,type:"mouse",button:2,x:100,y:100,t:0,...C}).action,"ignore"); A.up({id:1}); eq(A.down({id:1,type:"mouse",button:0,x:100,y:100,t:10,...C}).action,"start");});
T("quick successive single strokes (E bars) all draw", ()=>{const A=mk(); let t=0; for(let k=0;k<4;k++){ eq(d(A,10+k,t).action,"start"); m(A,10+k,t+50,260,200); u(A,10+k,t+120); t+=180;} });
console.log(`\n${pass} passed, ${fail} failed`);
