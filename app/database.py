fake_users_db = {
    "alex_client": {
        "username": "alex_client",
        "email": "alex@coworking.ru",
        "role": "client",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$OFA4dmV2c2Y4bHBlbms$8GzU2X/fE3ZlUksv6w1WDez0wXNn1v8v9x2C3Y4Z5A6"
    },
    "dmitry_admin": {
        "username": "dmitry_admin",
        "email": "dmitry@coworking.ru",
        "role": "admin",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$bXljaGFzdGVwYXNzd29yZA$4KzU1Y/fE3ZlUksv6w1WDez0wXNn1v8v9x2C3Y4Z5B7"
    }
}

fake_spaces_db = {
    1: {
        "space_id": 1,
        "name": "Главный Open-Space",
        "type": "open-space",
        "price_per_hour": 300,
        "amenities": ["Wi-Fi", "Coffee", "Принтер"]
    },
    2: {
        "space_id": 2,
        "name": "Переговорная 'Альфа'",
        "type": "meeting-room",
        "price_per_hour": 1000,
        "amenities": ["Wi-Fi", "Проектор", "Флипчарт", "Кондиционер"]
    }
}

fake_bookings_db = {}