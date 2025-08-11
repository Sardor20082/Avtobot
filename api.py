import hashlib
import requests
from datetime import datetime, timezone
from config import BASE_URL, HASH, CASHIERPASS, CASHDESK_ID, LANG

def md5_hex(s: str) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def get_balance():
    # UTC va vaqtni timezone aware qilib olish yaxshiroq
    dt_str = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M:%S")
    confirm = md5_hex(f"{CASHDESK_ID}:{HASH}")

    s1 = f"hash={HASH}&cashierpass={CASHIERPASS}&dt={dt_str}"
    sha1 = sha256_hex(s1)

    s2 = f"dt={dt_str}&cashierpass={CASHIERPASS}&cashdeskid={CASHDESK_ID}"
    md5_2 = md5_hex(s2)

    sign = sha256_hex(sha1 + md5_2)

    headers = {"Content-Type": "application/json", "sign": sign}
    params = {"confirm": confirm, "dt": dt_str}

    r = requests.get(f"{BASE_URL}/Cashdesk/{CASHDESK_ID}/Balance", headers=headers, params=params)
    return r.json()

def deposit_to_user(user_id: int, amount: float):
    s1 = f"hash={HASH}&lng={LANG}&UserId={user_id}"
    sha1 = sha256_hex(s1)

    # summa uchun string formatlash to'g'ri, 100.0 -> "100", 100.50 -> "100.5" emas, uni quyidagicha qilish mumkin:
    summa_str = f"{amount:.2f}".rstrip('0').rstrip('.')

    s2 = f"summa={summa_str}&cashierpass={CASHIERPASS}&cashdeskid={CASHDESK_ID}"
    md5_2 = md5_hex(s2)

    sign = sha256_hex(sha1 + md5_2)
    confirm = md5_hex(f"{user_id}:{HASH}")

    headers = {"Content-Type": "application/json", "sign": sign}
    payload = {
        "cashdeskId": CASHDESK_ID,
        "lng": LANG,
        "summa": amount,
        "confirm": confirm
    }
    r = requests.post(f"{BASE_URL}/Deposit/{user_id}/Add", headers=headers, json=payload)
    return r.json()

def payout_to_user(user_id: int, code: str):
    s1 = f"hash={HASH}&lng={LANG}&UserId={user_id}"
    sha1 = sha256_hex(s1)

    s2 = f"code={code}&cashierpass={CASHIERPASS}&cashdeskid={CASHDESK_ID}"
    md5_2 = md5_hex(s2)

    sign = sha256_hex(sha1 + md5_2)
    confirm = md5_hex(f"{user_id}:{HASH}")

    headers = {"Content-Type": "application/json", "sign": sign}
    payload = {
        "cashdeskId": CASHDESK_ID,
        "lng": LANG,
        "code": code,
        "confirm": confirm
    }
    r = requests.post(f"{BASE_URL}/Deposit/{user_id}/Payout", headers=headers, json=payload)
    return r.json()
