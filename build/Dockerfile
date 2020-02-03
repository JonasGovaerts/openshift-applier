from registry.redhat.io/ubi7/ubi

LABEL maintainer=govaertsjonas1@gmail.com
LABEL source=gitlab.com/https://gitlab.com/jonasgovaerts/ocp_namespace-applier

RUN yum install --enablerepo="rhel-server-rhscl-7-rpms" --enablerepo="rhel-7-server-rpms" -y python git openssh-clients

WORKDIR /usr/src/app

COPY ["./binaries/oc", "/usr/local/bin"]
COPY ["./script/namespace_applier.py", "/usr/src/app"]

ENTRYPOINT ["python", "-u", "./namespace_applier.py"]
