import hashlib
import requests
from datetime import datetime, timezone
from config import BASE_URL, HASH, CASHIERPASS, CASHDESK_ID, LANG

def md5_hex(s: str) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def get_sign(*args) -> str:
    """
    Sign hisoblash uchun yordamchi funksiya.
    Args qiymatlar ketma-ketligidan md5 va sha256 ni hisoblaydi.
    """
    # args: list of strings (md5 va sha256 lar uchun oldingi stringlar)
    # Funksiya hozir sizning logikaga mos holda ishlaydi
    # 1. sha256_hex(args[0]) + md5_hex(args[1]) ni sha256 ga aylantiradi
    sha1 = sha256_hex(args[0])
    md5_2 = md5_hex(args[1])
    return sha256_hex(sha1 + md5_2)

def get_balance():
    dt_str = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M:%S")
    confirm = md5_hex(f"{CASHDESK_ID}:{HASH}")

    s1 = f"hash={HASH}&cashierpass={CASHIERPASS}&dt={dt_str}"
    s2 = f"dt={dt_str}&cashierpass={CASHIERPASS}&cashdeskid={CASHDESK_ID}"

    sign = get_sign(s1, s2)

    headers = {
        "Content-Type": "application/json",
        "sign": sign
    }
    params = {
        "confirm": confirm,
        "dt": dt_str
    }

    try:
        response = requests.get(f"{BASE_URL}/Cashdesk/{CASHDESK_ID}/Balance", headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"success": False, "message": f"Xatolik: {e}"}

def deposit_to_user(user_id: int, amount: float):
    summa_str = f"{amount:.2f}".rstrip('0').rstrip('.')  # 10.00 -> 10

    s1 = f"hash={HASH}&lng={LANG}&UserId={user_id}"
    s2 = f"summa={summa_str}&cashierpass={CASHIERPASS}&cashdeskid={CASHDESK_ID}"

    sign = get_sign(s1, s2)
    confirm = md5_hex(f"{user_id}:{HASH}")

    headers = {
        "Content-Type": "application/json",
        "sign": sign
    }
    payload = {
        "cashdeskId": CASHDESK_ID,
        "lng": LANG,
        "summa": amount,
        "confirm": confirm
    }

    try:
        response = requests.post(f"{BASE_URL}/Deposit/{user_id}/Add", headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"success": False, "message": f"Xatolik: {e}"}

def payout_to_user(user_id: int, code: str):
    s1 = f"hash={HASH}&lng={LANG}&UserId={user_id}"
    s2 = f"code={code}&cashierpass={CASHIERPASS}&cashdeskid={CASHDESK_ID}"

    sign = get_sign(s1, s2)
    confirm = md5_hex(f"{user_id}:{HASH}")

    headers = {
        "Content-Type": "application/json",
        "sign": sign
    }
    payload = {
        "cashdeskId": CASHDESK_ID,
        "lng": LANG,
        "code": code,
        "confirm": confirm
    }

    try:
        response = requests.post(f"{BASE_URL}/Deposit/{user_id}/Payout", headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"success": False, "message": f"Xatolik: {e}"}
