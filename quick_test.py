#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрый тест API
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8001"
    
    print("🧪 Быстрый тест API")
    print("=" * 30)
    
    try:
        # Тест получения заявок
        print("📋 Тестируем /api/repairs...")
        response = requests.get(f"{base_url}/api/repairs", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API работает! Заявок: {data.get('total', len(data.get('items', [])))}")
            
            # Показываем первые несколько заявок
            items = data.get('items', data.get('repairs', []))
            for i, repair in enumerate(items[:3]):
                print(f"   {i+1}. {repair['firstName']} {repair.get('lastName', '')} - {repair['deviceType']} ({repair['status']})")
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Сервер не запущен или недоступен")
        print("💡 Запустите: python production_server.py")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_api()