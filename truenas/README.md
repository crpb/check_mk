# SCALE
## Tasks on OMD
- To use with a "Individual program call instead of agent access"
- on the omd host
  ```
  sudo -i -u sitename
  HOSTNAME=truenas.what.ever.domain.tld
  ssh-keygen -C "checkmk@$HOSTNAME" -t ed25519 -P "" -f ~/.ssh/$HOSTNAME >/dev/null
  cat ~/.ssh/$HOSTNAME.pub
  ```
- Add a rule for the host with something like
  `ssh -p NNNNNN -i ~/.ssh/$HOSTNAME$ -o StrictHostKeyChecking=yes -l checkmk $HOSTNAME$`
## Tasks on TrueNAS
- Create a new user
  - username: checkmk
  - disable password
  - SSH Access (which includes shell access)
  - opt. TrueNAS Access: Readonly Admin?
  - home: /mnt/pool/some/where/checkmk
  - public ssh key
    `command="sudo /mnt/pool/some/where/checkmk/check_mk_agent.linux" ssh-ed...`
- After creating the user install the agent (as root)
  ```
  cd ~checkmk
  wget https://raw.githubusercontent.com/crpb/check_mk/refs/heads/main/truenas/cmk.scale
  chmod +x cmk.scale
  ./cmk.scale
  ```
- Edit the user in the truenas gui and add a passwordless sudo command
  e.g. `/mnt/pool/some/where/checkmk/check_mk_agent.linux`

- Test the connection from the OMD System
  `ssh -i ~/.ssh/$HOST -p NNNNN $HOSTNAME -l checkmk $HOSTNAME`

# CORE
- To use with classic port 6556
- Activate TFTP-Server
- Run script from wherever it should be installed
