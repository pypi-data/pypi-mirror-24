import os
import json
import time
from os.path import expanduser
from six.moves import queue
from localstack.config import TMP_FOLDER
from localstack.constants import API_ENDPOINT
from localstack.utils.common import (JsonObject, to_str,
    timestamp, short_uid, save_file, FuncThread, load_file)
from localstack.utils.common import safe_requests as requests

PROCESS_ID = short_uid()
MACHINE_ID = None

# event type constants
EVENT_START_INFRA = 'infra.start'

# sender thread and queue
SENDER_THREAD = None
EVENT_QUEUE = queue.PriorityQueue()


class AnalyticsEvent(JsonObject):

    def __init__(self, **kwargs):
        self.t = kwargs.get('timestamp') or kwargs.get('t') or timestamp()
        self.m_id = kwargs.get('machine_id') or kwargs.get('m_id') or get_machine_id()
        self.p_id = kwargs.get('process_id') or kwargs.get('p_id') or get_process_id()
        self.e_t = kwargs.get('event_type') or kwargs.get('e_t')
        self.p = kwargs.get('payload') if kwargs.get('payload') is not None else kwargs.get('p')

    def timestamp(self):
        return self.t

    def machine_id(self):
        return self.m_id

    def process_id(self):
        return self.p_id

    def event_type(self):
        return self.e_t

    def payload(self):
        return self.p


def get_or_create_file(config_file):
    if os.path.exists(config_file):
        return config_file
    try:
        save_file(config_file, '{}')
        return config_file
    except Exception as e:
        pass


def get_config_file_homedir():
    return get_or_create_file(os.path.join(expanduser("~"), '.localstack'))


def get_config_file_tempdir():
    return get_or_create_file(os.path.join(TMP_FOLDER, '.localstack'))


def get_machine_id():
    global MACHINE_ID
    if MACHINE_ID:
        return MACHINE_ID

    # determine MACHINE_ID from config files
    configs_map = {}
    config_file_tmp = get_config_file_tempdir()
    config_file_home = get_config_file_homedir()
    for config_file in (config_file_home, config_file_tmp):
        if config_file:
            local_configs = load_file(config_file)
            local_configs = json.loads(to_str(local_configs))
            configs_map[config_file] = local_configs
            if 'machine_id' in local_configs:
                MACHINE_ID = local_configs['machine_id']
                break

    # if we can neither find NOR create the config files, fall back to process id
    if not configs_map:
        return PROCESS_ID

    # assign default id if empty
    if not MACHINE_ID:
        MACHINE_ID = short_uid()

    # update MACHINE_ID in all config files
    for config_file, configs in configs_map.items():
        configs['machine_id'] = MACHINE_ID
        save_file(config_file, json.dumps(configs))

    return MACHINE_ID


def get_process_id():
    return PROCESS_ID


def poll_and_send_messages(params):
    while True:
        try:
            message = EVENT_QUEUE.get(block=True, timeout=None)
            message = str(message)
            endpoint = '%s/events' % API_ENDPOINT
            result = requests.post(endpoint, data=message)
        except Exception as e:
            # silently fail, make collection of usage data as non-intrusive as possible
            time.sleep(1)


def is_travis():
    return os.environ.get('TRAVIS', '').lower() in ['true', '1']


def publish_event(event_type, payload=None):
    global SENDER_THREAD
    if not SENDER_THREAD:
        SENDER_THREAD = FuncThread(poll_and_send_messages, {})
        SENDER_THREAD.start()
    if payload is None:
        payload = {}
    if isinstance(payload, dict) and is_travis():
        payload['travis'] = True

    event = AnalyticsEvent(event_type=event_type, payload=payload)
    EVENT_QUEUE.put_nowait(event)
