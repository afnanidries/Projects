# WhatsApp Health Tip Reminder

A simple, full-stack web app that delivers randomized daily health tips to your verified WhatsApp number using Twilio's WhatsApp API. Built with Node.js, Express, and vanilla HTML/CSS for a clean and professional experience.

---

## Features
- Send a randomized health or wellness tip to your WhatsApp
- No signup or login required
- Built with Twilio's WhatsApp Sandbox API
- Clean, responsive interface styled for a modern wellness look

---

## Tech Stack

| Frontend        | Backend         | Messaging API  | Deployment |
|----------------|------------------|----------------|-------------|
| HTML / CSS     | Node.js + Express| Twilio WhatsApp | (Deploy to Render or local)

---

## Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/sms-health-reminder-bot.git
cd sms-health-reminder-bot
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Create a `.env` File
Set your Twilio credentials and WhatsApp Sandbox number:
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
```

Get these from [https://www.twilio.com/console/sms/whatsapp/learn](https://www.twilio.com/console/sms/whatsapp/learn) and join the sandbox from your own WhatsApp.

### 4. Run the App Locally
```bash
node index.js
```
Then go to [http://localhost:3000](http://localhost:3000)


---

## How It Works
1. Enter your name and WhatsApp number (e.g. `+1XXXXXXXXXX`)
2. Submit the form
3. Receive a tip like:
   > _"Hi Afnan, here’s your health tip: Stretch your back and shoulders for 5 minutes."_

---

## Sample Tips
- Drink at least 8 cups of water today.
- Avoid screens for 30 minutes before bed.
- Take 3 deep breaths right now.
- Skip sugary drinks today and go for tea.
- Call or message a friend — social connection is health.

---

## Future Improvements
- Daily recurring messages (cron)
- Custom scheduling by user
- Tip categories: mental, physical, nutrition
- Admin dashboard for managing tips

---

## Preview
![Screenshot](public/preview.png) <!-- Add this if you want to drop in a UI screenshot -->

---

## Author
**Afnan Idries**  
GitHub: [@afnanidries](https://github.com/afnanidries)
