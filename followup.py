import os, requests, datetime, random
TOKEN = os.environ["WHATSAPP_TOKEN"]
PHONE_ID = os.environ["WHATSAPP_PHONE_ID"]
TO = os.environ["WHATSAPP_TO"]

messages = [
    "Hey Isslam! 🌞 I hope you enjoyed today's reading. What was the most interesting idea you learned?",
    "Good morning Isslam! 📖 I hope you enjoyed reading today's article. Did it change how you think about something?",
    "Hey Isslam! ✨ I hope you enjoyed the article. Take a moment to think: what would you tell a friend about it?",
    "Hi Isslam! 🚀 I hope you enjoyed today's reading. Remember, one article a day = 365 ideas a year!",
]

now = datetime.datetime.now()
msg = random.choice(messages)

url = f"https://graph.facebook.com/v21.0/{PHONE_ID}/messages"
res = requests.post(url, headers={"Authorization": f"Bearer {TOKEN}"}, json={
    "messaging_product": "whatsapp",
    "to": TO,
    "type": "text",
    "text": {"body": msg}
})
print(res.status_code, res.text)
