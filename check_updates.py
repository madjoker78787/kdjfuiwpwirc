import subprocess
import os
import sys

def check_git_updates():
    repo_path = os.getcwd()
    try:
        subprocess.run(['git', '-C', repo_path, 'fetch'], check=True)

        current_branch = subprocess.check_output(
            ['git', '-C', repo_path, 'rev-parse', '--abbrev-ref', 'HEAD'],
            text=True
        ).strip()

        local_commit = subprocess.check_output(
            ['git', '-C', repo_path, 'rev-parse', current_branch],
            text=True
        ).strip()

        remote_commit = subprocess.check_output(
            ['git', '-C', repo_path, 'rev-parse', f'origin/{current_branch}'],
            text=True
        ).strip()

        # Сравниваем локальный и удаленный коммиты
        if local_commit != remote_commit:
            print(f"Обновления доступны для ветки '{current_branch}':")
            print(f"Локальный коммит: {local_commit}")
            print(f"Удаленный коммит: {remote_commit}")

            # Запросите у пользователя, нужно ли обновить код
            update = input("Хотите обновить код? (y/n): ").strip().lower()
            if update == 'y':
                subprocess.run(['git', '-C', repo_path, 'pull'], check=True)
                print("Код успешно обновлён.")
            else:
                print("Обновление кода отменено.")
        else:
            print(f"Ваша ветка '{current_branch}' актуальна.")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    check_git_updates()
    subprocess.run([sys.executable, 'main.py'])
