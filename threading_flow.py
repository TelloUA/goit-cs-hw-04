import os
from threading import Lock, Thread, current_thread

def search_keywords_thread(files, keywords, results, lock):
    name = current_thread().name
    # print(f"Працює {name}")
    for file in files:
        if not os.path.exists(file):
            print(f"{name} помилка: файл {file} не існує.")
            continue

        if not os.access(file, os.R_OK):
            print(f"{name} помилка: немає доступу до файлу {file}.")
            continue
    
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    with lock:
                        results[keyword].append(file)
                        print(f"{name} знайшов {keyword} в {file}")
    # print(f"Закінчився {name}")

def main_threading(files, keywords):
    num_threads = 3
    thread_list = []
    results = {keyword: [] for keyword in keywords}
    lock = Lock()

    chunks = [files[i::num_threads] for i in range(num_threads)]

    for chunk in chunks:
        thread = Thread(target=search_keywords_thread, args=(chunk, keywords, results, lock))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    print("Результати (Threading):")
    for keyword, files in results.items():
        print(f"Ключове слово: '{keyword}'")
        if files:
            print("  Знайдено у файлах:")
            for file in files:
                print(f"    - {file}")
        else:
            print("  Не знайдено у жодному файлі.")
