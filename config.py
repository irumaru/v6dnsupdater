import yaml

with open('config.yaml') as file:
    config = yaml.safe_load(file)

CLOUDFLARE_GLOBAL_API_KEY = config['cloudflare']['appKey']
CLOUDFLARE_EMAIL = config['cloudflare']['email']

CLOUDFLARE_ZONE_ID = config['cloudflare']['record']['zoneId']
CLOUDFLARE_RECORD_ID = config['cloudflare']['record']['recordId']
CLOUDFLARE_RECORD_NAME = config['cloudflare']['record']['name']

LOOP_INTERVAL = config['loopInterval']
INTERFACE = config['interface']
ONLINE_CHECK_ADDRESS = config['onlineCheckAddress']
LOG_PATH = config['logPath']