import os
import requests
import random
import string
from dotenv import load_dotenv

name_length = int(os.getenv("NAME_LENGTH"))
target_count = int(os.getenv("TARGET_COUNT"))
max_attempts = int(os.getenv("MAX_ATTEMPT"))

def generate_username(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def check_username(username):
    url = f"https://github.com/{username}"
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 404
    except requests.RequestException:
        return False

available_usernames = []

for _ in range(max_attempts):
    username = generate_username(name_length)
    if check_username(username):
        available_usernames.append(username)
        print(f"Available: {username}")
    if len(available_usernames) >= target_count:
        break

print("\nAvailable usernames:", available_usernames)