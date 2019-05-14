import sys
import json
import subprocess
import ConfigParser


def get_container_ip():
    try:
        container = json.loads(subprocess.check_output(['docker', 'inspect', 'ckan']))
        network_settings = container[0]['NetworkSettings']
        networks = network_settings['Networks']
        ip = networks['docker_default']['IPAddress']
        gateway = networks['docker_default']['Gateway']
        return (ip, gateway)
    except Exception as e:
        Print('Check that the CKAN container is running: `docker ps`')

if len(sys.argv) != 2:
    email = raw_input('Provide an email address to send emails to/from: ')
else:
    email = sys.argv[1]


ckan_config = '/var/lib/docker/volumes/docker_ckan_config/_data/production.ini'

config = ConfigParser.ConfigParser()
config.read(ckan_config)

# add plugins to config
plugins = config.get('app:main', 'ckan.plugins')
plugins += ' edawax dara journal-dashboard'
config.set('app:main', 'ckan.plugins', plugins)


# set email config options -- these assume the smtp servcer is the host machine
config.set('app:main', 'email_to', email)
config.set('app:main', 'error_email_from', email)
config.set('app:main', 'smtp_server', get_container_ip()[1])
config.set('app:main', 'smtp.starttls', 'false')
config.set('app:main', 'smtp.mail_form', email)


with open(ckan_config, 'wb') as configfile:
    config.write(configfile)




