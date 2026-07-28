import requests, datetime, math, subprocess, sys

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyN72bUynR-vhSIW1h8jryguSNiXLxjHriR-gid3tQznezec2ZOXQ3HDqT59PJpdT4e9Q/exec"

def run_jsm(email, license_code, script, voice_lang, video_type, resolution, all_keys):
    print(f"🔍 Checking License: {license_code} for {email}")
    res = requests.post(WEBHOOK_URL, json={"action":"check","email":email,"code":license_code}, timeout=10).json()
    if res.get("status")!= "ACTIVE": raise Exception(f"❌ License: {res.get('status')}")

    remaining_mins = int(res.get("remaining", 0))
    needed_mins = math.ceil(len(script.split()) / 150)
    print(f"✅ ACTIVE | Remaining: {remaining_mins} min | Needed: {needed_mins} min")
    if remaining_mins < needed_mins: raise Exception(f"❌ منٹ کم ہیں")

    requests.post(WEBHOOK_URL, json={"action":"deduct","email":email,"code":license_code,"mins":needed_mins}, timeout=10)
    print(f"✅ {needed_mins} منٹ کٹ گئے۔ باقی: {remaining_mins - needed_mins}")

    # KEYS
    groq_api_key=""; pexels_keys=[]; pixabay_key=""
    for line in all_keys.strip().splitlines():
        line=line.strip().strip(',').strip('"').strip("'")
        if not line: continue
        if line.startswith("gsk_"): groq_api_key=line
        elif len(line)>30 and "," in line: pexels_keys.extend([k.strip() for k in line.split(',') if len(k.strip())>10])
        elif len(line)>30: pexels_keys.append(line)
        elif "-" in line and line[0].isdigit(): pixabay_key=line

    # VOICE FIX: "ur-PK-AsadNeural - Male Urdu" se sirf "ur-PK-AsadNeural" nikalna
    voice_lang = voice_lang.split(" - ")[0].strip()

    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "moviepy==1.0.3", "edge-tts", "gtts", "pillow"])
    import urllib.request
    print(f"Settings: Voice={voice_lang} | Video={video_type} | Res={resolution}")
    exec(urllib.request.urlopen("https://raw.githubusercontent.com/sajan3399133cpu/JSM/main/app_avatar.py").read().decode())
