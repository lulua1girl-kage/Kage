from pathlib import Path

repo=Path(".").resolve()
project=repo/".nori-v36"/"v364-connect"
www=project/"www"

parts=sorted((repo/"sources/jarvis").glob("part-*.html"))
if len(parts)!=3:
    raise SystemExit("Expected three Jarvis source parts")
jarvis=www/"jarvis.html"
jarvis.write_text("".join(p.read_text(encoding="utf-8") for p in parts),encoding="utf-8")
s=jarvis.read_text(encoding="utf-8")

bridge='''<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script>
(function(){
const U="https://qrlvkxewyoceykaquapv.supabase.co",K="sb_publishable_3QSgkXgNWRa82Z2ID6n7Ag_QdvmH92_";
let c=null;try{c=window.supabase?.createClient(U,K)}catch(e){}
const L=k=>{try{return JSON.parse(localStorage.getItem("kage.jarvis."+k)||"null")}catch(e){return null}};
const S=(k,v)=>{try{localStorage.setItem("kage.jarvis."+k,JSON.stringify(v))}catch(e){}};
const img=f=>!f?Promise.resolve(null):new Promise((ok,no)=>{const r=new FileReader();r.onload=()=>ok(r.result);r.onerror=no;r.readAsDataURL(f)});
window.__KAGE_JARVIS_BRIDGE={client:c,localLoad:L,localSave:S,imageData:img,url:U,key:K};
})();
</script>
'''
s=s.replace("<script>\nconst AVATAR_MAIN",bridge+"<script>\nconst AVATAR_MAIN",1)

old="""  try{
    db = await window.claude?.use?.('db') ?? null;
    user = await window.claude?.use?.('user') ?? null;
    sample = await window.claude?.use?.('sample') ?? null;
  }catch(e){}
  if(user){ try{ uid = await user.id(); }catch(e){ uid=null; } }
"""
new="""  try{
    const b=window.__KAGE_JARVIS_BRIDGE;
    db=null;
    const ss=b?.client ? await b.client.auth.getSession() : {data:{session:null}};
    user=ss?.data?.session?.user||null; uid=user?.id||null;
    sample=async function(prompt,opts={}){
      const sess=b?.client ? (await b.client.auth.getSession()).data.session : null;
      if(!sess) throw new Error("SIGN_IN_REQUIRED");
      const message=Array.isArray(prompt)?prompt.map(x=>String(x?.content||x?.text||"")).join("\n"):String(prompt||"");
      const imageDataUrl=opts.images?await b.imageData(opts.images):null;
      const state={profile,memory,weakAreas,progress,drillStats,blockState,examPrep,studyNotes,mistakePatterns,ladder,rewards,excuseLog};
      const r=await fetch(b.url+"/functions/v1/nori-brain",{method:"POST",headers:{Authorization:"Bearer "+sess.access_token,apikey:b.key,"Content-Type":"application/json"},body:JSON.stringify({message,history:chatHistory.slice(-12),stateSummary:state,brainContext:{source:"jarvis-merged",mode:convoMode,mentorOn,voiceCallActive},nextMove:null,imageDataUrl})});
      const j=await r.json().catch(()=>({}));
      if(!r.ok||!j.ok) throw new Error(j.error||"NORI_BRAIN_UNAVAILABLE");
      return {text:j.reply||j.text||"",provider:j.provider,model:j.model};
    };
  }catch(e){sample=null}
  try{
    const b=window.__KAGE_JARVIS_BRIDGE;
    profile=Object.assign(profile,b.localLoad("profile")||{});
    memory=b.localLoad("memory")||memory; weakAreas=b.localLoad("weakAreas")||weakAreas; recap=b.localLoad("recap")||recap;
    examPrep=b.localLoad("examPrep")||examPrep; studyNotes=b.localLoad("studyNotes")||studyNotes;
    mistakePatterns=Object.assign(mistakePatterns,b.localLoad("mistakePatterns")||{});
    ladder=Object.assign(ladder,b.localLoad("ladder")||{}); rewards=Object.assign(rewards,b.localLoad("rewards")||{});
    excuseLog=b.localLoad("excuseLog")||excuseLog; chatHistory=b.localLoad("chatHistory")||chatHistory;
    drillStats=Object.assign(drillStats,b.localLoad("drillStats")||{}); progress=Object.assign(progress,b.localLoad("progress")||{});
    flashcards=b.localLoad("flashcards")||flashcards; blockState=Object.assign(blockState,b.localLoad("blockState")||{}); alarms=b.localLoad("alarms")||alarms;
  }catch(e){}
"""
if old not in s: raise SystemExit("Jarvis boot block not found")
s=s.replace(old,new,1)

