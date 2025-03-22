FROM mcr.microsoft.com/vscode/devcontainers/python:3

ARG UNAME=vscode
ARG UID=${UID}
ARG GID=${GID}

ARG PUBKEY=${PUBKEY}

RUN --mount=type=ssh <<EOF
set -e
mkdir -p /root/.ssh
ssh-keyscan github.com >> /root/.ssh/known_hosts
chmod 700 /root/.ssh
chmod 600 /root/.ssh/known_hosts

mkdir -p /home/$UNAME/bin /home/$UNAME/.ssh /home/$UNAME/.config/fish/conf.d

echo "${PUBKEY}" > /home/$UNAME/.ssh/authorized_keys

git clone git@github.com:mohshami/dotfiles.dev.git /home/$UNAME/dotfiles

usermod -g $GID $UNAME
chown -R $UNAME:$UNAME /home/$UNAME
chmod 700 /home/$UNAME/.ssh

apt-get -y update
apt-get -y full-upgrade
apt-get -y install ripgrep openssh-server fish pipx
apt-get -y clean
mkdir -p /var/run/sshd

chsh -s /usr/bin/fish $UNAME
su -c 'fish -c "echo"' $UNAME

chown -R $UNAME:$UNAME /home/$UNAME

mkdir -p /home/semaphore/.ssh/
chmod 700 /home/semaphore/.ssh/
chown -R $UNAME:$UNAME /home/semaphore/.ssh/
EOF

RUN ssh-keygen -A -q

ENTRYPOINT ["/usr/sbin/sshd", "-D"]
