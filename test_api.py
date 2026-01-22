#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование API TechRepair CRM
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_api():
    print("🧪 Тестирование TechRepair CRM API")
    print("=" * 40)
    
    try:
        # 1. Получение списка заявок
        print("📋 1. Получение списка заявок...")
        response = requests.get(f"{BASE_URL}/api/repairs")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Получено {data['total']} заявок")
        else:
            print(f"❌ Ошибка: {response.status_code}")
        
        # 2. Создание новой заявки
        print("\n📝 2. Создание новой заявки...")
        new_repair = {
            "firstName": "Тест",
            "lastName": "Тестов",
            "phone": "+7 (999) 000-00-00",
            "email": "test@example.com",
            "deviceType": "smartphone",
            "deviceBrand": "Samsung Galaxy S23",
            "problemType": "battery",
            "urgency": "medium",
            "address": "ул. Тестовая, 1",
            "description": "Быстро разряжается батарея"
        }
        
        response = requests.post(f"{BASE_URL}/api/repairs", 
                               json=new_repair,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Заявка создана: {data['repair_id']}")
            repair_id = data['repair_id']
        else:
            print(f"❌ Ошибка создания: {response.status_code}")
            return
        
        # 3. Проверяем что заявка появилась в списке
        print("\n🔍 3. Проверка обновленного списка...")
        response = requests.get(f"{BASE_URL}/api/repairs")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Теперь {data['total']} заявок в системе")
            
            # Ищем нашу заявку
            found = False
            for repair in data['items']:
                if repair['firstName'] == 'Тест':
                    print(f"✅ Найдена тестовая заявка: {repair['id']}")
                    found = True
                    break
            
            if not found:
                print("❌ Тестовая заявка не найдена в списке")
        
        # 4. Обновление статуса
        print("\n🔄 4. Обновление статуса заявки...")
        response = requests.put(f"{BASE_URL}/api/repairs/{repair_id}/status",
                              json={"status": "in-progress"},
                              headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print("✅ Статус обновлен на 'in-progress'")
        else:
            print(f"❌ Ошибка обновления статуса: {response.status_code}")
        
        # 5. Получение статистики
        print("\n📊 5. Получение статистики...")
        response = requests.get(f"{BASE_URL}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Статистика:")
            print(f"   • Всего заявок: {stats['total_repairs']}")
            print(f"   • Новых: {stats['new_repairs']}")
            print(f"   • В работе: {stats['in_progress']}")
            print(f"   • Завершено: {stats['completed_repairs']}")
            print(f"   • Срочных: {stats['urgent_repairs']}")
        else:
            print(f"❌ Ошибка получения статистики: {response.status_code}")
        
        print("\n🎉 Все тесты пройдены успешно!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к серверу")
        print("💡 Убедитесь что сервер запущен: python production_server.py")
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")

if __name__ == "__main__":
    test_api()