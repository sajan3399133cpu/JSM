import requests, datetime, math, subprocess, sys

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyN72bUynR-vhSIW1h8jryguSNiXLxjHriR-gid3tQznezec2ZOXQ3HDqT59PJpdT4e9Q/exec"

def run_jsm(email, license_code, script, voice_lang, video_type, resolution, all_keys):
    print(f"🔍 Checking License: {license_code} for {email}")
    check_data = {"action": "check", "email": email, "code": license_code}
    res = requests.post(WEBHOOK_URL, json=check_data, timeout=10).json()

    if res.get("status")!= "ACTIVE":
        raise Exception(f"❌ License Expired یا غلط ہے! Status: {res.get('status')}")

    remaining_mins = int(res.get("remaining", 0))
    needed_mins = math.ceil(len(script.split()) / 150)
    print(f"✅ License ACTIVE | Remaining: {remaining_mins} min | Needed: {needed_mins} min")

    if remaining_mins < needed_mins:
        raise Exception(f"❌ منٹ ختم! آپ کے پاس {remaining_mins} منٹ ہیں، چاہیے {needed_mins} منٹ")

    deduct_data = {"action": "deduct", "email": email, "code": license_code, "mins": needed_mins}
    requests.post(WEBHOOK_URL, json=deduct_data, timeout=10)
    print(f"✅ {needed_mins} منٹ کٹ گئے۔ باقی: {remaining_mins - needed_mins}")

    # KEYS AB YAHAN SE AYENGI
    groq_api_key=""; pexels_keys=[]; pixabay_key=""
    for line in all_keys.strip().splitlines():
        line=line.strip().strip(',').strip('"').strip("'")
        if not line: continue
        if line.startswith("gsk_"): groq_api_key=line.strip()
        elif len(line)>30 and "," in line: pexels_keys.extend([k.strip() for k in line.split(',') if len(k.strip())>10])
        elif len(line)>30: pexels_keys.append(line.strip())
        elif "-" in line and line[0].isdigit(): pixabay_key=line.strip()

    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "moviepy==1.0.3", "edge-tts", "gtts", "pillow", "nest-asyncio", "requests"])
    import urllib.request
    print(f"Keys Check: Groq=YES Pexels={len(pexels_keys)} Pixabay=YES")
    exec(urllib.request.urlopen("https://raw.githubusercontent.com/sajan3399133cpu/JSM/main/app_avatar.py").read().decode())
