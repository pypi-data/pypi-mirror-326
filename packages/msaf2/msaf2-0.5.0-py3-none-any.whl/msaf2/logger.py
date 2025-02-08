import logging
def configure_logger(level, warn_file, no_warn_details):
    logger = logging.getLogger('msafLogger')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s | %(pathname)s:%(funcName)s:%(lineno)s -  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)

    configure_threader_logger(level)
    
    configure_detailed_warning_logger(warn_file, no_warn_details)

    return logger

def configure_threader_logger(level):
    logger = logging.getLogger('msafThread')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s [Th:%(threadName)s] | %(pathname)s:%(funcName)s:%(lineno)s -  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)

def configure_detailed_warning_logger(warn_file, no_warn_details):
    logger = logging.getLogger('msafWarnings')   
    logger.setLevel(logging.DEBUG if not no_warn_details else logging.CRITICAL)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(warn_file, 'w')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)