# Сборка Pairwise для Windows

## 1. Установить Python 3

Скачать с https://www.python.org/downloads/ — **Python 3.10+**.

**ВАЖНО при установке:** поставить галочку **"Add Python to PATH"**.

Проверить установку:
```cmd
python --version
```

## 2. Установить зависимости

Открыть командную строку (cmd) в папке `windows_build\` и выполнить:

```cmd
python -m pip install -r requirements.txt
python -m pip install pyinstaller
```

> Если `python` не найден, попробуйте `py` вместо `python`.

## 3. Собрать .exe

```cmd
build_windows.bat
```

Результат: `dist\Pairwise\Pairwise.exe`

## 4. Установить Inno Setup

Скачать с https://jrsoftware.org/isinfo.php и установить.

## 5. Собрать установщик

```cmd
build_windows.bat installer
```

Результат: `Pairwise-Windows-Setup.exe`

## Если иконка на рабочем столе не обновилась

Windows кэширует иконки. После установки новой версии:

1. **Способ 1 (простой):** Перезагрузить компьютер
2. **Способ 2 (без перезагрузки):**
   - Открыть командную строку (cmd) от имени администратора
   - Выполнить: `ie4uinit.exe -show`
   - Или: `taskkill /f /im explorer.exe & start explorer.exe`
3. **Способ 3:** Удалить ярлык с рабочего стола и создать новый через меню Пуск