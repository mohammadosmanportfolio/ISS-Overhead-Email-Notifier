import requests, smtplib, time, os
from datetime import datetime

MY_LAT = 33.78990941221633 # Dummy latitude
MY_LONG = -118.22478396717416 # Dummy longitude
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_EMAIL_PASSWORD")

#Your position is within +5 or -5 degrees of the ISS position.
def is_ISS_close(user_lat_long, iss_lat_long):
    lat_difference = user_lat_long[0] - iss_lat_long[0]
    long_difference = user_lat_long[1] - iss_lat_long[1]
    return lat_difference >= -5 and lat_difference <= 5 and long_difference >= -5 and long_difference <= 5

def is_dark_or_not(sunrise_time, sunset_time, current_time):
    return current_time >= sunset_time or current_time <= sunrise_time

def send_email_notification():
    with smtplib.SMTP(host=os.environ.get("SMTP_HOST")) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg="Subject: ISS coming\n\nLook up!")

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour

#If the ISS is close to my current position and it is currently dark, send an email notification

if is_ISS_close(user_lat_long=(MY_LAT, MY_LONG), iss_lat_long=(iss_latitude, iss_longitude)) and is_dark_or_not(sunrise_time=sunrise, sunset_time=sunset,current_time=time_now):
    send_email_notification()
