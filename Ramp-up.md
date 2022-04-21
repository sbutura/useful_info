# Steps to setup environment
1. Install Ubuntu on Windows, VS Code, Python 3.8/3.9, PyCharm, DBeaver, DataGrip
2. Create morningstar github account following steps from [here](https://mswiki.morningstar.com/display/ITSM/Onboard+a+user+to+Morningstar%27s+organization+on+GitHub).
3. Read docs about [Great Expectations](https://docs.greatexpectations.io/docs/)
4. Follow [Great Expectations Getting started tutorial](https://docs.greatexpectations.io/docs/guides/setup/setup_overview)
   
   **NOTE:** on my case after pip install great_expectations and running $ **great_expectations --version** command, isn't working from Ubuntu terminal but is working from VS Code terminal ¯\ _ (ツ) _ / ¯
5. Install aws cli 
6. Install docker **!!!NOT WORKING!!!**
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

   


