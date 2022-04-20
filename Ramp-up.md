# Steps to setup environment
1. install Ubuntu on Windows
2. install aws cli 
3. install docker **!!!NOT WORKING!!!**
    - $ sudo apt install docker.io
    - $ docker --version
    - $ sudo systemctl status docker --> this command will not work on Ubuntu on WSL. Will throw this error: "System has not been booted with systemd as init system (PID 1). Can't operate."
    - $ ps -p 1 -o comm= --> this will show which init system I am using ( systemd / sysv). if output is 'init' the system is not using systemd but sysvinit 
   - $ sudo systemctl enable --now docker --> enable docker daemon, but will not work because of the init system :(
  
Systemd command | Sysvinit command 
---|---
systemctl start service_name|service service_name start
systemctl stop service_name|service service_name stop
systemctl restart service_name|service service_name restart
systemctl status service_name|service service_name status
systemctl enable service_name|chkconfig service_name on
systemctl disable service_name|chkconfig service_name off

   


