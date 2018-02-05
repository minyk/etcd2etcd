FROM centos:7

RUN yum install -y epel-release && yum install -y python-pip && pip install python-etcd

COPY etcd2etcd.py /etcd2etcd.py

ENTRYPOINT ["/usr/bin/python", "/etcd2etcd.py"]
