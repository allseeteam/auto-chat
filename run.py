import threading
import argparse
import time

from auto_chat.auto_chat import AutoChat


def loop(autochat_instance: AutoChat, exit_flag_instance: threading.Event) -> None:
    # infinite loop with check_time_and_send every 60 seconds
    while not exit_flag_instance.is_set():
        try:
            autochat_instance.check_time_and_send()
        except Exception as e:
            print(f"Error while executing check_time_and_send: {e}")
        time.sleep(60)


def wait_for_exit(exit_flag_instance: threading.Event):
    # waiting for user input to stop the program
    input("Press Enter to stop the program...")
    exit_flag_instance.set()
    print("Exiting...")


if __name__ == "__main__":
    # parsing arguments
    parser = argparse.ArgumentParser(description='AutoChat Configuration')
    parser.add_argument('--telegram-config', type=str, help='Path to Telegram config file')
    parser.add_argument('--auto-chat-config', type=str, help='Path to AutoChat config file')
    parser.add_argument('--yandex-cloud-config', type=str, help='Path to Yandex Cloud config file')
    parser.add_argument('--yandex-gpt-key', type=str, help='Path to Yandex GPT key file')
    args = parser.parse_args()
    # initializing auto chat
    autochat = AutoChat(
        telegram_config_file_path=args.telegram_config,
        auto_chat_config_file_path=args.auto_chat_config,
        yandex_cloud_config_file_path=args.yandex_cloud_config,
        yandex_gpt_key_file_path=args.yandex_gpt_key
    )
    # initializing exit flag
    exit_flag = threading.Event()
    # starting loop
    autochat_thread = threading.Thread(
        target=loop,
        args=(autochat, exit_flag)
    )
    autochat_thread.start()
    # starting waiting for user input thread
    wait_thread = threading.Thread(
        target=wait_for_exit,
        args=[exit_flag]
    )
    wait_thread.start()
    # if exit flag is set than stopping the program
    wait_thread.join()
    autochat.stop()
    autochat_thread.join()
