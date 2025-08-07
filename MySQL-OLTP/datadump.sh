#!/bin/sh
# The above line tells the interpreter this code needs to be run as a shell script.

# This will be printed on to the screen. In the case of cron job, it will be printed to the logs.
echo "Data dumping on progress..."
# Create a backup
if mysqldump -u root -pRRNY2dy4ufRcsxfCnqsurRCG sales sales_data > sales_data.sql ; then
 echo 'sales_data.sql created'
else
 echo 'Error! sales_data.sql was not created.'
 exit
fi