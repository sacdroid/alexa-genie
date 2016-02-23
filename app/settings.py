import os

AMAZON_APPLICATION_ID = 'amzn1.echo-sdk-ams.app.b62be354-7536-4752-a76e-5ce7e369cd05'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE_FILE = os.path.join(BASE_DIR, 'sarapoints.db')

CERTIFICATE_PATH='/home/pi/echo/certs/certificate.pem'
PRIVATE_KEY_PATH='/home/pi/echo/certs/private-key.pem'

SKILL_INVOCATION_NAME = 'Genie'
SKILL_NAME = 'Genie, what do you wish today'
SKILL_VERSION = '0.1'

POINT_HOLDER_NAME = 'Sara'

KODI_HOST='192.168.2.67'
KODI_PORT=8080
KODI_USER=''
KODI_PASSWORD=''



