import datetime


def log_debug(type: str, message: str) -> None:
    print(
        f"{type} event | {message} | {datetime.datetime.now().isoformat(timespec='milliseconds')}"
    )
