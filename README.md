etcd2etcd
=========
etcd key copier for fun.
* v2 api only
* usage:
```
$ docker run -it --rm minyk/etcd2etcd:v0.2 --source http://client.etcdtest1.l4lb.thisdcos.directory:2379 --destination http://client.etcdtest2.l4lb.thisdcos.directory:2379 --source-key KEY1 --destination-key KEY2
```
