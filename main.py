import os, feedparser, requests, datetime

TOKEN = os.environ["WHATSAPP_TOKEN"]
PHONE_ID = os.environ["WHATSAPP_PHONE_ID"]
TO = os.environ["WHATSAPP_TO"]

topics = {
    0: "math", # الاثنين
    1: "neuroscience", # الثلاثاء
    2: "atheism", # الاربعاء
    3: "physics", # الخميس
    4: "science", # الجمعة
    5: "cybersecurity", # السبت
    6: "math", # الاحد
}

today = datetime.datetime.now().weekday()
topic = topics[today]

feed = feedparser.parse(f"https://medium.com/feed/tag/{topic}")
msg = f"☀️ صباح الخير! موضوع اليوم: {topic.upper()}\n\n"
for e in feed.entries[:3]:
    msg += f"📰 {e.title}\n🔗 {e.link}\n\n"

url = f"https://graph.facebook.com/v21.0/{PHONE_ID}/messages"
requests.post(url, headers={"Authorization": f"Bearer {TOKEN}"}, json={
    "messaging_product": "whatsapp",
    "to": TO,
    "type": "text",
    "text": {"body": msg}
})
print("Sent:", topic)
