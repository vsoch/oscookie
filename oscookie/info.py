'''

info.py: get lists of packages, and managers to support main functions


'''

## OS IMAGES (provided via official docker library)
def get_baseos():
    return ['alpine:3.1','alpine:3.2','alpine:3.3','alpine:3.4','alpine:3.5',
            'busybox:1.26.1-glibc','busybox:1.26.1-musl','busybox:1.26.1-uclibc',
            'amazonlinux:latest',
            'centos:7','centos:6','centos:5',
            'cirros:0.3,4','cirros:0.3,3',
            'clearlinux:latest',
            'crux:3.1', # 'crux':'pkginfo --installed'
            'debian:8.6','debian:sid','debian:stretch','debian:wheezy', # 8.6 is jessie, 7.11 is wheezy
            'fedora:25','fedora:24','fedora:23','fedora:22',
            'mageia:5',
            'opensuse:42.2','opensuse:42.1','opensuse:13.2','opensuse:tumbleweed', #  42.2 is leap, 13.2 harlequin
            'oraclelinux:7.3','oraclelinux:7.2','oraclelinux:7.1','oraclelinux:7.0','oraclelinux:6.8',
            'oraclelinux:6.7','oraclelinux:6.6','oraclelinux:5.11',
            'photon:1.0',
            'sourcemage:0.62',
            'swarm:1.2.6-rc1',
            'ubuntu:14.04.5','ubuntu:16.04','ubuntu:16.10','ubuntu:17.04']


# We will generate a package list for each distribution based on the base
def get_managers():
  return {'ubuntu':{"list":'apt list'},
          'alpine':{"list":'apk info'},
          'debian':{"list":'apt list'},
          'oraclelinux':{"list":'yum list'},
          'centos':{"list":'yum list'},
          'debian':{"list":'apt list'},
          'fedora':{"list":'dnf list'},
          'opensuse':{"list":'rpm -qa'},
          'mageia':{"list":'rpm -qa'},
          'photon':{"list":'rpm -qa'}}
