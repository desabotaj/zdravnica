@echo off
chcp 65001 >nul
echo 📦 Подготовка проекта к деплою...

REM Создаём папку для деплоя
if not exist deploy_package mkdir deploy_package

REM Копируем нужные файлы
echo 📋 Копирование файлов...
copy production_server.py deploy_package\ >nul
copy index.html deploy_package\ >nul
copy admin.html deploy_package\ >nul
copy requirements.txt deploy_package\ >nul
copy runtime.txt deploy_package\ >nul

REM Копируем папку styles
xcopy /E /I /Y styles deploy_package\styles\ >nul

REM Создаём README для деплоя
(
echo TechRepair CRM - Файлы для деплоя
echo.
echo ИНСТРУКЦИЯ:
echo 1. Загрузите все файлы на хостинг
echo 2. Настройте Python приложение ^(версия 3.10+^)
echo 3. Укажите точку входа: production_server.py
echo 4. Установите переменные окружения:
echo    PORT=8001
echo    HOST=0.0.0.0
echo 5. Запустите приложение
echo.
echo ВАЖНО:
echo - Файлы данных ^(*_data.json^) создадутся автоматически
echo - Убедитесь что у приложения есть права на запись
echo - Для продакшена используйте HTTPS
echo.
echo Подробная инструкция: DEPLOY_RU.md
) > deploy_package\README_DEPLOY.txt

echo ✅ Готово! Файлы для деплоя в папке: deploy_package\
echo 📁 Загрузите содержимое папки на хостинг
pause

