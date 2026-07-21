import gradio as gr, asyncio, edge_tts, uuid, random, requests, re, os, json, base64, urllib.parse, datetime, time
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip
from moviepy.audio.fx.volumex import volumex

CONTACT = "03043399133 | 03022246271"
ON = "JAM SAEED MOTHA"; ONUM = "03043399133"; MN = "MUJAHID HUSSAIN"; MNUM = "03022246271"
BRAND_NAME = "JSM AI BY JAM SAEED MOTHA"

# 🔑 APIs & Keys Configuration
SUPABASE_KEY = "sb_publishable_1W4NK6X7Edacm_eSB1cFDQ_CkT6c4EY"
PIXABAY_KEY = "56386293-14facd94fdac26f9fc37f5f2c"
COVERR_API_KEY = "8c8c592b07a57e05dc49368c399b7659"

# Cleaned Direct Pexels API Keys (No UnicodeDecodeError)
XK = [
    "563492ad6f91700001000001c3b28bcae9b342419f9f91a27e0259f9",
    "563492ad6f917000010000012e8b0a232f0c43ca91e1d3e1ef62ea53",
    "563492ad6f91700001000001f35832ea5d63473f8a02a46e107779f2",
    "563492ad6f917000010000019e1b219159044955a6d59ea3b96e4911",
    "563492ad6f91700001000001d2938361099b418381bf47a32e185f31"
]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

VOICES = {
    "English Male (Andrew - Professional Studio)": "en-US-AndrewNeural",
    "English Male (Christopher - Deep Motivational)": "en-US-ChristopherNeural",
    "English Male (Ryan - UK Storyteller)": "en-GB-RyanNeural",
    "English Female (Jenny - Clear & Energetic)": "en-US-JennyNeural",
    "English Female (Sonia - UK Accent)": "en-GB-SoniaNeural",
    "Urdu Male (Asad - Deep Voice / Narrative Style)": "ur-PK-AsadNeural",
    "Urdu Female (Uzma - Soft & Clear)": "ur-PK-UzmaNeural",
    "Hindi Male (Arjun - Motivational Speaker Style)": "hi-IN-ArjunNeural",
    "Hindi Female (Swara - Dynamic & Crisp)": "hi-IN-SwaraNeural",
    "Russian Male (Dmitry - Strong Studio Voice)": "ru-RU-DmitryNeural",
    "Russian Female (Svetlana - Expressive)": "ru-RU-SvetlanaNeural",
    "Arabic Male (Hamed - Classic Powerful Voice)": "ar-SA-HamedNeural",
    "Arabic Female (Zariyah - Smooth Tone)": "ar-SA-ZariyahNeural",
    "Spanish Male (Alvaro - High Energy)": "es-ES-AlvaroNeural",
    "Spanish Female (Elvira - Expressive)": "es-ES-ElviraNeural"
}

BASE_DIR = "./JSM_Outputs"
FREE_DB = os.path.join(BASE_DIR, "free_daily.json")
LICENSE_DB = os.path.join(BASE_DIR, "jsm_licenses_final.json")
os.makedirs(BASE_DIR, exist_ok=True)

STOP_WORDS = {"about", "today", "video", "talk", "karenge", "baat", "shuru", "please", "subscribe", "channel", "welcome", "dosto", "bhai", "hello", "everyone"}

FIXED_LICENSES = {
    "AREEJ786": {"bound_email": "", "total": 300.0, "used": 0.0, "expiry": "2030-12-31"},
    "JSM300": {"bound_email": "", "total": 300.0, "used": 0.0, "expiry": "2030-12-31"},
    "JSM500": {"bound_email": "", "total": 500.0, "used": 0.0, "expiry": "2030-12-31"},
    "JSM600": {"bound_email": "", "total": 600.0, "used": 0.0, "expiry": "2030-12-31"},
    "JSM1000": {"bound_email": "", "total": 1000.0, "used": 0.0, "expiry": "2030-12-31"}
}

