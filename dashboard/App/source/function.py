import logging

def setup_logger(log_file, log_level_file, log_level_console):
    # Create a logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)  # Set the global log level
    
    # Create a file handler with log level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level_file)
    
    # Create a console handler with log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level_console)
    
    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger