import gradio as gr, asyncio, edge_tts, uuid, random, requests, re, os, json, urllib.parse, datetime
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip
from moviepy.audio.fx.volumex import volumex

CONTACT = "03043399133 | 03022246271"
BRAND_NAME = "JSM AI BY JAM SAEED MOTHA"

SUPABASE_KEY = "sb_publishable_1W4NK6X7Edacm_eSB1cFDQ_CkT6c4EY"
PIXABAY_KEY = "56386293-14facd94fdac26f9fc37f5f2c"
COVERR_API_KEY = "8c8c592b07a57e05dc49368c399b7659"

PEXELS_KEYS = [
    "ROKJvfYuuSkc7QVVL6VjCgYFyB8UQZCLLCctD2SfTJclrDGo5Ex3JMX6",
    "zniYavhal66VGwuV2kUlpRm7vG3Y0rddDLuzrlTvmPqQ26kdG0vcyy0",
    "f6lKxrHR8MHj1geD62crLTfDTQX0s7ewFkw3hEl4d4CenRTZXCkpCWD9",
    "1j6kFq1GRB4291F1s1RMGhlgIX3d3u78OaTpiDKmtlSAjJkKPb9vVTkL",
    "tpkypogswv07n84dh0iaHI9tamu43GEcvZokA3Xi3JSTUT0NV32A6gG9"
]

VOICES = {"English Male (Andrew)": "en-US-AndrewNeural","Urdu Male (Asad)": "ur-PK-AsadNeural","Hindi Male (Arjun)": "hi-IN-ArjunNeural"}
BASE_DIR = "./JSM_Outputs"; os.makedirs(BASE_DIR, exist_ok=True)
LICENSE_DB = os.path.join(BASE_DIR, "jsm_licenses_final.json")
FREE_DB = os.path.join(BASE_DIR, "free_daily.json")

FIXED_LICENSES = {"AREEJ786": {"bound_email": "", "total": 300.0, "used": 0.0, "expiry": "2030-12-31"},"JSM500": {"bound_email": "", "total": 500.0, "used": 0.0, "expiry": "2030-12-31"}}

CATEGORIES_MAP = {
    "medical": ["doctor", "hospital", "patient", "health", "surgery"], "engineering": ["engineer", "construction", "building", "bridge"],
    "software": ["coding", "software", "developer", "laptop"], "ai_tech": ["ai", "robot", "artificial intelligence", "technology"],
    "finance": ["money", "bitcoin", "trading", "bank", "wealth"], "business": ["corporate", "office", "meeting", "startup"],
    "e_commerce": ["shopping", "delivery", "ecommerce", "package"], "farming": ["farmer", "tractor", "agriculture", "field", "crop"],
    "real_estate": ["house", "property", "mansion", "apartment"], "storytelling": ["history", "kingdom", "warrior", "castle", "book"],
    "fitness": ["gym", "workout", "bodybuilding", "exercise"], "food": ["cooking", "chef", "restaurant", "recipe"],
    "travel": ["travel", "airplane", "beach", "hotel"], "education": ["student", "school", "university", "teacher"],
    "gaming": ["gaming", "gamer", "esports", "playstation"], "fashion": ["fashion", "model", "clothing", "style"],
    "automotive": ["car", "supercar", "mechanic", "racing"], "nature": ["forest", "river", "ocean", "sunset"],
    "space": ["space", "astronaut", "planet", "rocket"], "law": ["lawyer", "court", "judge", "police"],
    "science": ["laboratory", "chemistry", "experiment"], "music": ["musician", "guitar", "piano", "concert"],
    "art": ["painting", "artist", "design"], "pets": ["dog", "cat", "animals"], "beauty": ["makeup", "salon", "haircut"],
    "security": ["cybersecurity", "hacker", "cctv"], "crypto": ["blockchain", "ethereum", "nft"],
    "marketing": ["social media", "marketing", "seo"], "motivational": ["success", "motivation", "goal", "trophy"],
    "mindfulness": ["meditation", "peace", "calm"], "news": ["breaking news", "reporter", "media"],
    "military": ["army", "soldier", "navy"], "logistics": ["truck", "shipping", "warehouse"],
    "energy": ["solar energy", "wind turbine", "electricity"], "islamic": ["mosque", "quran", "prayer", "allah"],
    "village": ["village", "rural", "market"], "sports": ["cricket", "football", "stadium"],
    "technology": ["mobile", "gadget", "smartphone"], "cooking": ["cook", "kitchen", "dish"],
    "wedding": ["wedding", "bride", "groom"], "kids": ["kids", "toys", "children"],
    "animals": ["lion", "wildlife", "zoo"], "weather": ["rain", "weather", "storm"],
    "politics": ["politics", "election", "leader"], "religion": ["church", "temple", "religious"],
    "history": ["ancient", "king", "fort"], "psychology": ["psychology", "brain", "mind"],
    "relationship": ["love", "family", "relationship"], "home": ["home", "interior", "decor"],
    "jobs": ["job", "interview", "career"], "crypto_trading": ["crypto trading", "chart", "forex"],
    "general": ["abstract motion", "cinematic background"]
}
DYNAMIC_FALLBACKS = ["https://player.vimeo.com/external/371433846.sd.mp4?s=236da2f3c02230b0e5170d9a617651a029c29c8e&profile_id=165"]

