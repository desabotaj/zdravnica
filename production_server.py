#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production-ready сервер для TechRepair CRM
Готов для деплоя на сервер
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import uuid
from datetime import datetime
import threading

# Файл для хранения заявок
DATA_FILE = 'repairs_data.json'
LOCK = threading.Lock()

# Глобальное хранилище заявок
REPAIRS_STORAGE = []

# Доп. хранилища для CRM
CUSTOMERS_FILE = 'customers_data.json'
INVENTORY_FILE = 'inventory_data.json'
APPOINTMENTS_FILE = 'appointments_data.json'
SETTINGS_FILE = 'settings_data.json'

CUSTOMERS_STORAGE = []
INVENTORY_STORAGE = []
APPOINTMENTS_STORAGE = []
SETTINGS_STORAGE = {}


def _load_json_file(path, default):
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except Exception as e:
        print(f"❌ Ошибка чтения {path}: {e}")
        return default


def _save_json_file(path, data):
    try:
        with LOCK:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Ошибка записи {path}: {e}")

def load_repairs():
    """Загрузка заявок из файла"""
    global REPAIRS_STORAGE
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                REPAIRS_STORAGE = data.get('repairs', [])
                print(f"📂 Загружено {len(REPAIRS_STORAGE)} заявок из файла")
        else:
            # Создаем демо-данные при первом запуске
            REPAIRS_STORAGE = [
                {
                    "id": "repair_001",
                    "firstName": "Алексей",
                    "lastName": "Петров",
                    "phone": "+7 (999) 123-45-67",
                    "email": "alex@example.com",
                    "deviceType": "smartphone",
                    "deviceBrand": "iPhone 14 Pro",
                    "problemType": "screen",
                    "urgency": "high",
                    "address": "ул. Ленина, 15, кв. 42",
                    "description": "Разбился экран после падения. Тачскрин не работает.",
                    "status": "new",
                    "timestamp": "2026-01-22T10:30:00Z",
                    "source": "demo"
                },
                {
                    "id": "repair_002",
                    "firstName": "Мария",
                    "lastName": "Сидорова",
                    "phone": "+7 (999) 987-65-43",
                    "email": "maria@example.com",
                    "deviceType": "laptop",
                    "deviceBrand": "HP Pavilion 15",
                    "problemType": "performance",
                    "urgency": "medium",
                    "address": "пр. Мира, 88",
                    "description": "Ноутбук очень медленно работает, долго загружается.",
                    "status": "in-progress",
                    "timestamp": "2026-01-21T14:15:00Z",
                    "source": "demo"
                }
            ]
            save_repairs()
            print(f"📝 Созданы демо-данные: {len(REPAIRS_STORAGE)} заявок")
    except Exception as e:
        print(f"❌ Ошибка загрузки данных: {e}")
        REPAIRS_STORAGE = []

    # Загружаем остальные данные CRM
    load_customers()
    load_inventory()
    load_appointments()
    load_settings()


def load_customers():
    global CUSTOMERS_STORAGE
    data = _load_json_file(CUSTOMERS_FILE, {"items": []})
    CUSTOMERS_STORAGE = data.get("items", []) if isinstance(data, dict) else (data or [])


def save_customers():
    _save_json_file(CUSTOMERS_FILE, {"items": CUSTOMERS_STORAGE, "last_updated": datetime.now().isoformat(), "total": len(CUSTOMERS_STORAGE)})


def load_inventory():
    global INVENTORY_STORAGE
    data = _load_json_file(INVENTORY_FILE, {"items": []})
    INVENTORY_STORAGE = data.get("items", []) if isinstance(data, dict) else (data or [])


def save_inventory():
    _save_json_file(INVENTORY_FILE, {"items": INVENTORY_STORAGE, "last_updated": datetime.now().isoformat(), "total": len(INVENTORY_STORAGE)})


def load_appointments():
    global APPOINTMENTS_STORAGE
    data = _load_json_file(APPOINTMENTS_FILE, {"items": []})
    APPOINTMENTS_STORAGE = data.get("items", []) if isinstance(data, dict) else (data or [])


