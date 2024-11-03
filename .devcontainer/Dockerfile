FROM mcr.microsoft.com/vscode/devcontainers/python:3

ARG UNAME=vscode
ARG UID=1000
ARG GID=1000

RUN <<EOF
    userdel $UNAME
    groupadd -g $GID -o $UNAME
    useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
    mkdir -p /home/$UNAME/bin
    apt-get -y update
    apt-get -y full-upgrade
    apt-get -y install ripgrep
    apt-get -y clean
EOF

RUN chown -R $UNAME:$UNAME /home/$UNAME

USER $UNAME

ENTRYPOINT exec /bin/bash -c 'trap : TERM INT; sleep infinity & wait'
