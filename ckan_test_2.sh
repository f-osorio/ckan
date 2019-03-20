
LOC="/etc/ckan/default/development.ini"

echo "---Start---"
sed -i 's/host\/ckan_default/host\/ckan_test/' $LOC

echo "Creating system admin"
/home/ckan/Python/bin/paster user add admin password=ckan email=f.osorio@zbw.eu -c $LOC
/home/ckan/Python/bin/paster sysadmin add admin -c $LOC

echo "Changing config"
/home/ckan/Python/bin/paster serve $LOC &
echo "Server is running"

echo -e "\n\nRunning Tests"
#python /home/ckan/Python/src/ckanext-func-test/ckanext/func_test/tests/selenium/base.py
python /home/ckan/Python/src/ckanext-func-test/ckanext/func_test/tests/selenium/login.py
python /home/ckan/Python/src/ckanext-func-test/ckanext/func_test/tests/selenium/admin_workflows_1.py
python /home/ckan/Python/src/ckanext-func-test/ckanext/func_test/tests/selenium/author_workflows.py
python /home/ckan/Python/src/ckanext-func-test/ckanext/func_test/tests/selenium/admin_workflows_2.py
echo -e "Tests Finished\n\n"

sleep 3
PID=$!
kill $PID

echo "Reset test database"
/home/ckan/Python/bin/paster db clean -c $LOC  #clean database
/home/ckan/Python/bin/paster db init -c $LOC   #re-initialize

echo "Resetting config"
sed -i 's/host\/ckan_test/host\/ckan_default/' $LOC

