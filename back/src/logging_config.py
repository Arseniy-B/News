import logging
import logging.config
from pathlib import Path  # Опционально, для путей к файлам

# Словарь конфигурации (dictConfig)
LOGGING_CONFIG = {
    'version': 1,  # Версия формата конфигурации (всегда 1 для dictConfig)

    'disable_existing_loggers': False,  # Не отключать существующие логгеры (чтобы не сломать библиотеки)

    'formatters': {  # Форматтеры: определяют, как выглядят записи в логах
        'default': {  # Имя форматтера
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Шаблон: время, имя логгера, уровень, сообщение
            'datefmt': '%Y-%m-%d %H:%M:%S',  # Формат даты/времени
            'class': 'logging.Formatter',  # Класс форматтера (по умолчанию)
        },
        'detailed': {  # Дополнительный форматтер для детальных логов
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',  # + номер строки
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'class': 'logging.Formatter',
        },
    },

    'handlers': {  # Хендлеры: определяют, куда выводить логи (консоль, файл и т.д.)
        'console': {  # Хендлер для консоли
            'class': 'logging.StreamHandler',  # Класс: вывод в stdout/stderr
            'level': 'INFO',  # Минимальный уровень для этого хендлера
            'formatter': 'default',  # Какой форматтер использовать
            'stream': 'ext://sys.stdout',  # Поток: стандартный вывод (опционально)
        },
        'file': {  # Хендлер для файла
            'class': 'logging.FileHandler',  # Класс: запись в файл
            'filename': str(Path('logs/app.log')),  # Путь к файлу (используем Path для кросс-платформенности)
            'mode': 'a',  # Режим: 'a' — append (добавлять, не перезаписывать)
            'level': 'DEBUG',  # Более детальный уровень для файла
            'formatter': 'detailed',  # Детальный форматтер
        },
        'error_file': {  # Отдельный хендлер только для ошибок
            'class': 'logging.FileHandler',
            'filename': str(Path('logs/errors.log')),
            'mode': 'a',
            'level': 'ERROR',  # Только ERROR и выше
            'formatter': 'default',
        },
    },

    'root': {  # Корневой логгер: базовая настройка для всех логгеров
        'level': 'INFO',  # Глобальный минимальный уровень
        'handlers': ['console', 'file'],  # Хендлеры для root (все логгеры по умолчанию)
    },

    'loggers': {  # Конкретные логгеры для модулей/приложений
        'my_app': {  # Логгер для твоего приложения (имя соответствует __name__ в модулях)
            'level': 'DEBUG',  # Уровень для этого логгера (переопределяет root)
            'handlers': ['console', 'error_file'],  # Свои хендлеры (не propagate к root)
            'propagate': False,  # Не передавать логи родительскому логгеру (root)
        },
        'my_app.domain': {  # Подлоггер для подмодуля (иерархия: my_app > domain)
            'level': 'INFO',
            'propagate': True,  # Передавать в родительский (my_app)
        },
    },

    # Опционально: фильтры (не используются здесь, но можно добавить)
    # 'filters': {
    #     'require_debug': {'()': 'logging.Filter', 'name': 'DEBUG'},
    # },
}

def setup_logging():
    Path('logs').mkdir(exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG)
    
    logger = logging.getLogger(__name__)
    logger.info("Логирование настроено!")
