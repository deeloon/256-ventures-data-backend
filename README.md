# 256-ventures-data-backend
This module collects data from various sources, passes them through models and plots them using Plotly. 
Plots are then hosted onto a Dash webapp hosted via AWS Elastic Beanstalk

Files with prefix 'collect_' are for scheduled data collection

## To view plot of models:
http://256-ventures-dev.us-east-2.elasticbeanstalk.com

## To view Jupyter notebook files:
### Data Pulling
https://nbviewer.jupyter.org/github/deeloon/256-ventures-data-backend/blob/master/data_pulling.ipynb

### s2f model
https://nbviewer.jupyter.org/github/deeloon/256-ventures-data-backend/blob/master/s2f_model.ipynb

### scrape_coinfarm
https://nbviewer.jupyter.org/github/deeloon/256-ventures-data-backend/blob/master/scrape_blockchair.ipynb


## Connect to virtual computer for the first time (on administrator account):
1. Log in to AWS account and go to EC2 instance page. https://us-east-2.console.aws.amazon.com/ec2/home?region=us-east-2#Instances:sort=instanceId (For Autoview: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:sort=instanceId)
2. If you are trying to log in to the virtual computer from a new network, first add your IP address to security group.
3. On the left sidebar, scroll to Network&Security -> Security Groups and click on it.
4. On the dashboard, check the row with *Group Name* "launch-wizrd-1".
5. In the bottom section, go to the tab "Inbound" and click "Edit".
6. Click "Add Rule". A new row appears. Select *Type* "TCP" and *Source* "My IP" and Save.
7. Go back to the "Instances" page from left sidebar.
8. Tick the row with an empty "Name" field. Click "Connect".
9. Download remote desktop file. You will need an application to open this if your PC does not have one.
10. To get login password of the virtual computer, click "Get Password". 
11. Browse and upload 256_ventures_key_pair.pem file and click "Decrypt" to get the login password. 
12. Open the remote desktop file and log in. Check box for saving your credentials if you want to remember the password. 

## Deploying new code onto webapp
1. Log in to virtual computer. Edit the code in the "256_ventures" folder.
2. Open Windows Powershell (search the name in windows search bar), change directory to project folder
3. Type command "eb deploy" and run.
3. Wait 5 to 10 mins for the webapp to be deployed fully and then check for errors.

## Debugging deployment errors
1. Go to https://us-east-2.console.aws.amazon.com/elasticbeanstalk/home?region=us-east-2#/applications
2. Click into 256-ventures-dev. The color will be red if there are errors and green if the webapp is working.
3. If red, go to the left sidebar and click "Logs".
4. Click "Request Logs" on top right and "Last 100 lines".
5. Download logs and inspect the error.
6. To roll back to a previous working version, go to "Dashboard" on left sidebar and click "Upload and Deploy" in the middle of the page.
7. Follow instructions to deploy a previous working version.

## Notes:
1. Filepaths specified in the Github are relative to current directory, but should be changed to explicit directory in development.
2. Eg. "data/Bitmex..." should be "C:/.../256_ventures/data/Bitmex/..."
