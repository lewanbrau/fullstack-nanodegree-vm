P2 Tournament Results README
============================

Requirements
------------
1. Install Vagrant and VirtualBox
2. Clone the fullstack-nanodegree-vm repository
3. Launch the Vagrant VM

Instructions to run this app
----------------------------
1. Download all files from the github repo. Save them iside a vagrant shared folder setup from the requirements step.
2. SSH into Vagrant
	1. Within the Vagrant directory type 'vagrant up'
	2. type 'vagrant ssh'
	3. cd into your shared project folder e.g. 'cd /vagrant/tournament'
3. Create the databases
	1. open the psql terminal. Type 'psql'
	2. run the tournament.sql file by typing '\i tournament.sql'
	3. leave the psql terminal using control+d
4. Run the tests. Type 'python tournament_tests.py'