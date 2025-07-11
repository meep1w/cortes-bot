import db

def check_registration(user_id):
    """
    Заглушка проверки регистрации.
    Всегда возвращает False.
    Позже подключим реальный API.
    """
    return db.is_registered(user_id)
