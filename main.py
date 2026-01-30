import os
import requests
import random
import string
import sys
import time
from dotenv import load_dotenv

load_dotenv()

def generate_username(length: int, keywords: list[str] | None = None) -> str:
    """指定された長さのユーザー名を生成。keywords があればそのいずれかを含む。"""
    if keywords and length >= 2:
        word = random.choice(keywords)
        if len(word) >= length:
            return word[:length].lower()
        remaining = length - len(word)
        prefix_len = random.randint(0, remaining)
        suffix_len = remaining - prefix_len
        charset = string.ascii_lowercase + string.digits
        prefix = "".join(random.choices(charset, k=prefix_len))
        suffix = "".join(random.choices(charset, k=suffix_len))
        return prefix + word.lower() + suffix
    charset = string.ascii_lowercase + string.digits
    return "".join(random.choices(charset, k=length))


def check_username(username: str) -> bool:
    """GitHub でユーザー名が未使用（404）なら True を返す。"""
    url = f"https://github.com/{username}"
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 404
    except requests.RequestException:
        return False


def parse_args(args: list[str]) -> tuple[int, int, int, list[str]]:
    """
    コマンドライン引数または環境変数から設定を取得。
    戻り値: (name_length, target_count, max_attempts, keywords)
    """
    name_length = int(os.getenv("NAME_LENGTH", "4"))
    target_count = int(os.getenv("TARGET_COUNT", "1"))
    max_attempts = int(os.getenv("MAX_ATTEMPT", "100"))
    raw_keywords = os.getenv("KEYWORDS", "")
    keywords = [k.strip().lower() for k in raw_keywords.split(",") if k.strip()]

    if len(args) >= 3:
        name_length = int(args[0])
        target_count = int(args[1])
        max_attempts = int(args[2])
    if len(args) >= 4:
        keywords = [k.strip().lower() for k in args[3].split(",") if k.strip()]

    return name_length, target_count, max_attempts, keywords


def main(args: list[str]) -> None:
    if len(args) == 1 and args[0] in ("-h", "--help"):
        print("usage: python main.py [name_length] [target_count] [max_attempts] [keywords]")
        print("  name_length   : ユーザー名の長さ (default: .env or 4)")
        print("  target_count  : 見つける個数 (default: .env or 1)")
        print("  max_attempts  : 最大試行回数 (default: .env or 100)")
        print("  keywords      : 含めたいワードをカンマ区切り (optional)")
        print("例: python main.py 6 5 200 cat,star")
        return

    name_length, target_count, max_attempts, keywords = parse_args(args)

    if name_length < 1:
        print("name_length は 1 以上にしてください。")
        return
    if target_count < 1:
        print("target_count は 1 以上にしてください。")
        return
    if max_attempts < 1:
        print("max_attempts は 1 以上にしてください。")
        return

    available_usernames: list[str] = []
    used_keywords = keywords if keywords else None

    for attempt in range(max_attempts):
        username = generate_username(name_length, used_keywords)
        if check_username(username):
            available_usernames.append(username)
            print(f"Available: {username}")
        if len(available_usernames) >= target_count:
            break
        time.sleep(0.1)

    print("\nAvailable usernames:", available_usernames)


if __name__ == "__main__":
    main(sys.argv[1:])
