# SCALE
- To use with a "Individual program call instead of agent access"
- on the omd host
  ```
  sudo -i -u sitename
  ssh-keygen -C "checkmk@$HOSTNAME" -t ed25519 -P "" -f ~/.ssh/$HOSTNAME
  ```
- Add rule for ind. prog. call. and Value
  `ssh -p NNNNNN -i ~/.ssh/$HOSTNAME$ -o StrictHostKeyChecking=yes/no?! -l checkmk  $HOSTNAME$`
- Create read-only-admin: checkmk
- Homedir: e.g. /mnt/poolname/cmk
- ssh-key: command="sudo /mnt/poolname/cmk/cmk.scale" ssh-ed..
- Add sudo-no-password command from above "/mnt/poolname/cmk/cmk.scale"


# CORE
- To use with classic port 6556
- Activate TFTP-Server
- Run script from wherever it should be installed
