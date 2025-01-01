import os
from multiprocessing import Queue, Process, current_process

def search_keywords_process(files, keywords, queue):
    name = current_process().name
    # print(f"Працює {name}")
    local_results = {keyword: [] for keyword in keywords}
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
                    local_results[keyword].append(file)
                    print(f"{name} found {keyword} in {file}")
    queue.put(local_results)
    # print(f"Закінчився {name}")

def main_multiprocessing(files, keywords):
    num_processes = 3
    process_list = []
    queue = Queue()
    results = {keyword: [] for keyword in keywords}

    chunks = [files[i::num_processes] for i in range(num_processes)]

    for chunk in chunks:
        process = Process(target=search_keywords_process, args=(chunk, keywords, queue))
        process_list.append(process)
        process.start()

    for process in process_list:
        process.join()

    while not queue.empty():
        local_results = queue.get()
        for keyword, files in local_results.items():
            results[keyword].extend(files)

    print("Результати (Multiprocessing):")
    for keyword, files in results.items():
        print(f"Ключове слово: '{keyword}'")
        if files:
            print("  Знайдено у файлах:")
            for file in files:
                print(f"    - {file}")
        else:
            print("  Не знайдено у жодному файлі.")