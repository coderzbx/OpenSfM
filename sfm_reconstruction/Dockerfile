FROM kd-bd02.kuandeng.com/pavement_distresses/sfm_reconstruction:base

RUN useradd --create-home --no-log-init --shell /bin/bash hadoop
RUN adduser hadoop sudo
RUN echo 'hadoop:hadoop' | chpasswd

USER hadoop

ADD sfm_reconstruction /home/hadoop/bin
ADD run.sh /home/hadoop/bin
