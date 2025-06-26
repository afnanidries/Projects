// sms-health-reminder-bot/index.js
const express = require("express");
const bodyParser = require("body-parser");
const twilio = require("twilio");
require("dotenv").config();

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static("public"));

const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

const healthTips = [
  "Drink at least 8 cups of water today.",
  "Take a walk outside and enjoy fresh air.",
  "Get 7–9 hours of quality sleep tonight.",
  "Eat a fruit or veggie you haven’t had this week.",
  "Stretch your back and shoulders for 5 minutes.",
  "Avoid screens for 30 minutes before bed.",
  "Take 3 deep breaths right now — reset your mind.",
  "Do a quick 10-minute workout.",
  "Write down one thing you’re grateful for.",
  "Don’t forget to smile — it reduces stress!",
  "Call or message a friend — social connection is health.",
  "Check your posture. Sit up straight and relax your shoulders.",
  "Give your eyes a break — 20 seconds looking at something far away.",
  "Skip sugary drinks today and go for water or tea.",
  "Eat mindfully — chew slowly and savor your food."
];

app.post("/send", (req, res) => {
  const { name, phone } = req.body;
  const message = `Hi ${name}, here’s your health tip: ${healthTips[Math.floor(Math.random() * healthTips.length)]}`;

  client.messages
    .create({
      body: message,
      from: process.env.TWILIO_PHONE_NUMBER, // should be "whatsapp:+14155238886"
      to: `whatsapp:${phone}` // phone must be in international format like +1...
    })
    .then(() => res.status(200).send("WhatsApp message sent successfully!"))
    .catch(err => {
      console.error("Twilio Error:", err);
      res.status(500).send("Failed to send WhatsApp message.");
    });
});

app.listen(port, () => console.log(`Server running on port ${port}`));
