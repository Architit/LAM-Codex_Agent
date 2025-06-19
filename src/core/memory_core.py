import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class MemoryCore:
    def __init__(self):
        self.tasks: List[Dict[str, Any]] = []

    def add_task(self, task_info: Dict[str, Any]) -> None:
        """Добавляет новую задачу в ядро памяти."""
        task_info['added_at'] = datetime.now().isoformat()
        self.tasks.append(task_info)

    def update_task_status(self, task_id: int, new_status: str) -> bool:
        """Обновляет статус задачи."""
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id]['status'] = new_status
            self.tasks[task_id]['updated_at'] = datetime.now().isoformat()
            return True
        return False

    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Возвращает задачу по ID."""
        if 0 <= task_id < len(self.tasks):
            return self.tasks[task_id]
        return None

    def save_to_file(self, file_path: str) -> None:
        """Сохраняет все задачи в файл JSON."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def load_from_file(self, file_path: str) -> None:
        """Загружает задачи из файла JSON."""
        with open(file_path, 'r', encoding='utf-8') as f:
            self.tasks = json.load(f)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Возвращает список всех задач."""
        return self.tasks

    def remove_task(self, task_id: int) -> bool:
        """Удаляет задачу по ID."""
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]
            return True
        return False
