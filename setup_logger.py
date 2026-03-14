import logging, os, dotenv, requests

# Instalacja:
# pip install python-dotenv requests
# git submodule add https://github.com/cdcobra/logger_server logger_server
# git submodule update --init --recursive

# Dodaj do .env:
# LOGGER_HOST=localhost
# LOGGER_PORT=8000
# LOGGER_LEVEL=DEBUG
# APP_NAME=your_app_name

# Przykład użycia:
# from logger_server.setup_logger import setup_logging
# logger = setup_logging("app.main")
# logger.info("This is an info message")

class WebhookHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        dotenv.load_dotenv()
        super().__init__(level)
        self.webhook_url = f"http://{os.getenv('LOGGER_HOST')}:{os.getenv('LOGGER_PORT')}/log"
        self.application = os.getenv("APP_NAME")

    def emit(self, record):
        try:
            print(record.levelname, record.name, record.funcName, ':', record.lineno, '-', record.getMessage())  # Print the log message to console
            requests.post(self.webhook_url, json={"application": self.application, "level": record.levelname, "name": record.name, "funcName": record.funcName, "lineno": record.lineno, "message": record.getMessage()})
        except Exception as e:
            print(f"[Logger Error] Failed to send log to webhook: {e}")

def setup_logging() -> logging.Logger:
    dotenv.load_dotenv()
    app_logger = logging.getLogger("app")
    app_logger.setLevel(getattr(logging, os.getenv("LOGGER_LEVEL", "INFO").upper()))

    # ważne: żeby nie dodawać drugi raz przy ponownym setupie
    if not any(isinstance(h, WebhookHandler) for h in app_logger.handlers):
        app_logger.addHandler(WebhookHandler())

    # jeśli nie chcesz, żeby logi szły też do root/console:
    app_logger.propagate = False

    return app_logger