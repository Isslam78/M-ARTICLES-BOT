import os, feedparser, requests, datetime, re, html, time

TOKEN = os.environ["WHATSAPP_TOKEN"]
PHONE_ID = os.environ["WHATSAPP_PHONE_ID"]
TO = os.environ["WHATSAPP_TO"]

topics = {
    0: "math",
    1: "neuroscience",
    2: "atheism",
    3: "physics",
    4: "cybersecurity",
    5: "chess",
    6: "philosophy",
}

now = datetime.datetime.now()
today = now.weekday()
topic = topics[today]
day_of_year = now.timetuple().tm_yday

def clean_html(text):
    text = html.unescape(text or "")
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_full_text(entry):
    if entry.get("content"):
        t = clean_html(entry["content"][0].get("value", ""))
        if len(t) > 500:
            return t
    try:
        r = requests.get(entry.link, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        paras = re.findall(r'<p[^>]*>(.*?)</p>', r.text, re.DOTALL)
        full = " ".join([clean_html(p) for p in paras])
        full = full.replace("Continue reading", "").strip()
        if len(full) > 500:
            return full
    except Exception as e:
        print("Fetch failed:", e)
    return clean_html(entry.get("summary", ""))

def send_whatsapp(text):
    url = f"https://graph.facebook.com/v21.0/{PHONE_ID}/messages"
    res = requests.post(url, headers={"Authorization": f"Bearer {TOKEN}"}, json={
        "messaging_product": "whatsapp",
        "to": TO,
        "type": "text",
        "text": {"body": text}
    })
    print("Sent chunk:", res.status_code)
    return res

def split_text(text, max_len=3800):
    parts = []
    while len(text) > max_len:
        cut = text.rfind(". ", 0, max_len)
        if cut == -1:
            cut = max_len
        else:
            cut += 1
        parts.append(text[:cut].strip())
        text = text[cut:].strip()
    if text:
        parts.append(text)
    return parts

feed = feedparser.parse(f"https://medium.com/feed/tag/{topic}")
entries = feed.entries[:10]
start = day_of_year % max(1, len(entries))
article = entries[start]

title = article.title
author = article.get("author", "Unknown")
full_text = get_full_text(article)
print(f"Full article length: {len(full_text)} chars")
date_str = now.strftime("%A, %B %d")

send_whatsapp(f"☀️ Good Morning, Isslam!\n📅 {date_str}\n🎯 Today's Topic: {topic.upper()}\n\n📰 {title}\n✍️ By {author}\n\nThe full article is coming in parts, stay tuned... 👇")
time.sleep(2)

chunks = split_text(full_text, 3800)
for i, chunk in enumerate(chunks, 1):
    header = f"📖 PART {i}/{len(chunks)} - {title}\n\n"
    send_whatsapp(header + chunk)
    time.sleep(2)

send_whatsapp(f"✅ That's the full article! Done.\n\nHave a great day! 🚀\n🔗 Original: {article.link}")
