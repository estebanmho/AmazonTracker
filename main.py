import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os


EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")
URL = os.environ.get("URL")

def quitar_coma(price: str) -> float:
    price = price.replace(",", ".")
    return float(price)


def notify_user(price, product):
    with smtplib.SMTP("smtp-mail.outlook.com") as email_smtp:
        email_smtp.starttls()
        email_smtp.login(user=EMAIL, password=PASSWORD)
        body = f"El articulo {product} esta al gran precio de {price}€."
        email_smtp.sendmail(from_addr=EMAIL, to_addrs=TO_EMAIL, msg=("Subject:Price update\n\n" + body).encode("utf8"))


headers = {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "es-ES,es;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")
price = soup.find(name="span", id="priceblock_ourprice").getText().split()[0]
price = quitar_coma(price)
product = soup.find(name="span", id="productTitle").getText()

if price < 60:
    notify_user(price, product)
