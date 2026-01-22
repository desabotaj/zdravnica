#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовые данные для CRM системы ремонта техники
"""

from datetime import datetime, timedelta
import uuid

# Мок данные для мастера/администратора
ADMIN_DATA = {
    "user": {
        "id": 1,
        "name": "Сергей Мастеров",
        "email": "master@techrepair.com",
        "phone": "+7 (999) 100-20-30",
        "avatar": "/static/avatars/master.png",
        "rating": 4.9,
        "completed_repairs": 247,
        "verified": True,
        "registration_date": "2019-05-10",
        "specialization": ["Смартфоны", "Планшеты", "Ноутбуки", "ПК"]
    },
    "stats": {
        "active_repairs": 8,
        "completed_today": 3,
        "pending_calls": 5,
        "revenue_month": 125000,
        "avg_repair_time": "2.5 дня"
    }
}

# Мок данные для заявок на ремонт
REPAIRS_DATA = {
    "items": [
        {
            "id": "repair_001",
            "firstName": "Алексей",
            "lastName": "Петров",
            "phone": "+7 (999) 123-45-67",
            "email": "alex.petrov@email.com",
            "deviceType": "smartphone",
            "deviceBrand": "iPhone 14 Pro",
            "problemType": "screen",
            "urgency": "high",
            "address": "ул. Ленина, 15, кв. 42",
            "description": "Разбился экран после падения. Тачскрин не работает, видны трещины по всему экрану.",
            "status": "new",
            "created_at": "2026-01-22T10:30:00Z",
            "estimated_cost": 15000,
            "estimated_time": "1-2 дня",
            "assigned_master": None
        },
        {
            "id": "repair_002",
            "firstName": "Мария",
            "lastName": "Сидорова",
            "phone": "+7 (999) 987-65-43",
            "email": "maria.s@mail.ru",
            "deviceType": "laptop",
            "deviceBrand": "HP Pavilion 15",
            "problemType": "performance",
            "urgency": "medium",
            "address": "пр. Мира, 88, офис 12",
            "description": "Ноутбук очень медленно работает, долго загружается, зависает при работе с документами.",
            "status": "in-progress",
            "created_at": "2026-01-21T14:15:00Z",
            "estimated_cost": 3500,
            "estimated_time": "2-3 дня",
            "assigned_master": "Сергей Мастеров"
        },
        {
            "id": "repair_003",
            "firstName": "Дмитрий",
            "lastName": "Козлов",
            "phone": "+7 (999) 555-44-33",
            "email": "dmitry.kozlov@gmail.com",
            "deviceType": "tablet",
            "deviceBrand": "iPad Air 5",
            "problemType": "charging",
            "urgency": "low",
            "address": "ул. Гагарина, 25",
            "description": "Планшет не заряжается, при подключении зарядки индикатор не загорается.",
            "status": "completed",
            "created_at": "2026-01-20T09:45:00Z",
            "estimated_cost": 4500,
            "estimated_time": "1 день",
            "assigned_master": "Сергей Мастеров",
            "completion_date": "2026-01-21T16:30:00Z",
            "final_cost": 4200
        },
        {
            "id": "repair_004",
            "firstName": "Елена",
            "lastName": "Волкова",
            "phone": "+7 (999) 777-88-99",
            "email": "",
            "deviceType": "desktop",
            "deviceBrand": "Самосборный ПК",
            "problemType": "other",
            "urgency": "medium",
            "address": "",
            "description": "Компьютер не включается, при нажатии на кнопку питания ничего не происходит.",
            "status": "new",
            "created_at": "2026-01-22T08:20:00Z",
            "estimated_cost": 5000,
            "estimated_time": "1-3 дня",
            "assigned_master": None
        }
    ],
    "total": 4,
    "page": 1,
    "per_page": 20
}

# Мок данные для уведомлений и сообщений
NOTIFICATIONS_DATA = {
    "notifications": [
        {
            "id": "notif_001",
            "type": "new_repair",
            "title": "Новая заявка на ремонт",
            "message": "Алексей Петров оставил заявку на ремонт iPhone 14 Pro",
            "timestamp": "2026-01-22T10:30:00Z",
            "read": False,
            "priority": "high",
            "repair_id": "repair_001"
        },
        {
            "id": "notif_002",
            "type": "urgent_repair",
            "title": "Срочная заявка",
            "message": "Елена Волкова - экстренный ремонт ПК",
            "timestamp": "2026-01-22T08:20:00Z",
            "read": False,
            "priority": "urgent",
            "repair_id": "repair_004"
        },
        {
            "id": "notif_003",
            "type": "repair_completed",
            "title": "Ремонт завершен",
            "message": "iPad Air 5 - ремонт завершен успешно",
            "timestamp": "2026-01-21T16:30:00Z",
            "read": True,
            "priority": "normal",
            "repair_id": "repair_003"
        }
    ],
    "total_unread": 2
}

# Детальная информация о ремонтах
REPAIR_DETAILS = {
    "repair_001": {
        "parts_needed": [
            {"name": "Дисплей iPhone 14 Pro", "cost": 12000, "available": True},
            {"name": "Защитное стекло", "cost": 500, "available": True}
        ],
        "work_log": [
            {"timestamp": "2026-01-22T10:30:00Z", "action": "Заявка получена", "master": "Система"},
            {"timestamp": "2026-01-22T10:35:00Z", "action": "Первичная диагностика", "master": "Сергей Мастеров"}
        ],
        "photos": [
            "/static/repairs/repair_001_before_1.jpg",
            "/static/repairs/repair_001_before_2.jpg"
        ]
    }
}

# Статистика сервиса
SERVICE_STATS = {
    "today": {
        "new_repairs": 2,
        "completed_repairs": 1,
        "in_progress": 3,
        "revenue": 8700
    },
    "week": {
        "new_repairs": 15,
        "completed_repairs": 12,
        "revenue": 67500,
        "avg_repair_time": 2.3
    },
    "month": {
        "new_repairs": 58,
        "completed_repairs": 52,
        "revenue": 245000,
        "customer_satisfaction": 4.8
    }
}

# Настройки сервиса
SERVICE_SETTINGS = {
    "business_hours": {
        "monday": {"open": "09:00", "close": "19:00"},
        "tuesday": {"open": "09:00", "close": "19:00"},
        "wednesday": {"open": "09:00", "close": "19:00"},
        "thursday": {"open": "09:00", "close": "19:00"},
        "friday": {"open": "09:00", "close": "19:00"},
        "saturday": {"open": "10:00", "close": "17:00"},
        "sunday": {"closed": True}
    },
    "contact": {
        "phone": "+7 (999) 100-20-30",
        "email": "info@techrepair.com",
        "address": "г. Москва, ул. Техническая, 15"
    },
    "pricing": {
        "diagnostic": 500,
        "urgent_multiplier": 1.5,
        "home_visit": 1000
    }
}

# Типы устройств и проблем
DEVICE_TYPES = {
    "smartphone": {
        "name": "📱 Смартфон",
        "common_problems": ["screen", "battery", "charging", "water", "software"]
    },
    "tablet": {
        "name": "📟 Планшет", 
        "common_problems": ["screen", "charging", "software", "performance"]
    },
    "laptop": {
        "name": "💻 Ноутбук",
        "common_problems": ["performance", "screen", "battery", "charging", "software"]
    },
    "desktop": {
        "name": "🖥️ Настольный ПК",
        "common_problems": ["performance", "software", "connectivity", "other"]
    }
}

PROBLEM_TYPES = {
    "screen": {"name": "🖥️ Проблемы с экраном", "avg_cost": 8000, "avg_time": "1-2 дня"},
    "battery": {"name": "🔋 Проблемы с батареей", "avg_cost": 3500, "avg_time": "1 день"},
    "charging": {"name": "🔌 Не заряжается", "avg_cost": 2500, "avg_time": "1 день"},
    "water": {"name": "💧 Попадание жидкости", "avg_cost": 5000, "avg_time": "2-3 дня"},
    "software": {"name": "💾 Программные проблемы", "avg_cost": 2000, "avg_time": "1 день"},
    "performance": {"name": "⚡ Медленная работа", "avg_cost": 3000, "avg_time": "1-2 дня"},
    "audio": {"name": "🔊 Проблемы со звуком", "avg_cost": 2500, "avg_time": "1 день"},
    "connectivity": {"name": "📶 Проблемы с сетью", "avg_cost": 2000, "avg_time": "1 день"},
    "other": {"name": "🔧 Другое", "avg_cost": 4000, "avg_time": "1-3 дня"}
}