def Lj(p):
    try:
        data=json.load(open(p))
        for k,v in FIXED_LICENSES.items():
            if k not in data: data[k]=v
        return data
    except: return FIXED_LICENSES.copy()
def Sj(p,d):
    try:
        for k,v in FIXED_LICENSES.items():
            if k not in d: d[k]=v
        json.dump(d,open(p,'w'))
    except: pass
def clean_analyze(s): return re.sub(r"(sex|porn|xxx)"," ",s,flags=re.I), [x.strip() for x in re.split(r'[.!?\n]+',s) if len(x.strip())>5]
def detect_niche_and_keywords(sentence):
    l=sentence.lower(); detected="general"
    for cat,words in CATEGORIES_MAP.items():
        if any(w in l for w in words): detected=cat; break
    meaningful=[w for w in re.sub(r'[^\w\s]','',l).split() if len(w)>3]
    main=' '.join(meaningful[:2]) if meaningful else "success"
    return detected,[f"{detected} {main}",f"{main} cinematic 4k",f"{detected} professional",f"{main} people"]

def St(sentence,d,W,H,part_idx=0):
    niche,keywords=detect_niche_and_keywords(sentence)
    for q in keywords:
        qe=urllib.parse.quote(q)
        for key in PEXELS_KEYS:
            try:
                r=requests.get(f"https://api.pexels.com/videos/search?query={qe}&per_page=10",headers={"Authorization":key},timeout=7)
                if r.status_code==200 and r.json().get('videos'):
                    lk=r.json()['videos'][part_idx%len(r.json()['videos'])]['video_files'][0]['link']
                    t=f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"; open(t,'wb').write(requests.get(lk,timeout=15).content)
                    cl=VideoFileClip(t).resize((W,H)); return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
            except: continue
        try:
            r=requests.get(f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={qe}&per_page=10",timeout=7)
            if r.status_code==200 and r.json().get('hits'):
                lk=r.json()['hits'][part_idx%len(r.json()['hits'])]['videos']['medium']['url']
                t=f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"; open(t,'wb').write(requests.get(lk,timeout=15).content)
                cl=VideoFileClip(t).resize((W,H)); return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
        except: pass
        try:
            r=requests.get(f"https://api.coverr.co/videos?query={qe}&api_key={COVERR_API_KEY}",timeout=7)
            if r.status_code==200 and r.json().get('hits'):
                lk=r.json()['hits'][part_idx%len(r.json()['hits'])]['urls']['mp4']
                t=f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"; open(t,'wb').write(requests.get(lk,timeout=15).content)
                cl=VideoFileClip(t).resize((W,H)); return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
        except: pass
        try:
            r=requests.get(f"https://api.mixkit.co/videos/search/?q={qe}",timeout=7)
            if r.status_code==200 and r.json().get('videos'):
                lk=r.json()['videos'][part_idx%len(r.json()['videos'])]['video_url']
                t=f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"; open(t,'wb').write(requests.get(lk,timeout=15).content)
                cl=VideoFileClip(t).resize((W,H)); return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
        except: pass
        try:
            r=requests.get(f"https://www.videvo.net/api/videos/search/?query={qe}",timeout=7)
            if r.status_code==200 and r.json().get('results'):
                lk=r.json()['results'][part_idx%len(r.json()['results'])]['video_files'][0]['link']
                t=f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"; open(t,'wb').write(requests.get(lk,timeout=15).content)
                cl=VideoFileClip(t).resize((W,H)); return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
        except: pass
    t=f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"; open(t,'wb').write(requests.get(DYNAMIC_FALLBACKS[0],timeout=15).content)
    cl=VideoFileClip(t).resize((W,H)); return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)

async def Tt(t,o,v): await edge_tts.Communicate(t,v,rate="+4%").save(o)
def run_tts(tx,out,vc):
    try: loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(Tt(tx,out,vc)); loop.close()
    except: pass