repls={
"const persistProfile = debounced(async ()=>{ if(profileDocRef) try{ await profileDocRef.set({profile, memory, weakAreas, recap, examPrep, studyNotes, mistakePatterns, ladder, rewards, excuseLog}); }catch(e){} }, 400);":"const persistProfile = debounced(async ()=>{const b=window.__KAGE_JARVIS_BRIDGE;b?.localSave('profile',profile);b?.localSave('memory',memory);b?.localSave('weakAreas',weakAreas);b?.localSave('recap',recap);b?.localSave('examPrep',examPrep);b?.localSave('studyNotes',studyNotes);b?.localSave('mistakePatterns',mistakePatterns);b?.localSave('ladder',ladder);b?.localSave('rewards',rewards);b?.localSave('excuseLog',excuseLog);if(profileDocRef)try{await profileDocRef.set({profile,memory,weakAreas,recap,examPrep,studyNotes,mistakePatterns,ladder,rewards,excuseLog})}catch(e){}},400);",
"const persistChat = debounced(async ()=>{ if(chatDocRef) try{ await chatDocRef.set({messages: chatHistory.slice(-40)}); }catch(e){} }, 500);":"const persistChat = debounced(async ()=>{window.__KAGE_JARVIS_BRIDGE?.localSave('chatHistory',chatHistory.slice(-40));if(chatDocRef)try{await chatDocRef.set({messages:chatHistory.slice(-40)})}catch(e){}},500);",
"const persistDrillStats = debounced(async ()=>{ if(drillDocRef) try{ await drillDocRef.set(drillStats); }catch(e){} }, 500);":"const persistDrillStats = debounced(async ()=>{window.__KAGE_JARVIS_BRIDGE?.localSave('drillStats',drillStats);if(drillDocRef)try{await drillDocRef.set(drillStats)}catch(e){}},500);",
"const persistProgress = debounced(async ()=>{ if(progressDocRef) try{ await progressDocRef.set(progress); }catch(e){} }, 400);":"const persistProgress = debounced(async ()=>{window.__KAGE_JARVIS_BRIDGE?.localSave('progress',progress);if(progressDocRef)try{await progressDocRef.set(progress)}catch(e){}},400);",
"const persistCards = debounced(async ()=>{ if(cardsDocRef) try{ await cardsDocRef.set({cards:flashcards}); }catch(e){} }, 400);":"const persistCards = debounced(async ()=>{window.__KAGE_JARVIS_BRIDGE?.localSave('flashcards',flashcards);if(cardsDocRef)try{await cardsDocRef.set({cards:flashcards})}catch(e){}},400);",
"const persistBlock = debounced(async ()=>{ if(blockDocRef) try{ await blockDocRef.set(blockState); }catch(e){} }, 300);":"const persistBlock = debounced(async ()=>{window.__KAGE_JARVIS_BRIDGE?.localSave('blockState',blockState);if(blockDocRef)try{await blockDocRef.set(blockState)}catch(e){}},300);",
"const persistAlarms = debounced(async ()=>{ if(alarmDocRef) try{ await alarmDocRef.set({alarms}); }catch(e){} }, 300);":"const persistAlarms = debounced(async ()=>{window.__KAGE_JARVIS_BRIDGE?.localSave('alarms',alarms);if(alarmDocRef)try{await alarmDocRef.set({alarms})}catch(e){}},300);"
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit("persist function missing")
    s=s.replace(a,b,1)
s=s.replace("setStatus('online · memory synced');","setStatus(sample?'online · Nori Brain connected':'local mode · sign in for AI');")
s=s.replace("setStatus(sample ? 'online · memory local to this device' : 'preview mode');","setStatus(sample?'online · Nori Brain connected':'local mode · sign in for AI');")
jarvis.write_text(s,encoding="utf-8")

# IMPORTANT: the inspected V36.5 base already has the intended Home / Recover / Study /
# Tracker / Profile command suite and bottom navigation. Do not replace it with JARVIS.
# JARVIS is kept as an integrated tool page only.
idx=www/"index.html"
x=idx.read_text(encoding="utf-8")
# no navigation injection

p=www/"nori-system-directory-v34.js"
q=p.read_text(encoding="utf-8")
if "'danatbayu@gmail.com'" not in q and "'danatbayu9@gmail.com'" in q:
  q=q.replace("'danatbayu9@gmail.com'","'danatbayu@gmail.com','mirasutton58@gmail.com','justicesteve.councle@gmail.com'",1)
elif "'mirasutton58@gmail.com'" not in q:
  raise SystemExit("Could not find existing admin allowlist anchor")
p.write_text(q,encoding="utf-8")
print("KAGE merge complete: preservation-first, no shell/nav replacement")
