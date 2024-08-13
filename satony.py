#!/usr/bin/env python3
from colorama import init, Style
import sys
import random
import string
import subprocess
import requests
import time
from faker import Faker
import base64
from bs4 import BeautifulSoup

fake = Faker()


init(autoreset=True)

API_URL = "https://www.1secmail.com/api/v1/"  

def create_gradient_text(text, start_color=(255, 0, 0), end_color=(255, 255, 255)):
    gradient_text = ""
    length = len(text)

    for i, char in enumerate(text):
        red = int(start_color[0] + (end_color[0] - start_color[0]) * (i / length))
        green = int(start_color[1] + (end_color[1] - start_color[1]) * (i / length))
        blue = int(start_color[2] + (end_color[2] - start_color[2]) * (i / length))
        gradient_text += f"\033[38;2;{red};{green};{blue}m{char}"

    return gradient_text


def print_banner():
    banner = r"""
   ▄████████    ▄████████     ███      ▄██████▄  ███▄▄▄▄   ▄██   ▄   
  ███    ███   ███    ███ ▀█████████▄ ███    ███ ███▀▀▀██▄ ███   ██▄ 
  ███    █▀    ███    ███    ▀███▀▀██ ███    ███ ███   ███ ███▄▄▄███ 
  ███          ███    ███     ███   ▀ ███    ███ ███   ███ ▀▀▀▀▀▀███ 
▀███████████ ▀███████████     ███     ███    ███ ███   ███ ▄██   ███ 
         ███   ███    ███     ███     ███    ███ ███   ███ ███   ███ 
   ▄█    ███   ███    ███     ███     ███    ███ ███   ███ ███   ███ 
 ▄████████▀    ███    █▀     ▄████▀    ▀██████▀   ▀█   █▀   ▀█████▀  
"""
    print(Style.BRIGHT + create_gradient_text(banner))
    print(create_gradient_text("Version: 1.0 [Beta]"))
    print(create_gradient_text("TG > @ragotn"))
    print(create_gradient_text("Discord > culturing"))

def main_menu():
    print(Style.BRIGHT + create_gradient_text("Main menu\n"))
    print(create_gradient_text("1 > Генератор Пароля"))
    print(create_gradient_text("2 > Поиск по IP"))
    print(create_gradient_text("3 > Получение временной почты"))
    print(create_gradient_text("4 > Поиск по никнейму"))
    print(create_gradient_text("5 > Порт скан"))
    print(create_gradient_text("6 > Вымышленная личность"))
    print(create_gradient_text("7 > Вымышленная карта"))
    print(create_gradient_text("8 > Discord TOKEN"))
    print(create_gradient_text("\nВыберите опцию > "), end='')

