import hmac, hashlib
from datetime import timedelta
import time 
import logging

from django.conf import settings

AUTH_EXPECTED_KEYS = ["id", "first_name", "last_name", "username", "auth_date", "hash"]
logger = logging.getLogger("wsgi")


def validate_telegram_auth(
    get_data: dict, 
    tg_secret: str = settings.TELEGRAM_BOT_TOKEN,
    livetime_delta_sec: int = timedelta(minutes=5).total_seconds()
):
    if not tg_secret or not get_data:
        return False
    
    expected_keys = AUTH_EXPECTED_KEYS
    
    if not all([k in get_data.keys() for k in expected_keys]):
        return False
    
    if settings.DEBUG:
        return True
    
    if "photo_url" in get_data:
        expected_keys.append("photo_url")
    
    data = dict(sorted(
        { 
            k: v 
            for k, v in get_data.copy().items() 
            if k in expected_keys 
        }.items(),
        key=lambda p: p[0]
    ))
    
    try:
        auth_delta = time.time() - int(data["auth_date"])

        if (auth_delta - livetime_delta_sec) > 0:
            return False
    except ValueError:
        return False
    
    try:
        current_hash = data.pop("hash")
        data = "\n".join([ f"{k}={v}" for k, v in data.items() ])
        
        expected_hash = hmac.new(
            hashlib.sha256(tg_secret.encode()).digest(), 
            data.encode(),
            hashlib.sha256 
        ).hexdigest()

        return current_hash == expected_hash
    except:
        pass
    return False
