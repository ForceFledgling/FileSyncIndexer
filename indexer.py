import os
import shutil
import json
import time


class FileIndexer:
    def __init__(self, source_dirs, temp_dir, index_file, check_interval=5, stable_time=10):
        # Преобразуем ~ в полный путь для каждой директории
        self.source_dirs = [os.path.expanduser(dir) for dir in source_dirs]
        self.temp_dir = os.path.expanduser(temp_dir)
        self.index_file = os.path.expanduser(index_file)
        self.index = self.load_index()
        self.check_interval = check_interval  # Интервал проверки в секундах
        self.stable_time = stable_time  # Время для проверки стабильности размера файла в секундах

        # Создаем временную директорию, если она не существует
        os.makedirs(self.temp_dir, exist_ok=True)

    def load_index(self):
        """Загружает индекс из файла или создает пустой индекс, если файла нет."""
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {}

    def save_index(self):
        """Сохраняет текущий индекс в файл."""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=4)

    def copy_to_temp(self, filepath, rel_path):
        """Копирует файл в временную директорию, сохраняя структуру папок."""
        temp_path = os.path.join(self.temp_dir, rel_path)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        shutil.copy(filepath, temp_path)

    def index_files(self):
        """Основной метод для индексации и копирования новых файлов."""
        if not self.index:
            print("Индекс не найден. Создаю новый индекс, копирование файлов не производится.")
            self.create_initial_index()
            self.save_index()
            return

        self.index_and_copy_new_files()
        self.save_index()

    def create_initial_index(self):
        """Создает начальный индекс файлов без копирования."""
        for source_dir in self.source_dirs:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    rel_path = os.path.join(os.path.basename(source_dir), os.path.relpath(filepath, source_dir))

                    self.index[filepath] = {
                        'path': filepath,
                        'name': file,
                        'rel_path': rel_path,
                    }

    def index_and_copy_new_files(self):
        """Индексирует новые файлы и копирует их в temp_dir."""
        for source_dir in self.source_dirs:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    rel_path = os.path.join(os.path.basename(source_dir), os.path.relpath(filepath, source_dir))

                    if filepath in self.index:
                        continue

                    if self.is_file_still_downloading(filepath):
                        continue  # Пропускаем файл, если он все еще изменяется

                    self.copy_to_temp(filepath, rel_path)
                    self.index[filepath] = {
                        'path': filepath,
                        'name': file,
                        'rel_path': rel_path,
                    }

    def is_file_still_downloading(self, filepath):
        """Проверяет, изменяется ли размер файла (еще не завершено копирование/скачивание)."""
        try:
            initial_size = os.path.getsize(filepath)
            time.sleep(self.stable_time)
            final_size = os.path.getsize(filepath)
            return initial_size != final_size
        except OSError:
            return True  # Если файл не доступен, считаем его еще не завершенным


if __name__ == '__main__':
    source_dirs = [
        '~/Documents',
        '~/Desktop',
        '~/Downloads',
    ]
    temp_dir = '~/tmp/file_indexer/files'
    index_file = '~/tmp/file_indexer/index.json'

    while True:
        indexer = FileIndexer(source_dirs, temp_dir, index_file)
        indexer.index_files()
        
        # Запускать раз в пол минуты
        time.sleep(30)