def save_appointments():
    _save_json_file(APPOINTMENTS_FILE, {"items": APPOINTMENTS_STORAGE, "last_updated": datetime.now().isoformat(), "total": len(APPOINTMENTS_STORAGE)})


def load_settings():
    global SETTINGS_STORAGE
    data = _load_json_file(SETTINGS_FILE, {})
    SETTINGS_STORAGE = data if isinstance(data, dict) else {}


def save_settings():
    _save_json_file(SETTINGS_FILE, SETTINGS_STORAGE)


def _customer_key(phone: str, email: str):
    phone = (phone or "").strip()
    email = (email or "").strip().lower()
    return phone or email or None


def upsert_customer_from_repair(repair: dict):
    """Создаёт/обновляет клиента по заявке (по телефону или email)"""
    key = _customer_key(repair.get("phone"), repair.get("email"))
    if not key:
        return
    with LOCK:
        existing = None
        for c in CUSTOMERS_STORAGE:
            if _customer_key(c.get("phone"), c.get("email")) == key:
                existing = c
                break
        if existing:
            # обновляем контактные данные/имя, но не затираем явно заполненное пустым
            for field in ("firstName", "lastName", "phone", "email"):
                v = repair.get(field)
                if v:
                    existing[field] = v
            existing["updated_at"] = datetime.now().isoformat()
        else:
            CUSTOMERS_STORAGE.insert(0, {
                "id": str(uuid.uuid4()),
                "firstName": repair.get("firstName", ""),
                "lastName": repair.get("lastName", ""),
                "phone": repair.get("phone", ""),
                "email": repair.get("email", ""),
                "note": "",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            })
    save_customers()

def save_repairs():
    """Сохранение заявок в файл"""
    try:
        with LOCK:
            data = {
                "repairs": REPAIRS_STORAGE,
                "last_updated": datetime.now().isoformat(),
                "total": len(REPAIRS_STORAGE)
            }
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 Сохранено {len(REPAIRS_STORAGE)} заявок")
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")

class ProductionHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        """Логирование с временной меткой"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")
    
    def do_GET(self):
        """Обработка GET запросов"""
        try:
            path = self.path.split('?')[0]  # Убираем query параметры
            
            # Главная страница
            if path == '/' or path == '/index.html':
                self.send_main_page()
            
            # API для заявок
            elif path == '/api/repairs':
                self.send_repairs_api()
            
            # Конкретная заявка
            elif path.startswith('/api/repairs/') and not path.endswith('/status'):
                repair_id = path.split('/')[-1]
                self.send_repair_by_id(repair_id)
            
            # Статистика
            elif path == '/api/stats':
                self.send_stats_api()

            # CRM: клиенты/склад/календарь/настройки
            elif path == '/api/customers':
                self.send_customers_api()
            elif path.startswith('/api/customers/'):
                customer_id = path.split('/')[-1]
                self.send_customer_by_id(customer_id)
            elif path == '/api/inventory':
                self.send_inventory_api()
            elif path.startswith('/api/inventory/'):
                item_id = path.split('/')[-1]
                self.send_inventory_by_id(item_id)
            elif path == '/api/appointments':
                self.send_appointments_api()
            elif path.startswith('/api/appointments/'):
                appt_id = path.split('/')[-1]
                self.send_appointment_by_id(appt_id)
            elif path == '/api/settings':
                self.send_settings_api()
            
            # HTML файлы
            elif path.endswith('.html'):
                filename = path.lstrip('/')
                self.send_html_file(filename)
            
            # Статические файлы
            elif path.startswith('/static/'):
                self.send_static_file(path)
            elif path.startswith('/styles/'):
                self.send_static_file(path)
            
            # Все остальное
            else:
                self.send_json_response({"status": "ok", "path": path})
                
        except Exception as e:
            print(f"❌ Ошибка GET {self.path}: {e}")
            self.send_json_response({"error": str(e)}, 500)
    
    def do_POST(self):
        """Обработка POST запросов"""
        try:
            path = self.path
            
            if path == '/api/repairs':
                self.create_repair()
            elif path == '/api/customers':
                self.create_customer()
            elif path == '/api/inventory':
                self.create_inventory_item()
            elif path == '/api/appointments':
                self.create_appointment()
            else:
                self.send_json_response({"status": "ok", "message": "POST processed"})
                
        except Exception as e:
            print(f"❌ Ошибка POST {self.path}: {e}")
            self.send_json_response({"error": str(e)}, 500)
    
    def do_PUT(self):
        """Обработка PUT запросов"""
        try:
            path = self.path
            
            if '/api/repairs/' in path and '/status' in path:
                self.update_repair_status()
            elif path.startswith('/api/repairs/'):
                self.update_repair()
            elif path.startswith('/api/customers/'):
                self.update_customer()
            elif path.startswith('/api/inventory/'):
                self.update_inventory_item()
            elif path.startswith('/api/appointments/'):
                self.update_appointment()
            elif path == '/api/settings':
                self.update_settings()
            else:
                self.send_json_response({"status": "updated"})
                
        except Exception as e:
            print(f"❌ Ошибка PUT {self.path}: {e}")
            self.send_json_response({"error": str(e)}, 500)
    
    def do_DELETE(self):
        """Обработка DELETE запросов"""
        try:
            path = self.path
            
            if path.startswith('/api/repairs/'):
                self.delete_repair()
            elif path.startswith('/api/customers/'):
                self.delete_customer()
            elif path.startswith('/api/inventory/'):
                self.delete_inventory_item()
            elif path.startswith('/api/appointments/'):
                self.delete_appointment()
            else:
                self.send_json_response({"status": "deleted"})
                
        except Exception as e:
            print(f"❌ Ошибка DELETE {self.path}: {e}")
            self.send_json_response({"error": str(e)}, 500)
    
    def do_OPTIONS(self):
        """Обработка OPTIONS для CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def create_repair(self):
        """Создание новой заявки"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Создаем новую заявку
                new_repair = {
                    "id": str(uuid.uuid4()),
                    "firstName": data.get('firstName', ''),
                    "lastName": data.get('lastName', ''),
                    "phone": data.get('phone', ''),
                    "email": data.get('email', ''),
                    "deviceType": data.get('deviceType', ''),
                    "deviceBrand": data.get('deviceBrand', ''),
                    "problemType": data.get('problemType', ''),
                    "urgency": data.get('urgency', 'low'),
                    "address": data.get('address', ''),
                    "description": data.get('description', ''),
                    "status": "new",
                    "timestamp": datetime.now().isoformat(),
                    "source": "repair_landing"
                }
                
                # Добавляем в начало списка
                with LOCK:
                    REPAIRS_STORAGE.insert(0, new_repair)
                
                # Сохраняем в файл
                save_repairs()
                # Обновляем клиентов
                upsert_customer_from_repair(new_repair)
                
                print(f"✅ Новая заявка: {new_repair['firstName']} {new_repair['lastName']} - {new_repair['deviceType']}")
                
                self.send_json_response({
                    "status": "success",
                    "message": "Заявка создана успешно",
                    "repair_id": new_repair['id']
                })
            else:
                self.send_json_response({"error": "Нет данных"}, 400)
                
        except Exception as e:
            print(f"❌ Ошибка создания заявки: {e}")
            self.send_json_response({"error": f"Ошибка создания заявки: {str(e)}"}, 500)
    
    def update_repair_status(self):
        """Обновление статуса заявки"""
        try:
            repair_id = self.path.split('/')[-2]
            
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                new_status = data.get('status')
                
                # Находим и обновляем заявку
                with LOCK:
                    for repair in REPAIRS_STORAGE:
                        if repair['id'] == repair_id:
                            old_status = repair['status']
                            repair['status'] = new_status
                            repair['updated_at'] = datetime.now().isoformat()
                            
                            if new_status == 'completed':
                                repair['completion_date'] = datetime.now().isoformat()
                            
                            save_repairs()
                            
                            print(f"🔄 Статус заявки {repair_id}: {old_status} → {new_status}")
                            
                            self.send_json_response({
                                "status": "success",
                                "message": f"Статус изменен на '{new_status}'"
                            })
                            return
                
                self.send_json_response({"error": "Заявка не найдена"}, 404)
            else:
                self.send_json_response({"error": "Нет данных"}, 400)
                
        except Exception as e:
            print(f"❌ Ошибка обновления статуса: {e}")
            self.send_json_response({"error": str(e)}, 500)
    
    def delete_repair(self):
        """Удаление заявки"""
        try:
            repair_id = self.path.split('/')[-1]
            
            with LOCK:
                original_length = len(REPAIRS_STORAGE)
                REPAIRS_STORAGE[:] = [r for r in REPAIRS_STORAGE if r['id'] != repair_id]
                
                if len(REPAIRS_STORAGE) < original_length:
                    save_repairs()
                    print(f"🗑️ Заявка удалена: {repair_id}")
                    self.send_json_response({"status": "success", "message": "Заявка удалена"})
                else:
                    self.send_json_response({"error": "Заявка не найдена"}, 404)
                    
        except Exception as e:
            print(f"❌ Ошибка удаления: {e}")
            self.send_json_response({"error": str(e)}, 500)
    
    def send_main_page(self):
        """Отправка главной страницы"""
        if os.path.exists('index.html'):
            self.send_html_file('index.html')
        elif os.path.exists('repair_landing.html'):
            self.send_html_file('repair_landing.html')
        else:
            self.send_fallback_page()
    
    def send_repairs_api(self):
        """API для получения заявок"""
        try:
            # Фильтрация и поиск (если нужно)
            query_params = self.path.split('?')[1] if '?' in self.path else ''
            
            response = {
                "items": REPAIRS_STORAGE,
                "total": len(REPAIRS_STORAGE),
                "page": 1,
                "per_page": 50,
                "timestamp": datetime.now().isoformat()
            }
            
            self.send_json_response(response)
            
        except Exception as e:
            print(f"❌ Ошибка API заявок: {e}")
            self.send_json_response({"error": str(e)}, 500)
    
    def send_repair_by_id(self, repair_id):
        """Получение конкретной заявки"""
        try:
            repair = next((r for r in REPAIRS_STORAGE if r['id'] == repair_id), None)
            if repair:
                self.send_json_response(repair)
            else:
                self.send_json_response({"error": "Заявка не найдена"}, 404)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def update_repair(self):
        """Полное обновление заявки (кроме id)"""
        try:
            repair_id = self.path.split('/')[-1]
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_json_response({"error": "Нет данных"}, 400)
                return
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            updated = None
            with LOCK:
                for repair in REPAIRS_STORAGE:
                    if repair.get('id') == repair_id:
                        # Обновляем только известные поля
                        allowed = {
                            "firstName", "lastName", "phone", "email",
                            "deviceType", "deviceBrand", "problemType",
                            "urgency", "address", "description",
                            "status", "technician"
                        }
                        for k, v in data.items():
                            if k in allowed:
                                repair[k] = v
                        repair["updated_at"] = datetime.now().isoformat()
                        updated = repair
                        break

            if not updated:
                self.send_json_response({"error": "Заявка не найдена"}, 404)
                return

            save_repairs()
            upsert_customer_from_repair(updated)
            self.send_json_response({"status": "success", "item": updated})
        except Exception as e:
            print(f"❌ Ошибка обновления заявки: {e}")
            self.send_json_response({"error": str(e)}, 500)

    # -------- Customers API --------
    def send_customers_api(self):
        self.send_json_response({"items": CUSTOMERS_STORAGE, "total": len(CUSTOMERS_STORAGE), "timestamp": datetime.now().isoformat()})

    def send_customer_by_id(self, customer_id):
        customer = next((c for c in CUSTOMERS_STORAGE if c.get("id") == customer_id), None)
        if not customer:
            self.send_json_response({"error": "Клиент не найден"}, 404)
            return
        # считаем количество заявок по ключу
        key = _customer_key(customer.get("phone"), customer.get("email"))
        repairs_count = 0
        if key:
            for r in REPAIRS_STORAGE:
                if _customer_key(r.get("phone"), r.get("email")) == key:
                    repairs_count += 1
        payload = dict(customer)
        payload["repairs_count"] = repairs_count
        self.send_json_response(payload)

    def create_customer(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_json_response({"error": "Нет данных"}, 400)
                return
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            item = {
                "id": str(uuid.uuid4()),
                "firstName": data.get("firstName", ""),
                "lastName": data.get("lastName", ""),
                "phone": data.get("phone", ""),
                "email": data.get("email", ""),
                "note": data.get("note", ""),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
            with LOCK:
                CUSTOMERS_STORAGE.insert(0, item)
            save_customers()
            self.send_json_response({"status": "success", "item": item})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def update_customer(self):
        try:
            customer_id = self.path.split('/')[-1]
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_json_response({"error": "Нет данных"}, 400)
                return
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            updated = None
            with LOCK:
                for c in CUSTOMERS_STORAGE:
                    if c.get("id") == customer_id:
                        for k in ("firstName", "lastName", "phone", "email", "note"):
                            if k in data:
                                c[k] = data.get(k, "")
                        c["updated_at"] = datetime.now().isoformat()
                        updated = c
                        break
            if not updated:
                self.send_json_response({"error": "Клиент не найден"}, 404)
                return
            save_customers()
            self.send_json_response({"status": "success", "item": updated})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def delete_customer(self):
        try:
            customer_id = self.path.split('/')[-1]
            with LOCK:
                before = len(CUSTOMERS_STORAGE)
                CUSTOMERS_STORAGE[:] = [c for c in CUSTOMERS_STORAGE if c.get("id") != customer_id]
            if len(CUSTOMERS_STORAGE) == before:
                self.send_json_response({"error": "Клиент не найден"}, 404)
                return
            save_customers()
            self.send_json_response({"status": "success"})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    # -------- Inventory API --------
    def send_inventory_api(self):
        self.send_json_response({"items": INVENTORY_STORAGE, "total": len(INVENTORY_STORAGE), "timestamp": datetime.now().isoformat()})

    def send_inventory_by_id(self, item_id):
        item = next((i for i in INVENTORY_STORAGE if i.get("id") == item_id), None)
        if not item:
            self.send_json_response({"error": "Позиция не найдена"}, 404)
            return
        self.send_json_response(item)

    def create_inventory_item(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_json_response({"error": "Нет данных"}, 400)
                return
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            item = {
                "id": str(uuid.uuid4()),
                "name": data.get("name", ""),
                "sku": data.get("sku", ""),
                "qty": data.get("qty", 0),
                "min_qty": data.get("min_qty", 0),
                "location": data.get("location", ""),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
            with LOCK:
                INVENTORY_STORAGE.insert(0, item)
            save_inventory()
            self.send_json_response({"status": "success", "item": item})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def update_inventory_item(self):
        try:
            item_id = self.path.split('/')[-1]
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_json_response({"error": "Нет данных"}, 400)
                return
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            updated = None
            with LOCK:
                for i in INVENTORY_STORAGE:
                    if i.get("id") == item_id:
                        for k in ("name", "sku", "qty", "min_qty", "location"):
                            if k in data:
                                i[k] = data.get(k)
                        i["updated_at"] = datetime.now().isoformat()
                        updated = i
                        break
            if not updated:
                self.send_json_response({"error": "Позиция не найдена"}, 404)
                return
            save_inventory()
            self.send_json_response({"status": "success", "item": updated})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def delete_inventory_item(self):
        try:
            item_id = self.path.split('/')[-1]
            with LOCK:
                before = len(INVENTORY_STORAGE)
                INVENTORY_STORAGE[:] = [i for i in INVENTORY_STORAGE if i.get("id") != item_id]
            if len(INVENTORY_STORAGE) == before:
                self.send_json_response({"error": "Позиция не найдена"}, 404)
                return
            save_inventory()
            self.send_json_response({"status": "success"})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    # -------- Appointments API --------
    def send_appointments_api(self):
        self.send_json_response({"items": APPOINTMENTS_STORAGE, "total": len(APPOINTMENTS_STORAGE), "timestamp": datetime.now().isoformat()})

    def send_appointment_by_id(self, appt_id):
        item = next((a for a in APPOINTMENTS_STORAGE if a.get("id") == appt_id), None)
        if not item:
            self.send_json_response({"error": "Запись не найдена"}, 404)
            return
        self.send_json_response(item)

    def create_appointment(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_json_response({"error": "Нет данных"}, 400)
                return
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            item = {
                "id": str(uuid.uuid4()),
                "start": data.get("start", ""),
                "customer": data.get("customer", ""),
                "title": data.get("title", ""),
                "technician": data.get("technician", ""),
                "status": data.get("status", "planned"),
                "note": data.get("note", ""),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
            with LOCK:
                APPOINTMENTS_STORAGE.insert(0, item)
            save_appointments()
            self.send_json_response({"status": "success", "item": item})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def update_appointment(self):
        try:
            appt_id = self.path.split('/')[-1]
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_json_response({"error": "Нет данных"}, 400)
                return
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            updated = None
            with LOCK:
                for a in APPOINTMENTS_STORAGE:
                    if a.get("id") == appt_id:
                        for k in ("start", "customer", "title", "technician", "status", "note"):
                            if k in data:
                                a[k] = data.get(k)
                        a["updated_at"] = datetime.now().isoformat()
                        updated = a
                        break
            if not updated:
                self.send_json_response({"error": "Запись не найдена"}, 404)
                return
            save_appointments()
            self.send_json_response({"status": "success", "item": updated})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def delete_appointment(self):
        try:
            appt_id = self.path.split('/')[-1]
            with LOCK:
                before = len(APPOINTMENTS_STORAGE)
                APPOINTMENTS_STORAGE[:] = [a for a in APPOINTMENTS_STORAGE if a.get("id") != appt_id]
            if len(APPOINTMENTS_STORAGE) == before:
                self.send_json_response({"error": "Запись не найдена"}, 404)
                return
            save_appointments()
            self.send_json_response({"status": "success"})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    # -------- Settings API --------
    def send_settings_api(self):
        self.send_json_response(SETTINGS_STORAGE or {})

    def update_settings(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_json_response({"error": "Нет данных"}, 400)
                return
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            if not isinstance(data, dict):
                self.send_json_response({"error": "Неверный формат"}, 400)
                return
            with LOCK:
                SETTINGS_STORAGE.update(data)
                SETTINGS_STORAGE["updated_at"] = datetime.now().isoformat()
            save_settings()
            self.send_json_response({"status": "success", "settings": SETTINGS_STORAGE})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)
    
    def send_stats_api(self):
        """API статистики"""
        try:
            total = len(REPAIRS_STORAGE)
            new_count = len([r for r in REPAIRS_STORAGE if r['status'] == 'new'])
            in_progress = len([r for r in REPAIRS_STORAGE if r['status'] == 'in-progress'])
            completed = len([r for r in REPAIRS_STORAGE if r['status'] == 'completed'])
            urgent = len([r for r in REPAIRS_STORAGE if r['urgency'] == 'high'])
            
            # Заявки за сегодня
            today = datetime.now().date()
            today_count = 0
            for repair in REPAIRS_STORAGE:
                try:
                    repair_date = datetime.fromisoformat(repair['timestamp'].replace('Z', '+00:00')).date()
                    if repair_date == today:
                        today_count += 1
                except:
                    pass
            
            stats = {
                "total_repairs": total,
                "new_repairs": new_count,
                "in_progress": in_progress,
                "completed_repairs": completed,
                "urgent_repairs": urgent,
                "today_repairs": today_count,
                "timestamp": datetime.now().isoformat()
            }
            
            self.send_json_response(stats)
            
        except Exception as e:
            print(f"❌ Ошибка статистики: {e}")
            self.send_json_response({"error": str(e)}, 500)
    
    def send_html_file(self, filename):
        """Отправка HTML файла"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                
            else:
                print(f"❌ Файл не найден: {filename}")
                self.send_fallback_page()
                
        except Exception as e:
            print(f"❌ Ошибка файла {filename}: {e}")
            self.send_json_response({"error": f"File error: {e}"}, 500)
    
    def send_static_file(self, path):
        """Отправка статических файлов"""
        try:
            filename = path[1:]  # Убираем ведущий /
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    content = f.read()
                
                # Определяем MIME тип
                if filename.endswith('.css'):
                    content_type = 'text/css'
                elif filename.endswith('.js'):
                    content_type = 'application/javascript'
                elif filename.endswith('.png'):
                    content_type = 'image/png'
                elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif filename.endswith('.svg'):
                    content_type = 'image/svg+xml'
                else:
                    content_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Cache-Control', 'public, max-age=3600')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_json_response({"error": "Static file not found"}, 404)
                
        except Exception as e:
            print(f"❌ Ошибка статического файла {path}: {e}")
            self.send_json_response({"error": str(e)}, 500)
    
    def send_fallback_page(self):
        """Fallback страница если основные файлы не найдены"""
        html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechRepair CRM</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        h1 { font-size: 3em; margin-bottom: 20px; }
        .btn {
            display: inline-block;
            padding: 15px 30px;
            margin: 10px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
        }
        .btn:hover { background: #2980b9; }
        .status { margin: 20px 0; padding: 15px; background: rgba(0,255,0,0.2); border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 TechRepair CRM</h1>
        <div class="status">
            ✅ Сервер работает<br>
            📊 API доступно<br>
            💾 Данные сохраняются
        </div>
        <p>Система управления заявками на ремонт техники</p>
        <a href="/api/repairs" class="btn">📋 API Заявок</a>
        <a href="/api/stats" class="btn">📊 Статистика</a>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_json_response(self, data, status=200):
        """Отправка JSON ответа"""
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            response = json.dumps(data, ensure_ascii=False, indent=2)
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Ошибка JSON ответа: {e}")

def main():
    # Настройки сервера
    PORT = int(os.environ.get('PORT', 8001))  # Поддержка переменной окружения для деплоя
    HOST = os.environ.get('HOST', '0.0.0.0')  # 0.0.0.0 для деплоя на сервер
    
    print("🔧 TechRepair CRM - Production Server")
    print("=" * 50)
    print(f"🌐 Хост: {HOST}")
    print(f"🔌 Порт: {PORT}")
    print(f"📂 Файл данных: {DATA_FILE}")
    print("=" * 50)
    
    # Загружаем данные при запуске
    load_repairs()
    
    try:
        server = HTTPServer((HOST, PORT), ProductionHandler)
        print(f"✅ Сервер запущен на {HOST}:{PORT}")
        print("📱 Доступные URL:")
        print(f"   • Главная: http://{HOST}:{PORT}")
        print(f"   • API заявок: http://{HOST}:{PORT}/api/repairs")
        print(f"   • Статистика: http://{HOST}:{PORT}/api/stats")
        print("⏹️ Для остановки нажмите Ctrl+C")
        print()
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
        print("💾 Данные сохранены в файл")
    except OSError as e:
        if "Address already in use" in str(e) or "10048" in str(e):
            print(f"❌ Порт {PORT} уже используется!")
            print("💡 Попробуйте изменить порт через переменную окружения PORT")
        else:
            print(f"❌ Ошибка сети: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Сохраняем данные при завершении
        save_repairs()
        save_customers()
        save_inventory()
        save_appointments()
        save_settings()

if __name__ == "__main__":
    main()