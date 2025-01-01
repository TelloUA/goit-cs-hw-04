import time
from pathlib import Path
from multiprocessing_flow import main_multiprocessing
from threading_flow import main_threading

def main():
    files = list(Path("texts").glob("*.txt"))
    if not files:
        print("Помилка: Текстові файли не знайдені у директорії 'texts'.")
        return 

    keywords = ["day", "fish", "night"]

    start_time = time.time()
    main_threading(files, keywords)
    threading_duration = time.time() - start_time
    print(f"Час виконання для багатопотокового підходу: {threading_duration:.4f} секунд.")

    start_time = time.time()
    main_multiprocessing(files, keywords)
    multiprocessing_duration = time.time() - start_time
    print(f"Час виконання для багатопроцесорного підходу: {multiprocessing_duration:.4f} секунд.")

if __name__ == "__main__":
    main()
