import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] - %(name)s - %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


def main():
    logger.info('Hello from casino!')


if __name__ == '__main__':
    try:
        main()
    finally:
        logger.info('Goodbye!')
