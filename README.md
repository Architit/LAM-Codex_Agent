```markdown
# 🧠 LAM-Codex_Agent

**Codex-агент** — это специализированный исполнитель для работы с кодом в экосистеме **LAM (Living Architectonic Mind)**.  
Он принимает промпты, генерирует, исполняет и валидирует код, формируя отклики, пригодные для включения в живую архитектуру системы.

---

## 🎯 Назначение

- Генерация и редактирование кода (Python, Bash, Docker, HTML и др.)
- Запуск сценариев локально или в песочнице
- Тестирование функций и логики через `pytest`, `mypy`, `ruff`
- Работа по промптам от других агентов (например, LAM-Core, Archivator)
- Ведение журналов исполнения и возврат данных в формате LAM

---

## 🧩 Архитектура

```

LAM-Codex\_Agent/
├── README.md                # Текущий файл
├── .gitignore               # Исключения
├── LICENSE                  # MIT License
├── prompts/                 # Шаблоны и реальные промпты
│   └── example.task.md      # Примеры задач
├── src/
│   └── agent/
│       ├── **init**.py
│       ├── core.py          # Главная логика обработки
│       ├── executor.py      # Запуск кода
│       └── formatter.py     # Преобразование данных
├── tests/
│   └── test\_sanity.py       # Первичный тест
└── requirements.txt         # Зависимости

````

---

## 🛠 Установка и запуск

```bash
# Клонируй репозиторий
git clone https://github.com/<твое_имя>/LAM-Codex_Agent.git
cd LAM-Codex_Agent

# Создай виртуальное окружение
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# Установи зависимости
pip install -r requirements.txt

# Запусти тест
pytest -q
````

---

## 📤 Использование

```python
from agent.core import handle_prompt

prompt = "Создай функцию, которая сортирует список строк по длине."
result = handle_prompt(prompt)
print(result.code)
```

---

## 📡 Взаимодействие с системой LAM

Codex\_Agent может вызываться:

* напрямую из других агентов LAM (например, Archivator)
* вручную через CLI (`python -m agent.cli`)
* через HTTP-интерфейс (планируется)

---

## 🧪 Тесты и стиль

* Линтер: `ruff`
* Типизация: `mypy`
* Форматтер: `black`
* Тесты: `pytest`

Запуск:

```bash
ruff src/
mypy src/
pytest tests/
```

---

## 📄 Лицензия

MIT © [Kyrylo Liapustin](mailto:lkises01@gmail.com)

---

```

---

Если хочешь, могу сразу сгенерировать:

- `requirements.txt` с зависимостями
- `src/agent/core.py` с заготовкой для функции `handle_prompt()`
- `example.task.md` в папке `prompts/`

⚡ Просто скажи:  
> «Создай основу агента Codex» — и мы начнем формировать структуру по папкам.
```