def Gen(email,code,script,lang,vtype,res,show_sub,pr=gr.Progress()):
    if not script.strip() or not email.strip(): return None,None,"Email / Script likho"
    word_count=len(script.split())
    if word_count>800: return None,None,f"❌ حد ختم! {word_count} الفاظ۔ Limit 800"
    code=code.strip().upper(); email=email.strip().lower(); db=Lj(LICENSE_DB)
    if code in FIXED_LICENSES:
        lic=db[code]; rem=lic["total"]-lic["used"]; free=False
    elif not code:
        fd=Lj(FREE_DB); ek=email+"_"+datetime.date.today().isoformat(); ut=fd.get(ek,0)
        if ut>=1: return None,None,f"Daily Free Khatam! {CONTACT}"
        rem=1-ut; free=True; ft=fd; et=ek
    else:
        return None,None,f"Invalid Code! {CONTACT}"

    cs,kws=clean_analyze(script); voice_code=VOICES.get(lang,"en-US-AndrewNeural")
    if res=="MP3 Only (Audio Voice)":
        pr(0.3,desc="Generating Audio..."); audio_file=f"./JSM_Audio_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        run_tts(cs,audio_file,voice_code); au=AudioFileClip(audio_file); duration_mins=au.duration/60.0; au.close()
        if free: ft[et]=ut+duration_mins; Sj(FREE_DB,ft)
        else: db[code]["used"]+=duration_mins; Sj(LICENSE_DB,db)
        return None,audio_file,f"✅ Audio Done! {duration_mins:.1f}m | Words: {word_count}/800"

    W,H=(1280,720) if res=="1280x720 - HD" else (854,480)
    if "TikTok" in vtype: W,H=(720,1280)
    pvs=[]; chs=kws; total_steps=len(chs); need=0.0; global_clip_counter=0

    for idx,ch in enumerate(chs):
        niche=detect_niche_and_keywords(ch)[0]; percent=((idx+1)/total_steps)*100
        pr((idx+1)/total_steps,desc=f"Scene {idx+1}/{total_steps} - {niche} - {percent:.1f}%")
        ap=f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"; run_tts(ch,ap,voice_code)
        if not os.path.exists(ap): continue
        au=AudioFileClip(ap)
        if au.duration>0.4: au=au.subclip(0,au.duration-0.2)
        need+=au.duration/60.0
        if need>rem+0.01: au.close(); return None,None,f"Need {need:.1f}m Baki {rem:.1f}m"
        sub_clips=[]; dur_left=au.duration
        while dur_left>0:
            cur=min(2.8,dur_left); sc=St(ch,cur,W,H,global_clip_counter); sub_clips.append(sc); dur_left-=cur; global_clip_counter+=1
        base=concatenate_videoclips(sub_clips,method="compose") if len(sub_clips)>1 else sub_clips[0]
        base=base.set_duration(au.duration); layers=[base]
        if show_sub:
            try: txt=TextClip(ch[:90],fontsize=int(W*0.04),color='yellow',stroke_color='black',stroke_width=3.5,method='caption',size=(W*0.88,None)).set_duration(au.duration).set_position(('center',0.78),relative=True); layers.append(txt)
            except: pass
        fn=CompositeVideoClip(layers).set_audio(au); vp=f"{BASE_DIR}/P_{idx}.mp4"; fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=4,logger=None); pvs.append(VideoFileClip(vp)); au.close()

    fv=concatenate_videoclips(pvs,method="compose"); vf=f"./JSM_Video_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=4,logger=None)
    if free: ft[et]=ut+need; Sj(FREE_DB,ft); msg=f"FREE {need:.1f}m OK | Words: {word_count}/800"
    else: db[code]["used"]+=need; Sj(LICENSE_DB,db); msg=f"PAID Baki {(db[code]['total']-db[code]['used']):.1f}m | Words: {word_count}/800"
    return vf,vf,msg

with gr.Blocks(title="JSM MASTER V3.5") as demo:
    gr.HTML(f"<h1 style='color:#FFD700;text-align:center'>✦ JSM VIDEO GENERATOR MASTER V3.5 ✦</h1><p style='text-align:center;color:#D4AF37'>{BRAND_NAME} | 52 Categories + 6 Stock Sites</p>")
    with gr.Row(): email=gr.Textbox(label="Email"); code=gr.Textbox(label="License Code"); lang=gr.Dropdown(list(VOICES.keys()),value="English Male (Andrew)")
    with gr.Row(): vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9"); resolution=gr.Dropdown(["MP3 Only (Audio Voice)","1280x720 - HD","854x480 - SD Fast"],value="1280x720 - HD"); show_sub=gr.Checkbox(value=True,label="Subtitles")
    script=gr.Textbox(lines=8,label="Script Max 800 Words")
    btn=gr.Button("GENERATE",variant="primary")
    with gr.Row(): video=gr.Video(); download=gr.File()
    status=gr.Textbox(label="Status")
    btn.click(Gen,[email,code,script,lang,vtype,resolution,show_sub],[video,download,status])
demo.queue().launch(share=True)
