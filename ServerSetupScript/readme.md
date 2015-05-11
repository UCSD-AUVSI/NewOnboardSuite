## To make the OBC python server always run at bootup:

sudo cp OBCautostart.sh /etc/init.d

sudo chmod +x /etc/init.d/OBCautostart.sh

sudo update-rc.d OBCautostart.sh defaults

sudo /etc/init.d/OBCautostart.sh start

## Additional Notes
Server log files (e.g. stderr and console output) will be saved in the `ServerLogs` file.