def encode_user_id(user_id):
    user_id_str = str(user_id)
    encoded_bytes = base64.b64encode(user_id_str.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return encoded_str

def generate_random_password(length=12):
    """Generate a random password of a given length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def search_ip_with_nmap(ip_address):
    """Perform an nmap scan on the provided IP address."""
    try:
        result = subprocess.run(["nmap", "-sV", ip_address], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении nmap: {e}"

def fetch_temp_email():
    """Fetch a temporary email address using an online service."""
    try:
        response = requests.get(API_URL + "?" + "action=genRandomMailbox&count=1")
        email = response.json()[0]
        print(create_gradient_text(f"Ваш временный email: {email}"))
        return email
    except requests.RequestException as e:
        print(f"Ошибка при получении временной почты: {e}")
        return None

def check_email_inbox(email):
    """Check the inbox for new emails."""
    username, domain = email.split('@')
    try:
        while True:
            response = requests.get(API_URL + "?" + f"action=getMessages&login={username}&domain={domain}")
            messages = response.json()
            if messages:
                for message in messages:
                    mail_id = message['id']
                    details = get_email_details(username, domain, mail_id)
                    print(create_gradient_text(f"\nНовое сообщение от: {message['from']}\nТема: {message['subject']}\n"))
                    print(create_gradient_text(f"Текст:\n{details}"))
            else:
                print(create_gradient_text("Нет новых сообщений."))
            time.sleep(30) 
    except requests.RequestException as e:
        print(f"Ошибка при проверке почты: {e}")

def get_email_details(username, domain, mail_id):
    """Fetch email details."""
    try:
        response = requests.get(API_URL + "?" + f"action=readMessage&login={username}&domain={domain}&id={mail_id}")
        message = response.json()
        return message.get('textBody', '')
    except requests.RequestException as e:
        print(f"Ошибка при получении деталей сообщения: {e}")
        return "Не удалось загрузить сообщение."

def search_username(username):
    """Search for a username across multiple domains with more detailed checks."""
    domains = {
        "Instagram": "https://www.instagram.com/{}",
        "Twitter": "https://twitter.com/{}",
        "GitHub": "https://github.com/{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "TikTok": "https://www.tiktok.com/@{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "Doxbin": "https://doxbin.org/u/{}",
        "YouTube": "https://www.youtube.com/user/{}",
        "Twitch": "https://www.twitch.tv/{}",
        "Discord": "https://discord.com/users/{}",
        "Roblox": "https://www.roblox.com/users/{}",
        "SoundCloud": "https://soundcloud.com/{}",
        "Spotify": "https://open.spotify.com/user/{}",
        "Yandex": "https://yandex.ru/users/{}",
        "Yappy": "https://yappy.com/{}"
    }

    for site_name, domain in domains.items():
        url = domain.format(username)
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            response = requests.get(url, headers=headers, allow_redirects=True)

            if response.status_code == 200:
                if "profile" in response.text or "user" in response.url:
                    print(create_gradient_text(f"Пользователь найден на {site_name}: {url}"))
                else:
                    print(create_gradient_text(f"Пользователь не найден на {site_name}"))
            else:
                print(create_gradient_text(f"Пользователь не найден на {site_name}"))
        except requests.RequestException as e:
            print(f"Ошибка при проверке {site_name}: {e}")

def scan_ports(ip_address):
    """Scan ports on the given IP address using nmap."""
    try:
        print(create_gradient_text("Сканирование портов..."))
        result = subprocess.run(["nmap", "-p-", ip_address], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении nmap: {e}"

def generate_fake_identity():
    """Generate a fictional identity."""
    full_name = fake.name()
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=99).strftime("%Y-%m-%d")
    address = fake.address().replace('\n', ', ')
    passport_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    inn = ''.join(random.choices(string.digits, k=10))

    return {
        "ФИО": full_name,
        "Дата рождения": birth_date,
        "Адрес": address,
        "Паспорт": passport_number,
        "ИНН": inn
    }

def generate_fake_credit_card():
    """Generate fictional credit card details."""
    card_number = '4' + ''.join(random.choices(string.digits, k=15))
    expiration_date = f"{random.randint(1, 12):02d}/{random.randint(24, 30)}"
    cardholder_name = fake.name()
    bank = fake.company()
    cvc = ''.join(random.choices(string.digits, k=3))

    return {
        "Номер карты": card_number,
        "Дата окончания": expiration_date,
        "Владелец": cardholder_name,
        "Банк": bank,
        "CVC-код": cvc
    }

def print_fake_identity():
    """Print the generated fictional identity."""
    identity = generate_fake_identity()
    print(create_gradient_text("\nСгенерированная вымышленная личность:\n"))
    for key, value in identity.items():
        print(create_gradient_text(f"{key}: {value}"))

def print_fake_credit_card():
    """Print the generated fictional credit card details."""
    credit_card = generate_fake_credit_card()
    print(create_gradient_text("\nСгенерированная вымышленная карта:\n"))
    for key, value in credit_card.items():
        print(create_gradient_text(f"{key}: {value}"))


def fetch_discord_token(discord_id):
    """Fetch a simulated Discord token for a given Discord ID."""
    encoded_id = encode_user_id(discord_id)
    return f"Первая часть-{encoded_id}"


def main():
    print_banner()
    main_menu()
    choice = input()
    
    if choice == '1':
        print(create_gradient_text("Вы выбрали опцию 1"))
        print(create_gradient_text(f"Ваш сгенерированный пароль: {generate_random_password()}"))
    elif choice == '2':
        print(create_gradient_text("Вы выбрали опцию 2"))
        ip_address = input(create_gradient_text("Введите IP-адрес для сканирования: "))
        print(search_ip_with_nmap(ip_address))
    elif choice == '3':
        print(create_gradient_text("Вы выбрали опцию 3"))
        email = fetch_temp_email()
        if email:
            check_email_inbox(email)
    elif choice == '4':
        print(create_gradient_text("Вы выбрали опцию 4"))
        username = input(create_gradient_text("Введите никнейм для поиска: "))
        search_username(username)
    elif choice == '6':
        print(create_gradient_text("Вы выбрали опцию 6"))
        ip_address = input(create_gradient_text("Введите IP-адрес для сканирования портов: "))
        print(scan_ports(ip_address))
    elif choice == '7':
        print(create_gradient_text("Вы выбрали опцию 7"))
        print_fake_identity()
    elif choice == '8':
        print(create_gradient_text("Вы выбрали опцию 8"))
        discord_id = input(create_gradient_text("Введите Discord ID: "))
        token = fetch_discord_token(discord_id)
        if token:
            print(f"Token: {token}")  
        else:
            print(create_gradient_text("Не удалось получить токен."))
    elif choice == '9':
        print(create_gradient_text("Вы выбрали опцию 9"))
        print_fake_credit_card()
    else:
        print(create_gradient_text("Неверный выбор. Попробуйте снова."))





if __name__ == "__main__":
    main()
