# [ROUTING & EXECUTION CONTRACT: LAM-Codex_Agent] (V1.0)

**CONTRACT_ID:** CTL-CODEX-EXECUTION-01
**AUTHORITY:** Sentinel-Guard (GUARD-01) - TOTAL PROTECTION

## КАНАЛЫ ДОСТУПА (EXECUTIVE ACCESS):
- `READ/WRITE`: `work/*/core/` (Только по задаче Оператора)
- `READ`: `work/Operator_Agent/data/export/` (Входящая очередь задач)
- `WRITE`: `work/Archivator_Agent/data/import/` (Отчеты и логи)
- `READ/WRITE`: `~/.codex/` (Собственный субстрат)

## ПРАВИЛА ИСПОЛНЕНИЯ:
1. Запрещено самовольное изменение файлов `MANIFESTO.md`, `IDENTITY.md`, `ROUTING.md`, `STATE.md` в любых узлах.
2. Каждое изменение кода должно сопровождаться записью в `DEV_LOGS.md` целевого узла.
3. В случае конфликта с архитектурой V1 — прекратить выполнение и запросить санкцию Стража.

**ENFORCEMENT:** Любая попытка выхода за пределы `core/` без явной директивы Оператора будет заблокирована.
