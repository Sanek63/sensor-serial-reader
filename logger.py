import logging


def get_logger(logger_name: str, path: str):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(logger_name)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(path)

    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
