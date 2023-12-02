#Last package update 02 December 2023
FROM lscr.io/linuxserver/sonarr:latest
LABEL Maintainer="bizalu"

# Prepare python environment
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get upgrade -y && apt-get install -y python3 python3-defusedxml && apt-get clean
RUN if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi

# Install custom post files
COPY services/ /etc/s6-overlay/s6-rc.d/
RUN find /etc/s6-overlay/s6-rc.d/ -name run -exec chmod u+x {} \;

# Install custom post script
COPY custom-script/ /etc/cont-post.d/
RUN chmod u+x /etc/cont-post.d/*
