FROM python:3.8-alpine

WORKDIR /opt/mike

# @see https://leemendelowitz.github.io/blog/how-does-python-find-packages.html
# Python by default reads site packages from /usr/local/lib/python3.8/site-packages
# while apk install py3-lxml to /usr/lib/python3.8/site-packages
ENV PYTHONPATH /usr/local/lib/python3.8/site-packages:/usr/lib/python3.8/site-packages

# install the initial set of dependencies that do not depend on setup.py (i.e. change less frequently)
RUN apk add --update --no-cache mariadb-connector-c py3-cryptography py3-lxml py3-future py3-yaml \
    && pip list

# install project dependencies
COPY setup.py .
COPY mycroft_holmes/__init__.py mycroft_holmes/
COPY mycroft_holmes/bin mycroft_holmes/bin

RUN apk add --no-cache --virtual .build-deps build-base automake autoconf libtool mariadb-dev libffi-dev \
    && pip install -e . \
    && apk del .build-deps \
    && pip list

# copy the rest of the files
COPY . .

# expose the HTTP port
EXPOSE 5000

# label the image with branch name and commit hash
LABEL maintainer="maciej.brencz@gmail.com"
ARG BRANCH="master"
ARG COMMIT=""
LABEL branch=${BRANCH}
LABEL commit=${COMMIT}

# your custom config YAML should be mounted
# and MIKE_CONFIG env variable should point to it
ENV MIKE_CONFIG /opt/mike/example.yaml

ENV COMMIT_SHA=${COMMIT}
ENV COMMIT_BRANCH=${BRANCH}

# entrypoint script
RUN echo "gunicorn 'mycroft_holmes.app.app:setup_app()' --worker-class sync -b 0.0.0.0:5000 --workers 4 --access-logfile -" > entrypoint

# do not run as root
USER 65534

# run the app
CMD ["sh", "entrypoint"]

# https://docs.docker.com/engine/reference/builder/#healthcheck
HEALTHCHECK --interval=15s --timeout=1s --retries=3 \
  CMD wget 0.0.0.0:5000 --spider -q -U 'wget/healthcheck' || exit 1
