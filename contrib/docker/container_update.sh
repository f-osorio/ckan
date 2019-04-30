# create admin account for new instance
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan sysadmin -c /etc/ckan/production.ini add ckan

# update .ini file to include plugins
docker exec -it ckan sed -i '/^\[app:main\]$/,/^\[/ s/^ckan.plugins = stats text_view image_view recline_view/ckan.plugins = stats text_view image_view recline_view edawax dara/' /etc/ckan/production.ini
