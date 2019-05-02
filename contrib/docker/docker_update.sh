# Update .ini to include plugins
docker exec -it ckan sed -i '/^\[app:main\]$/,/^\[/ s/^ckan.plugins = stats text_view image_view recline_view/ckan.plugins = stats text_view image_view recline_view edawax dara/' /etc/ckan/production.ini

# create test data
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan create-test-data -c /etc/ckan/production.ini

# Create admin account
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan sysadmin -c /etc/ckan/production.ini add ckan
