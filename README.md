# TP_Categorization_Hackathon

Система сортировки входящих писем для IT-поддержки: читает файлы из `inbox`, классифицирует по правилам, перекладывает в папки и пишет лог со статистикой.

## Категории

| Папка | Назначение |
|-------|------------|
| `incidents` | срочные поломки, URGENT |
| `monitoring` | алерты, grafana, jira |
| `access` | доступы, VPN, пароли |
| `software` | установка и обновление ПО |
| `general` | обычные обращения |
| `spam` | спам и фишинг |
| `unclassified` | не подошло ни одно правило |
| `failed` | файл не прочитали |

Если письмо не подходит ни под одну категорию — попадает в `unclassified`.  
Битые, пустые и бинарные файлы — в `failed`.

## Структура

```
main.py              — запуск
run.sh               — bash-скрипт
src/mail_system/     — код приложения
tests/               — pytest на своих фикстурах
data/inbox/inbox/    — исходные письма
mailbox/             — результат работы (логи, не в git)
```

## Установка

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```powershell
python main.py
```

или через bash (Git Bash / WSL):

```bash
bash run.sh
```

Параметры:

```powershell
python main.py --mailbox mailbox --source data/inbox/inbox --force
```

- `--force` — очистить inbox и скопировать письма заново из source

## Результат

После запуска смотри:

- `mailbox/processing.log` — что куда попало и почему
- `mailbox/stats.txt` — сколько писем в каждой категории
- папки `mailbox/incidents/`, `mailbox/spam/` и т.д.

## Тесты

```powershell
pytest
```

Тесты используют файлы из `tests/fixtures/`, не из `data/inbox/`.

## Команда

Проект для хакатона «Технологии программирования», НИУ ВШЭ.
