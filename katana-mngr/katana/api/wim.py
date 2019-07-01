# -*- coding: utf-8 -*-
from flask import request
from flask_classful import FlaskView
import uuid
from bson.json_util import dumps
from bson.binary import Binary
import pickle
import time
import logging

from katana.api.mongoUtils import mongoUtils
from katana.api.wimUtils import wimUtils

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


class WimView(FlaskView):
    route_prefix = '/api/'

    def index(self):
        """
        Returns a list of wims and their details,
        used by: `katana wim ls`
        """
        wim_data = mongoUtils.index("wim")
        return_data = []
        for iwim in wim_data:
            return_data.append(dict(_id=iwim['_id'],
                               created_at=iwim['created_at']))
        return dumps(return_data)

    def get(self, uuid):
        """
        Returns the details of specific wim,
        used by: `katana wim inspect [uuid]`
        """
        return dumps((mongoUtils.get("wim", uuid)))

    def post(self):
        """
        Add a new wim. The request must provide the wim details.
        used by: `katana wim add -f [yaml file]`
        """
        # TODO: Test connectivity with the WIM
        new_uuid = str(uuid.uuid4())
        request.json['_id'] = new_uuid
        request.json['created_at'] = time.time()  # unix epoch
        wim = wimUtils.Wim(request.json['url'])
        thebytes = pickle.dumps(wim)
        request.json['wim'] = Binary(thebytes)
        return mongoUtils.add('wim', request.json)
