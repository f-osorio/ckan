# create test data
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan create-test-data -c /etc/ckan/production.ini

# Create admin account
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan sysadmin -c /etc/ckan/production.ini add ckan
