import json
import os

def get_credential(name):
    cred_file = os.environ.get('PY_AGENT_CREDENTIALS_FILE', 'credentials.json')
    cred_file = os.path.join(os.path.dirname(__file__), cred_file)

    with open(cred_file, 'r') as f:
        creds = json.load(f)
        return creds.get(name, None)
