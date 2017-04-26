FROM fedora:25
MAINTAINER Paolo Antinori

RUN useradd -m -d /home/sopel sopel
WORKDIR /home/sopel

RUN dnf update -y && \
    dnf install -y git python3-enchant

RUN pip3 install git+https://github.com/sopel-irc/sopel.git

USER sopel

CMD sopel

COPY scripts/ /tmp/scripts
# this convoluted thing is because of issues to perform `chown` across multiple commands
RUN rm -rf /home/sopel/.sopel &&\
    mkdir -p /home/sopel/.sopel &&\
    cp -R /tmp/scripts/* /home/sopel/.sopel &&\
    chown -R sopel:sopel /home/sopel 
VOLUME /home/sopel/.sopel