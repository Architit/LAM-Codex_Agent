from core.memory_core import MemoryCore  # type: ignore[import]


class Agent:
    def __init__(self):
        self.memory_core = MemoryCore()

    def process_task(self, task_info):
        """
        Обработка задачи с сохранением результата в ядро памяти.
        """
        # Реализуй логику обработки задачи
        self.memory_core.add_task(task_info)
        return "Задача обработана и сохранена."

    def get_task_status(self, task_id):
        """
        Получение статуса задачи по ID из ядра памяти.
        """
        task = self.memory_core.get_task(task_id)
        return task if task else "Задача не найдена."

    def save_agent_state(self, file_path):
        """
        Сохранение состояния памяти агента в файл.
        """
        self.memory_core.save_to_file(file_path)

    def load_agent_state(self, file_path):
        """
        Загрузка состояния памяти агента из файла.
        """
        self.memory_core.load_from_file(file_path)
