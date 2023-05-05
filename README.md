# Partial-Partitioning-Testing
Code for the automated partial partition testing project
For running the tool:

First, all these folders- node0, network_nodes, and apps directories-  should be copied into the master node - A third party node used to run our tool.

Then on the master node, cd into node0 and run bash setup_node0.sh to complete all the installations, sudo scp chrony.conf node0:/etc/chrony to change the chrony configurations and sudo systemctl restart chronyd.service to restart chrony after changing its configuration.>>>> with these three commands the master node will be ready.

Now to set up the remaining nodes in the network that the tested application is going to use them, we run python3 setting_ip_nodes.py inside node0 directory.
By this, the tool is now ready to be used.

The user should have all the installations requied for running thier application ready and installed.

If the user would like to test any of the applications already tested all they need is copying the user_config.py in the application's directory into node0 directory in the master node after making some changes to suit their network, run python3 cpature_connections.py and then we run python3 inject_partitions.py, after running the tool the generated logs and the tests_logs and results will show up in the tested application directory.

If the user would like to test new application, they should create a new directory for their application and make changes to user_config.py and follow the previous steps.  



