FROM lscr.io/linuxserver/sonarr:latest
LABEL Maintainer="bizalu"

# Prepare python environment
ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache python3 py3-defusedxml py3-psycopg2
RUN apk -U upgrade --no-cache
RUN if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi

# Install custom post files
COPY scripts/services/ /etc/s6-overlay/s6-rc.d/
RUN find /etc/s6-overlay/s6-rc.d/ -name run -exec chmod u+x {} \;

# Install custom init script
COPY scripts/10-init-config.sh /custom-cont-init.d/
RUN chmod 744 /custom-cont-init.d/*
COPY src/init/ /app/init/

# Install custom post script
COPY scripts/10-custom-config.sh /custom-cont-post.d/
RUN chmod 744 /custom-cont-post.d/*
COPY /src/config/ /app/config/