CATEGORIES_MAP = {
    "medical": ["doctor", "hospital", "patient", "medical", "health", "surgery", "clinic", "nurse", "medicine"],
    "engineering": ["engineer", "construction", "architect", "building", "bridge", "blueprint", "site"],
    "software": ["coding", "software", "developer", "programmer", "python", "computer", "laptop", "code"],
    "ai_tech": ["ai", "robot", "artificial intelligence", "cyberpunk", "future", "technology", "data"],
    "finance": ["bitcoin", "crypto", "trading", "stock market", "money", "investing", "bank", "wealth"],
    "business": ["corporate", "office", "meeting", "business", "presentation", "boss", "strategy"],
    "e_commerce": ["shopping", "product", "delivery", "ecommerce", "store", "online shopping", "package"],
    "farming": ["farmer", "kisan", "tractor", "agriculture", "field", "crop", "village", "harvest"],
    "real_estate": ["house", "property", "mansion", "apartment", "real estate", "interior design", "realtor"],
    "storytelling": ["history", "ancient", "mystery", "dark", "kingdom", "warrior", "legend", "castle"],
    "fitness": ["gym", "workout", "fitness", "bodybuilding", "exercise", "running", "yoga", "athlete"],
    "food": ["cooking", "chef", "food", "kitchen", "restaurant", "recipe", "delicious", "baking"],
    "travel": ["travel", "tourism", "airplane", "beach", "mountains", "vacation", "hotel", "adventure"],
    "education": ["student", "school", "university", "book", "library", "learning", "teacher", "study"],
    "gaming": ["gaming", "gamer", "esports", "playstation", "xbox", "controller", "streamer"],
    "fashion": ["fashion", "model", "clothing", "style", "runway", "photoshoot", "dress"],
    "automotive": ["car", "supercar", "driving", "mechanic", "engine", "vehicle", "racing"],
    "nature": ["forest", "river", "ocean", "landscape", "sunset", "sky", "wildlife", "flowers"],
    "space": ["space", "galaxy", "astronaut", "planet", "stars", "universe", "nasa", "rocket"],
    "law": ["lawyer", "court", "judge", "justice", "legal", "law", "handcuffs"],
    "science": ["laboratory", "chemistry", "microscope", "science", "experiment", "research", "physics"],
    "music": ["musician", "guitar", "piano", "studio", "singing", "concert", "dj"],
    "art": ["painting", "artist", "drawing", "design", "creative", "sculpture", "exhibition"],
    "pets": ["dog", "cat", "animals", "cute pets", "puppy", "veterinary"],
    "beauty": ["makeup", "skincare", "salon", "barber", "haircut", "spa"],
    "security": ["cybersecurity", "hacker", "police", "security camera", "cctv", "guard"],
    "crypto": ["blockchain", "ethereum", "nft", "digital currency", "wallet"],
    "marketing": ["social media", "marketing", "seo", "branding", "advertising", "content creation"],
    "motivational": ["success", "inspiration", "motivation", "hard work", "goal", "trophy"],
    "mindfulness": ["meditation", "mindfulness", "peace", "nature relax", "calm"],
    "news": ["breaking news", "journalism", "reporter", "studio news", "media"],
    "military": ["army", "military", "soldier", "weapon", "navy", "airforce"],
    "logistics": ["truck", "shipping", "cargo", "warehouse", "logistics", "freight"],
    "energy": ["solar energy", "wind turbine", "electricity", "green energy", "power plant"],
    "general": ["abstract motion background", "cinematic timelapse", "modern aesthetic"]
}

DYNAMIC_FALLBACKS = [
    "https://player.vimeo.com/external/371433846.sd.mp4?s=236da2f3c02230b0e5170d9a617651a029c29c8e&profile_id=165",
    "https://player.vimeo.com/external/538569350.sd.mp4?s=8b652ee97d8b36a19f5617bfd69106ec2b9cb525&profile_id=165",
    "https://player.vimeo.com/external/409132226.sd.mp4?s=ebd04cb5038c353b3b194519543e33c7dae2051f&profile_id=165",
    "https://player.vimeo.com/external/435649383.sd.mp4?s=7b9a52bc23924df50f3c0e1fc84241e06fa4d5de&profile_id=165",
    "https://images.pexels.com/videos/4482/motion-background-pms-1.mp4"
]

def Lj(p):
    try:
        data = json.load(open(p))
        for k, v in FIXED_LICENSES.items():
            if k not in data: data[k] = v
        return data
    except:
        return FIXED_LICENSES.copy()

