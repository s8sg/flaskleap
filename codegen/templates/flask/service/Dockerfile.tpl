FROM ubuntu

RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

RUN apt-get update; return 0

RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

RUN apt-get install -y python python-dev python-distribute python-pip

RUN apt-get install -y libsasl2-dev libldap2-dev libssl-dev

RUN apt-get install -y pandoc

RUN mkdir /{{ service_name }}

COPY requirements.txt /{{ service_name }}/requirements.txt
COPY {{ service_name }} /{{ service_name }}/{{ service_name }}
COPY setup.py /{{ service_name }}/setup.py
COPY setup.cfg /{{ service_name }}/setup.cfg
COPY server.py /{{ service_name }}/server.py
COPY tox.ini /{{ service_name }}/tox.ini
COPY Makefile /{{ service_name }}/Makefile
COPY README.md /{{ service_name }}/README.md
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x docker-entrypoint.sh
RUN pip install --upgrade pip 
RUN pip install -r /{{ service_name }}/requirements.txt
# cherrypy servs as a light weight wsgi server
RUN pip install cherrypy
# As we don't need the flask app to be installed 
# we use dev mode to install the dependency
RUN cd {{ service_name }};make install-dev

EXPOSE 8080

WORKDIR /

ENTRYPOINT ["/docker-entrypoint.sh"]
