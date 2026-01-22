#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed script: создаёт N тестовых заявок через API production_server.py

Запуск:
  python seed_repairs.py --count 30 --base-url http://127.0.0.1:8001
"""

from __future__ import annotations

import argparse
import json
import random
import string
import sys
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


FIRST_NAMES = [
    "Алексей", "Мария", "Дмитрий", "Елена", "Иван", "Ольга", "Никита", "Анна", "Сергей", "Наталья",
    "Максим", "Ксения", "Артём", "Юлия", "Павел", "Татьяна", "Илья", "Виктория", "Роман", "Светлана",
]
LAST_NAMES = [
    "Петров", "Сидорова", "Козлов", "Волкова", "Иванов", "Смирнова", "Попов", "Соколова", "Лебедев", "Кузнецова",
    "Морозов", "Новикова", "Фёдоров", "Павлова", "Семенов", "Алексеева", "Зайцев", "Яковлева", "Орлов", "Григорьева",
]

DEVICE_TYPES = ["smartphone", "tablet", "laptop", "desktop", "other"]
DEVICE_BRANDS = {
    "smartphone": ["iPhone 12", "iPhone 13", "iPhone 14 Pro", "Samsung Galaxy S23", "Xiaomi Redmi Note 12", "Google Pixel 7"],
    "tablet": ["iPad Air 4", "iPad 10", "Samsung Tab S8", "Xiaomi Pad 6", "Lenovo Tab P11"],
    "laptop": ["MacBook Air M1", "MacBook Pro 14", "HP Pavilion 15", "Lenovo ThinkPad T14", "ASUS VivoBook 15", "Acer Aspire 5"],
    "desktop": ["ПК (самосбор)", "Dell OptiPlex", "HP ProDesk", "Lenovo IdeaCentre"],
    "other": ["Nintendo Switch", "Apple Watch", "Steam Deck", "Пауэрбанк", "Роутер"],
}

PROBLEM_TYPES = ["screen", "battery", "charging", "water", "software", "performance", "audio", "connectivity", "other"]
URGENCIES = ["low", "medium", "high"]
STATUSES = ["new", "in-progress", "completed", "cancelled"]
TECHNICIANS = ["Иван", "Сергей", "Андрей", "Олег", "Мария", "Антон", ""]


def rand_phone() -> str:
    # +7 9XX XXX-XX-XX
    a = random.randint(900, 999)
    b = random.randint(100, 999)
    c = random.randint(10, 99)
    d = random.randint(10, 99)
    return f"+7 ({a}) {b}-{c}-{d}"


def rand_email(first: str, last: str) -> str:
    if random.random() < 0.25:
        return ""
    dom = random.choice(["mail.ru", "gmail.com", "yandex.ru", "outlook.com"])
    suffix = random.randint(1, 9999)
    local = f"{first}.{last}.{suffix}".lower()
    local = local.replace("ё", "e")
    return f"{local}@{dom}"


def rand_address() -> str:
    if random.random() < 0.35:
        return ""
    streets = ["Ленина", "Мира", "Пушкина", "Техническая", "Советская", "Гагарина", "Комсомольская", "Набережная"]
    street = random.choice(streets)
    house = random.randint(1, 180)
    apt = random.randint(1, 250)
    return f"ул. {street}, д. {house}, кв. {apt}"


def rand_description(problem: str, device: str) -> str:
    variants = {
        "screen": [
            "Трещины на экране после падения, сенсор местами не реагирует.",
            "Полосы на дисплее, иногда мерцает.",
            "Экран чёрный, но звук/вибрация есть.",
        ],
        "battery": [
            "Быстро разряжается, выключается на 20–30%.",
            "Греется при зарядке, батарея держит 2–3 часа.",
        ],
        "charging": [
            "Не заряжается, кабель/блок питания меняли — без эффекта.",
            "Зарядка идёт только в определённом положении штекера.",
        ],
        "water": [
            "Попала вода, после этого не включается.",
            "Пролили чай, кнопки залипают, звук стал тише.",
        ],
        "software": [
            "После обновления зависает, приложения вылетают.",
            "Вирус/реклама, нужна чистка и настройка.",
        ],
        "performance": [
            "Тормозит, долго загружается, шумит кулер.",
            "Подвисает при работе с браузером и документами.",
        ],
        "audio": [
            "Динамик хрипит, микрофон плохо слышно.",
            "Нет звука в наушниках, разъём шатается.",
        ],
        "connectivity": [
            "Плохо ловит Wi‑Fi, Bluetooth постоянно отваливается.",
            "Сеть не видит, SIM определяется через раз.",
        ],
        "other": [
            "Нужна диагностика, непонятно в чём проблема.",
            "Периодически перезагружается, иногда не включается.",
        ],
    }
    base = random.choice(variants.get(problem, variants["other"]))
    extra = ""
    if random.random() < 0.35:
        extra = f" ({device})"
    if random.random() < 0.25:
        extra += f" Срочно: {random.choice(['желательно сегодня', 'к завтрашнему дню', 'до выходных'])}."
    return base + extra


def rand_timestamp() -> str:
    now = datetime.now(timezone.utc)
    delta_days = random.randint(0, 14)
    delta_minutes = random.randint(0, 24 * 60)
    ts = now - timedelta(days=delta_days, minutes=delta_minutes)
    return ts.replace(microsecond=0).isoformat()


def rand_status() -> str:
    r = random.random()
    if r < 0.55:
        return "new"
    if r < 0.80:
        return "in-progress"
    if r < 0.95:
        return "completed"
    return "cancelled"


def post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with urlopen(req, timeout=10) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument("--base-url", type=str, default="http://127.0.0.1:8001")
    args = parser.parse_args()

    target = args.base_url.rstrip("/") + "/api/repairs"
    ok = 0
    for i in range(args.count):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        device_type = random.choice(DEVICE_TYPES)
        device_brand = random.choice(DEVICE_BRANDS[device_type])
        problem = random.choice(PROBLEM_TYPES)
        urgency = random.choice(URGENCIES)
        status = rand_status()

        payload = {
            "firstName": first,
            "lastName": last,
            "phone": rand_phone(),
            "email": rand_email(first, last),
            "deviceType": device_type,
            "deviceBrand": device_brand,
            "problemType": problem,
            "urgency": urgency,
            "address": rand_address(),
            "description": rand_description(problem, device_brand),
            "status": status,
            "technician": random.choice(TECHNICIANS),
            "timestamp": rand_timestamp(),
            "source": "seed_repairs.py",
        }

        try:
            post_json(target, payload)
            ok += 1
        except HTTPError as e:
            print(f"[{i+1}/{args.count}] HTTPError: {e.code} {e.reason}", file=sys.stderr)
        except URLError as e:
            print(f"[{i+1}/{args.count}] URLError: {e.reason}", file=sys.stderr)
        except Exception as e:
            print(f"[{i+1}/{args.count}] Error: {e}", file=sys.stderr)

    print(f"✅ Создано заявок: {ok}/{args.count}")
    return 0 if ok == args.count else 2


if __name__ == "__main__":
    raise SystemExit(main())


