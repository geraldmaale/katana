import requests
import json
import logging

# Logging Parameters
logger = logging.getLogger(__name__)
file_handler = logging.handlers.RotatingFileHandler(
    'katana.log', maxBytes=10000, backupCount=5)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
stream_formatter = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class Ems():
    """
    Class implementing the communication API with EMS
    """

    def __init__(self, url):
        """
        Initialize an object of the class
        """
        self.url = url

    def conf_radio(self, emsd):
        """
        Configure radio components for the newly created slice
        """
        ems_url = self.url
        api_prefix = '/deploy'
        url = ems_url + api_prefix
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = emsd
        r = None
        try:
            r = requests.post(url, json=json.loads(json.dumps(data)), timeout=10,
                              headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.exception("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            logger.exception("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            logger.exception("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            logger.exception("Error:", err)
