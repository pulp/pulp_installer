FROM fedora:28
MAINTAINER ppicka@redhat.com

RUN dnf -y install \
 openssh-server \
 openssh-clients \
 sudo \
 passwd \
 which \
 sshfs \
 python3-libselinux \
 selinux-policy \
 firewalld \
 && dnf clean all

RUN echo 'root:root' | chpasswd
RUN useradd vagrant
RUN echo 'vagrant:vagrant' | chpasswd
RUN echo 'vagrant ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

CMD /sbin/init
