import threading
import argparse
import signal
import time

from auto_chat.auto_chat import AutoChat


def auto_chat_check_loop(autochat_instance: AutoChat, exit_flag_instance: threading.Event) -> None:
    # infinite loop with check_time_and_send every 60 seconds
    while not exit_flag_instance.is_set():
        try:
            autochat_instance.check_time_and_send()
        except Exception as e:
            print(f"Error while executing check_time_and_send: {e}")
        time.sleep(60)


def stop_program(
        exit_flag_instance: threading.Event,
        autochat_instance: AutoChat,
        autochat_thread_instance: threading.Thread
) -> None:
    print('\n' + 'Stopping the program...')
    exit_flag_instance.set()
    autochat_instance.stop()
    autochat_thread_instance.join()
    print('Program stopped.')


if __name__ == "__main__":
    print('Starting the program...')
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
    # starting auto chat loop
    autochat_thread = threading.Thread(
        target=auto_chat_check_loop,
        args=(autochat, exit_flag)
    )
    autochat_thread.start()
    print('Program is running...' + '\n' + 'Use Ctrl+C or just exit to stop the program')
    # setting stop signals
    signal.signal(signal.SIGINT, lambda sig, frame: stop_program(exit_flag, autochat, autochat_thread))
    signal.signal(signal.SIGTERM, lambda sig, frame: stop_program(exit_flag, autochat, autochat_thread))
