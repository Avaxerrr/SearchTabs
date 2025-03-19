import logging

def setup_logger():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('../browser_test.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
