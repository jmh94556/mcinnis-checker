import os
import smtplib
from email.message import EmailMessage
import requests

FACILITY_URL = "https://www.rec.us/locations/aa24a995-9adc-46d3-bc4b-20875266ea95"
TARGET_TIMES = ["10:00", "11:00"]
TOTAL_COURTS = 3  # Courts 1b, 2a, 2b reservable


def check_courts():
  try:
    # Rec.us public availability endpoint check for McInnis Park
    response = requests.get(
        "https://www.rec.us/api/v1/locations/aa24a995-9adc-46d3-bc4b-20875266ea95/availability",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    data = response.json()

    for slot in data.get("slots", []):
      if slot["time"] in TARGET_TIMES and slot["day"] == "Tuesday":
        reserved_count = slot.get("reserved_count", 0)
        available_count = TOTAL_COURTS - reserved_count

        # Alert if exactly 1 court is left open (2 are reserved)
        if available_count == 1:
          send_group_text(
              f"Pickleball Alert! Only 1 court left for Tuesday at"
              f" {slot['time']} AM at McInnis Park. Grab it: {FACILITY_URL}"
          )
  except Exception as e:
    print(f"Error checking schedule: {e}")


def send_group_text(msg_body):
  sender_email = os.environ.get("ALERT_EMAIL")
  sender_password = os.environ.get("ALERT_PASSWORD")

  recipients = [
      "9258192723@tmomail.net",
      "7086389124@vtext.com",
      "4159993774@txt.att.net",
      "4159718775@vtext.com",
      "9086427650@mypixmessages.com",
      "6175130812@vtext.com",
      "4159714090@text.att.net",  # Standard gateway fallback
  ]

  msg = EmailMessage()
  msg.set_content(msg_body)
  msg.Subject = "McInnis Court Alert"
  msg.From = sender_email
  msg.To = ", ".join(recipients)

  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, sender_password)
    server.send_message(msg)


if __name__ == "__main__":
  check_courts()
