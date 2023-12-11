#!/usr/bin/python3.10
#Note: if the folders aren't accessable, you will need to restart the client machine, or restart the client workstation with these commands:
# net stop workstation /y
# net start workstation

import subprocess
import time as t



def installation():
	subprocess.run("apt install samba", shell=True)
	t.sleep(3)
	subprocess.run("ufw allow samba", shell=True)
	subprocess.run("ufw allow 21", shell=True)
	subprocess.run("ufw allow 445", shell=True)
	subprocess.run("ufw allow 137", shell=True)
	subprocess.run("ufw allow 138", shell=True)
	subprocess.run("ufw allow 139", shell=True)
	t.sleep(2)

def user_creation(newuser):
	subprocess.run(f"useradd {newuser}", shell=True)
	subprocess.run(f"passwd {newuser}", shell=True)
	group_name = input("Enter group name for new user: ")
	subprocess.run(f"groupadd {group_name}", shell=True)
	subprocess.run(f"usermod --append --groups {group_name} {newuser}", shell=True)
	t.sleep(2)

def folder_creation(newuser):
	samba_password = subprocess.run(f"smbpasswd -a {newuser}\n", shell=True)
	folder_amount = int(input("Enter how many NEW folders do you want to create and share: "))
	start_amount = 1
	dir_location = input("Enter Where will the new folders be created (Example: /home/elliot ): ")

	folder_list = []
	while start_amount <= folder_amount:
		folder_name = input(f"Name of folder {start_amount}: ")
		folder_list.append(folder_name)
		start_amount += 1
	for folder in folder_list:
		subprocess.run(f"mkdir {dir_location}/{folder}", shell=True)
		subprocess.run(f"chmod 777 {dir_location}", shell=True)
		choice = input(f"Will {folder} require a password for access? type yes if so, otherwise press enter: ")
		if choice == "yes":
			subprocess.run(f"chown -R {newuser}:{newuser} {dir_location}/{folder}", shell=True)
			subprocess.run(f"chmod -R  770 {dir_location}/{folder}", shell=True)
			subprocess.run(f"echo [{folder}] >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo path = {dir_location}/{folder} >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo writable = yes >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo read only = no >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo available = yes >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo browsable = yes >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo public = yes >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo force user = {newuser} >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo valid users = {newuser} >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo ntlm auth = yes >> /etc/samba/smb.conf", shell=True)
			print("folder {folder} was created with 770 privledges and can only be accessed by {newuser}'s username and password\n")
		else:
			subprocess.run(f"chmod -R 777 {dir_location}/{folder}", shell=True)
			subprocess.run(f"echo [{folder}] >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo path = {dir_location}/{folder} >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo writable = yes >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo read only = no >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo available = yes >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo browsable = yes >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo public = yes >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo null password = yes >> /etc/samba/smb.conf", shell=True)
			subprocess.run(f"echo ntlm auth = yes >> /etc/samba/smb.conf", shell=True)
			print("folder {folder} was created with 777 privledges and can be accessed by any user\n")
	print(f"Your new Samba user is {newuser} and Samba password, not the users password, is {samba_password} which will be used to log into the protected folders from windows")
	print("creation was sucesssful, will restart Samba in 5 seconds")
	t.sleep(5)
	subprocess.run("systemctl restart smbd", shell=True)

if __name__ == "__main__":

	choice = input("Are you using root account? type yes or no: ")
	if choice == "no":
		print("change user to root first")
	if choice == "yes":
		subprocess.run("echo Continueing Installation: ", shell=True)
		installation()
		newuser = input("Please add a NEW user for system that will be used for Samba: ")
		user_creation(newuser)
		folder_creation(newuser)






