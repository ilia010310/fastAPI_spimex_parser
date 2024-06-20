from datetime import datetime, timedelta


def get_expire_time() -> int:
    """Генерирует количество секунд до 14:11 и возвращает его"""
    now = datetime.now()
    drop_time = now.replace(hour=14, minute=11, second=0)
    if now > drop_time:
        drop_time += timedelta(days=1)
    res = abs((now - drop_time).total_seconds())
    return int(res)
