from docker.io/centos:8

LABEL maintainer=govaertsjonas1@gmail.com
LABEL source=gitlab.com/https://gitlab.com/jonasgovaerts/ocp_namespace-applier

ENV HOME=/root

RUN yum install -y python38 git wget python3-pip && wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz -O /tmp/oc.tar.gz && tar -xvzf /tmp/oc.tar.gz -C /usr/local/bin/ --strip-components 1 && rm /tmp/oc.tar.gz && pip3 install gitpython && wget https://github.com/mikefarah/yq/releases/download/3.4.0/yq_linux_amd64 -O /usr/bin/yq && chmod +x /usr/bin/yq

WORKDIR /root

COPY ["./script/namespace_applier.py", "/usr/src/app/namespace_applier.py"]
COPY ["./script/oc_apply", "/usr/local/bin/oc_apply"]

RUN mkdir -p /resources && chgrp -R 0 /root && chmod -R g=u /root && chgrp -R 0 /usr/src/app && chmod -R g=u /usr/src/app && chgrp -R 0 /resources && chmod -R g=u /resources && chmod +x /usr/local/bin/oc_apply

ENTRYPOINT ["python3", "-u", "/usr/src/app/namespace_applier.py"]
