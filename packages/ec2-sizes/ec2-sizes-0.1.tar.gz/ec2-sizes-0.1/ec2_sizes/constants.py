"""Constants"""
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INSTANCE_TYPE_FILE = os.path.join(BASE_DIR, 'ec2-sizes.json')
INSTANCE_TYPE_FILE = os.environ.get('INSTANCE_TYPE_FILE',
                                    DEFAULT_INSTANCE_TYPE_FILE)
INSTANCE_TYPES = json.load(open(INSTANCE_TYPE_FILE))
