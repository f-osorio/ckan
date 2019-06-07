import sys
import json
import subprocess
import ConfigParser


def get_docker_ip():
    results = subprocess.check_output(['ifconfig'])
    for item in results.split('\n\n'):
        pos = item.find(':')
        name = item[:pos]

        pos = item.find('inet')
        address = item[pos+5:pos+15]
        if 'docker' in name:
            return address

    return False


if len(sys.argv) != 2:
    email = raw_input('Provide an email address to send emails to/from: ')
else:
    email = sys.argv[1]

#TODO update to use new 'named volume'
ckan_config = '/var/lib/docker/volumes/docker_ckan_config/_data/production.ini'

config = ConfigParser.ConfigParser()
config.read(ckan_config)

# add plugins to config
plugins = config.get('app:main', 'ckan.plugins')
plugins += ' edawax dara journal-dashboard pdf_view resource_proxy'
config.set('app:main', 'ckan.plugins', plugins)

# update preview capabilities
default_views = config.get('app:main', 'ckan.views.default_views')
default_views += ' pdf_view resource_proxy'
config.set('app:main', 'ckan.views.default_views', default_views)


# add text format previews
text_previews = 'text plain text/plain txt do application/x-stata-d TXT LOG log SPS sps dta'
config.set('app:main', 'ckan.preview.text_formats', text_previews)

# doi settings
config.set('app:main', 'ckanext.dara.doi_prefix', '10.23456')
config.set('app:main', 'ckanext.dara.use_testserver', 'true')
config.set('app:main', 'ckanext.dara.demo.user', '')
config.set('app:main', 'ckanext.dara.demo.password', '')
config.set('app:main', 'ckanext.dara.user', '')
config.set('app:main', 'ckanext.dara.password', '')


# storage path
config.set('app:main', 'ckan.storage_path', '/var/lib/ckan/default')


# set email config options -- these assume the smtp servcer is the host machine
config.set('app:main', 'email_to', email)
config.set('app:main', 'error_email_from', email)
config.set('app:main', 'smtp.server', get_docker_ip())
config.set('app:main', 'smtp.starttls', 'false')
config.set('app:main', 'smtp.mail_form', email)

# start stat tracking
config.set('app:main', 'ckan.tracking_enabled', 'true')


# solr_url - Not needed
#config.set('app:main', 'solr_url', 'http://127.0.0.1:8983/solr/ckan')

# wordpresser_proxt
config.set('app:main', 'wordpresser.proxy_host', 'https://www.edawax.de')

with open(ckan_config, 'wb') as configfile:
    config.write(configfile)
