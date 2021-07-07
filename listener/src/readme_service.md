cp file_listener_service /etc/init.d/file_listener_service
chmod +x /etc/init.d/file_listener_service
update-rc.d file_listener_service defaults
service file_listener_service start