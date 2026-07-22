# Pairwise Test Case Generator

Инструмент для QA-инженеров: генерация тестовых наборов методом Pairwise (All-Pairs Testing) с удобным графическим интерфейсом.

## Возможности

- Ввод параметров и их значений через таблицу
- Генерация минимального набора комбинаций методом Pairwise
- Экспорт результатов в CSV
- Копирование в буфер обмена для вставки в Excel / Google Sheets (TSV-формат)

## Установка

### macOS

1. Скачайте **Pairwise-macOS.dmg** из [Releases](https://github.com/vyaaliy/pairwise/releases).
2. Откройте `.dmg` файл.
3. Перетащите **Pairwise.app** в папку **Applications**.
4. Запустите **Pairwise** из Launchpad или папки Applications.

> При первом запуске macOS может показать предупреждение о неподписанном разработчике.  
> Нажмите правой кнопкой мыши на `Pairwise.app` → **Открыть**, затем подтвердите запуск.

### Windows

1. Скачайте **Pairwise-Windows-Setup.exe** из [Releases](https://github.com/vyaaliy/pairwise/releases).
2. Запустите установщик.
3. Следуйте инструкциям установщика.
4. После установки запустите **Pairwise** через ярлык на рабочем столе или в меню Пуск.

> Если Windows Defender или браузер блокируют установщик, нажмите **"Сохранить всё равно"** / **"Запустить в любом случае"**.

### Запуск из исходного кода (для разработчиков)

```bash
git clone https://github.com/vyaaliy/pairwise.git
cd pairwise
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows
pip install -r requirements.txt
python3 main.py
```

## Как использовать

1. Нажмите **"Добавить параметр"**.
2. Введите название параметра и его значения через запятую.
3. Добавьте необходимое количество параметров.
4. Нажмите **"Сгенерировать"**.
5. Экспортируйте результат в CSV или скопируйте в буфер обмена для вставки в Excel / Google Sheets.

## Сборка дистрибутива

### macOS

```bash
chmod +x build_macos.sh
./build_macos.sh
```

Требуется **Python 3 + PyInstaller**. Результат: `Pairwise-macOS.dmg` (~40 MB).

### Windows

Все необходимые файлы для сборки на Windows находятся в папке **`windows_build/`**:

1. Скопировать `windows_build/` на Windows-машину.
2. Установить Python 3 и зависимости: `pip install -r requirements.txt`
3. Установить PyInstaller: `pip install pyinstaller`
4. Собрать .exe: `build_windows.bat`
5. Установить [Inno Setup](https://jrsoftware.org/isinfo.php)
6. Собрать установщик: `build_windows.bat installer`

Результат: `Pairwise-Windows-Setup.exe`.

## Технологии

- **Python 3** — язык программирования
- **PySide6** — графический интерфейс (Qt)
- **allpairspy** — алгоритм pairwise-генерации
- **PyInstaller** — сборка .app для macOS
- **PyInstaller** — сборка .exe для Windows
- **Inno Setup** — установщик для Windows
- **create-dmg** / hdiutil — создание .dmg для macOS

## Лицензия

MIT License. Copyright © 2026 Timur Poltorakov.