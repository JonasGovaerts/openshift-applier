from registry.redhat.io/ubi7/ubi

LABEL maintainer=govaertsjonas1@gmail.com
LABEL source=gitlab.com/https://gitlab.com/jonasgovaerts/ocp_namespace-applier

RUN yum install --enablerepo="rhel-server-rhscl-7-rpms" --enablerepo="rhel-7-server-rpms" -y python git wget

RUN wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz -O /tmp/oc.tar.gz && tar -xvzf /tmp/oc.tar.gz -C /usr/local/bin/ --strip-components 1 && rm /tmp/oc.tar.gz

WORKDIR /usr/src/app

COPY ["./script/namespace_applier.py", "/usr/src/app"]

USER 1001

ENTRYPOINT ["python", "-u", "./namespace_applier.py"]