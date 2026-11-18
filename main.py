import os, feedparser, requests, datetime, re, html

TOKEN = os.environ["WHATSAPP_TOKEN"]
PHONE_ID = os.environ["WHATSAPP_PHONE_ID"]
TO = os.environ["WHATSAPP_TO"]

topics = {
    0: "math", # Monday
    1: "neuroscience", # Tuesday
    2: "atheism", # Wednesday
    3: "physics", # Thursday
    4: "science", # Friday
    5: "cybersecurity", # Saturday
    6: "math", # Sunday
}

today = datetime.datetime.now().weekday()
topic = topics[today]

def clean_text(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:600]

feed = feedparser.parse(f"https://medium.com/feed/tag/{topic}")
msg = f"☀️ Good Morning! Today's topic: {topic.upper()}\n\n"

for e in feed.entries[:3]:
    title = e.title
    summary = clean_text(e.get("summary", "") or e.get("description", ""))
    if not summary:
        summary = "No summary available for this article."
    msg += f"📰 {title}\n\n{summary}\n\n━━━━━━━━━━\n\n"

url = f"https://graph.facebook.com/v21.0/{PHONE_ID}/messages"
requests.post(url, headers={"Authorization": f"Bearer {TOKEN}"}, json={
    "messaging_product": "whatsapp",
    "to": TO,
    "type": "text",
    "text": {"body": msg}
})
print("Sent:", topic)