def Sj(p, d):
    try:
        for k, v in FIXED_LICENSES.items():
            if k not in d: d[k] = v
        json.dump(d, open(p, 'w'))
    except: pass

def clean_analyze(script):
    clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked|boobs|bikini)", " ", script, flags=re.I)
    sens = [s.strip() for s in re.split(r'[.!?\n]+', clean) if len(s.strip()) > 5]
    return clean, sens

def Kw(text):
    l = text.lower()
    for cat, words in CATEGORIES_MAP.items():
        if any(w in l for w in words):
            return f"{cat} {random.choice(words)} cinematic 4k"
    
    clean_text = re.sub(r'[^\w\s]', '', l)
    meaningful = [w for w in clean_text.split() if len(w) > 3 and w not in STOP_WORDS]
    if len(meaningful) >= 1:
        return f"{' '.join(meaningful[:2])} professional cinematic 4k"
    return "cinematic dynamic motion background 4k"

def get_niche_music(text):
    q = "cinematic inspiring background"
    l = text.lower()
    if any(x in l for x in ["tech", "coding", "ai"]): q = "ambient tech electronic"
    elif any(x in l for x in ["finance", "money", "business"]): q = "corporate business motivation"
    elif any(x in l for x in ["gym", "fitness", "workout"]): q = "energetic rock sports"
    try:
        r = requests.get(f"https://pixabay.com/api/soundeffects/?key={PIXABAY_KEY}&q={urllib.parse.quote(q)}&per_page=10", timeout=6)
        if r.json().get('hits'):
            mp = f"{BASE_DIR}/bgm_{uuid.uuid4().hex[:4]}.mp3"
            open(mp, 'wb').write(requests.get(random.choice(r.json()['hits'])['download_url'], timeout=12).content)
            return mp
    except: pass
    return None

