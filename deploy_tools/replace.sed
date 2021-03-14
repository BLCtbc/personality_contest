sed -i "" "s/USERNAME/$USERNAME/g" nginx.$SITENAME.conf gunicorn-$SITENAME.service logrotate.$SITENAME.conf
sed -i "" "s/SITENAME/$SITENAME/g" nginx.$SITENAME.conf gunicorn-$SITENAME.service logrotate.$SITENAME.conf
sed -i "" "s/PROJECTNAME/$PROJECTNAME/g" nginx.$SITENAME.conf gunicorn-$SITENAME.service logrotate.$SITENAME.conf
# replaces all occurrences of USERNAME, SITENAME, PROJECTNAME with $USERNAME, $SITENAME, $PROJECTNAME env vars
