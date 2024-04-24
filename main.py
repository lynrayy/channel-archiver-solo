import config, auth
import os
from app import app


def warnings():
    critical = False

    def warn_channel_none(name, is_critical = False):
        print(f"Внимание! Вы не указали ID канала-{name}.{' Без этого канала бот не сможет работать' if is_critical else ''}")

    def warn_id_not_100(name):
        print(f"Внимание! ID канала-{name} указано как чат, а не канал. ID канала ВСЕГДА начинается с -100!\n   "
              f"Бот продолжит работу, но вероятность возникновения ошибок возрастает в разы.")

    if auth.api_id == 12345678 or auth.api_id == 0 or auth.api_id is None:
        print("Внимание! Вы не настроили api_id в файле auth.py")
        critical = True
    if auth.api_hash == "a1b2c3d4e5f6g7h8i9" or auth.api_hash == "" or auth.api_hash is None:
        print("Внимание! Вы не настроили api_hash в файле auth.py")
        critical = True
    if auth.phone_number == "+79994441122" or auth.phone_number == "" or auth.phone_number is None:
        print("Внимание! Вы не настроили phone_number в файле auth.py")
        critical = True

    if config.source_channel_id == -10011111111 or config.source_channel_id is None:
        warn_channel_none("источника", True)
        critical = True
    if config.archive_channel_id == -10022222222 or config.archive_channel_id is None:
        warn_channel_none("архива", True)
        critical = True
    if config.deleted_channel_id == -10033333333 or config.deleted_channel_id is None:
        warn_channel_none("удалёнок")

    if not str(config.source_channel_id).startswith("-100"):
        warn_id_not_100('источника')
    if not str(config.archive_channel_id).startswith("-100"):
        warn_id_not_100('архива')
    if not str(config.deleted_channel_id).startswith("-100"):
        warn_id_not_100('удалёнок')
    if critical:
        print("\n==================\nОБРАТИТЕ ВНИМАНИЕ!\n==================\n"
              "При запуске возникла одна или несколько серьёзных проблем с вашими настройками. Бот не сможет работать при таких настройках.\n"
              "Процесс завершается...\n")
        os._exit(-1)

    print(f"\nПосты будут сохраняться в архив как {'собственные посты' if config.store_as_archive else 'репосты из источника'}\n\n--------------Бот запущен--------------")


def main():
    while True:
        try:
            app.run()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    warnings()
    main()