def St(text, d, W, H, part_idx=0):
    q = Kw(text)
    q_encoded = urllib.parse.quote(q)
    
    # 1. Pexels Multi-Key Search
    for key in XK:
        try:
            r = requests.get(f"https://api.pexels.com/videos/search?query={q_encoded}&per_page=30", headers={"Authorization": key}, timeout=6)
            if 'videos' in r.json() and r.json()['videos']:
                v_list = r.json()['videos']
                v_obj = v_list[part_idx % len(v_list)]
                lk = v_obj['video_files'][0]['link']
                t = f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"
                open(t, 'wb').write(requests.get(lk, timeout=12).content)
                cl = VideoFileClip(t).resize((W, H))
                return cl.loop(duration=d) if cl.duration < d else cl.subclip(0, d)
        except: continue

    # 2. Pixabay API Search
    try:
        r = requests.get(f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={q_encoded}&per_page=30", timeout=6)
        if r.json().get('hits'):
            v_list = r.json()['hits']
            v_obj = v_list[part_idx % len(v_list)]
            lk = v_obj['videos']['medium']['url']
            t = f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"
            open(t, 'wb').write(requests.get(lk, timeout=12).content)
            cl = VideoFileClip(t).resize((W, H))
            return cl.loop(duration=d) if cl.duration < d else cl.subclip(0, d)
    except: pass

    # 3. Coverr API Search
    try:
        r = requests.get(f"https://api.coverr.co/videos?query={q_encoded}&api_key={COVERR_API_KEY}", timeout=6)
        if r.json().get('hits'):
            v_list = r.json()['hits']
            v_obj = v_list[part_idx % len(v_list)]
            lk = v_obj['urls']['mp4']
            t = f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"
            open(t, 'wb').write(requests.get(lk, timeout=12).content)
            cl = VideoFileClip(t).resize((W, H))
            return cl.loop(duration=d) if cl.duration < d else cl.subclip(0, d)
    except: pass

    # 4. Dynamic Fallback
    fallback_url = DYNAMIC_FALLBACKS[part_idx % len(DYNAMIC_FALLBACKS)]
    try:
        t = f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"
        open(t, 'wb').write(requests.get(fallback_url, timeout=12).content)
        cl = VideoFileClip(t).resize((W, H))
        return cl.loop(duration=d) if cl.duration < d else cl.subclip(0, d)
    except: pass

    return ColorClip((W, H), color=(random.randint(10, 40), random.randint(10, 40), random.randint(10, 40)), duration=d)

async def Tt(t, o, v): await edge_tts.Communicate(t, v, rate="+4%").save(o)
def run_tts(tx, out, vc):
    try:
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(Tt(tx, out, vc)); loop.close()
    except: pass

def Gen(email, code, script, lang, vtype, res, show_sub, cat_hidden, pr=gr.Progress()):
    if not script.strip() or not email.strip(): return None, None, "Email / Script likho"
    
    code = code.strip().upper(); today = datetime.date.today(); email = email.strip().lower()
    
    db = Lj(LICENSE_DB)
    if code in FIXED_LICENSES:
        lic = db[code]
        if lic["used"] >= lic["total"]: return None, None, f"Khatam! {lic['used']:.1f}/{lic['total']}"
        rem = lic["total"] - lic["used"]; free = False
    elif not code:
        fd = Lj(FREE_DB); ek = email + "_" + today.isoformat(); ut = fd.get(ek, 0)
        if ut >= 1: return None, None, f"Daily Free Khatam! {CONTACT}"
        rem = 1 - ut; free = True; ft = fd; et = ek
    else:
        if code not in db: return None, None, f"❌ Invalid Code! {CONTACT}"
        lic = db[code]
        if lic["bound_email"] and lic["bound_email"] != email: return None, None, f"LOCKED! {lic['bound_email']}"
        if not lic["bound_email"]: lic["bound_email"] = email
        if lic["used"] >= lic["total"]: return None, None, f"Khatam! {lic['used']:.1f}/{lic['total']}"
        rem = lic["total"] - lic["used"]; free = False

    cs, kws = clean_analyze(script)
    voice_code = VOICES.get(lang, "en-US-AndrewNeural")

    if res == "MP3 Only (Audio Voice)":
        pr(0.3, desc="Generating Speech Audio...")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = f"./JSM_Audio_{timestamp}.mp3"
        run_tts(cs, audio_file, voice_code)
        
        if os.path.exists(audio_file):
            au = AudioFileClip(audio_file)
            duration_mins = au.duration / 60.0
            au.close()
            
            if free: ft[et] = ut + duration_mins; Sj(FREE_DB, ft)
            else: db[code]["used"] += duration_mins; Sj(LICENSE_DB, db)
                
            return None, audio_file, f"✅ Audio Generated Successfully! ({duration_mins:.1f} mins)"
        else:
            return None, None, "❌ Audio Generation Failed!"

    res_map = {"1280x720 - HD": (1280, 720), "854x480 - SD Fast": (854, 480)}
    W, H = res_map.get(res, (1280, 720))
    if "TikTok" in vtype: W, H = (720, 1280)

    pvs = []
    try:
        chs = kws; need = 0.0
        total_steps = len(chs)
        global_clip_counter = 0
        
        for idx, ch in enumerate(chs):
            pr(idx / total_steps, desc=f"Processing Scene {idx+1}/{total_steps}...")
            
            ap = f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"
            run_tts(ch, ap, voice_code)
            if not os.path.exists(ap): continue
            au = AudioFileClip(ap)
            if au.duration > 0.4: au = au.subclip(0, au.duration - 0.2)
            
            need += au.duration / 60.0
            if need > rem + 0.01: au.close(); return None, None, f"Need {need:.1f}m Baki {rem:.1f}m"
            
            max_clip_dur = 3.5
            sub_clips = []
            dur_left = au.duration
            
            while dur_left > 0:
                cur_sub_dur = min(max_clip_dur, dur_left)
                sc = St(ch, cur_sub_dur, W, H, part_idx=global_clip_counter)
                sub_clips.append(sc)
                dur_left -= cur_sub_dur
                global_clip_counter += 1
                
            base_clip = concatenate_videoclips(sub_clips, method="compose") if len(sub_clips) > 1 else sub_clips[0]
            base_clip = base_clip.set_duration(au.duration)
            
            layers = [base_clip]
            if show_sub:
                try:
                    txt = TextClip(ch[:90], fontsize=int(W*0.04), color='yellow', stroke_color='black', stroke_width=3.5, method='caption', size=(W*0.88, None)).set_duration(au.duration).set_position(('center', 0.78), relative=True)
                    layers.append(txt)
                except: pass
            fn = CompositeVideoClip(layers).set_audio(au)
            vp = f"{BASE_DIR}/P_{idx}.mp4"
            fn.write_videofile(vp, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=4, logger=None)
            pvs.append(VideoFileClip(vp)); au.close()
            
        if not pvs: return None, None, "Script check karo"
        
        pr(0.9, desc="Merging scenes and adding background music...")
        fv = concatenate_videoclips(pvs, method="compose")
        video_duration = fv.duration
        original_audio = fv.audio
        
        bgm_path = get_niche_music(script)
        if bgm_path and os.path.exists(bgm_path):
            try:
                bgm = AudioFileClip(bgm_path).loop(duration=video_duration).fx(volumex, 0.25)
                fv = fv.set_audio(CompositeAudioClip([original_audio, bgm]))
            except: pass
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        vf = f"./JSM_Video_{timestamp}.mp4"
        fv.write_videofile(vf, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=4, logger=None)
        for pv in pvs: pv.close()
        
        if free:
            ft[et] = ut + need; Sj(FREE_DB, ft); st_msg = f"FREE {need:.1f}m OK"
        else:
            db[code]["used"] += need; Sj(LICENSE_DB, db); st_msg = f"PAID Baki {(db[code]['total']-db[code]['used']):.1f}m"
            
        return vf, vf, st_msg
    except Exception as e: return None, None, f"Error:{str(e)[:200]}"

css = """
body, .gradio-container { background-color: #000000 !important; color: #FFFFFF !important; }
#header { background-color: #000000 !important; border-bottom: 2px solid #FFD700 !important; padding: 20px; text-align: center; }
#header h1 { color: #FFD700 !important; font-size: 32px !important; font-weight: 900 !important; }
.sub-title { color: #D4AF37 !important; }
.gr-box, .gr-block { background-color: #000000 !important; border: 1px solid #333 !important; }
.gr-textbox, .gr-dropdown, .gr-checkbox { background-color: #000000 !important; color: #FFD700 !important; border: 1px solid #333 !important; }
label { color: #FFD700 !important; }
button.primary { background: linear-gradient(90deg, #FFD700, #FFA500) !important; color: #000000 !important; font-weight: bold !important; border: none !important; }
"""

with gr.Blocks(title="JSM VIDEO GENERATOR MASTER", css=css) as demo:
    gr.HTML(f"""
    <div id="header">
        <h1>✦ JSM VIDEO GENERATOR MASTER ✦</h1>
        <div class="sub-title">{BRAND_NAME}</div>
        <div style="color:#A0A0A0; font-size:12px; margin-top:10px;">{ON}: {ONUM} | {MN}: {MNUM}</div>
    </div>
    """)
    
    with gr.Row():
        email = gr.Textbox(label="Email", placeholder="your@gmail.com")
        code = gr.Textbox(label="License Code", placeholder="Enter valid key")
        lang = gr.Dropdown(list(VOICES.keys()), value="English Male (Andrew - Professional Studio)", label="🌍 Voice & Speaker Style Select")
    with gr.Row():
        vtype = gr.Dropdown(["YouTube 16:9", "TikTok 9:16"], value="YouTube 16:9", label="Type")
        resolution = gr.Dropdown(["MP3 Only (Audio Voice)", "1280x720 - HD", "854x480 - SD Fast"], value="1280x720 - HD", label="Output Mode / Quality")
        show_sub = gr.Checkbox(label="Subtitles ON/OFF", value=True)
        cat_hidden = gr.Textbox(value="Auto", visible=False)
        
    script = gr.Textbox(lines=8, label="Your Long Script (Up to 8 Mins) - Har Line = New Visual Scene", max_length=12000)
    btn = gr.Button("✨ GENERATE MASTER GOLDEN VIDEO ✨", variant="primary")
    
    with gr.Row():
        video = gr.Video(label="Player View")
        download_btn = gr.File(label="📥 DOWNLOAD FILE (Video/MP3)")
        
    status = gr.Textbox(label="Status")
    btn.click(Gen, [email, code, script, lang, vtype, resolution, show_sub, cat_hidden], [video, download_btn, status])

demo.queue(max_size=10).launch(share=True, show_error=True)
