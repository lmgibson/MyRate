
FROM ubuntu:trusty

RUN apt-get update

RUN apt-get install -y python3 python3-pip

RUN apt-get install -y libgconf2-4 libnss3-1d libxss1
RUN apt-get install -y fonts-liberation libappindicator1 xdg-utils

RUN apt-get install -y software-properties-common
RUN apt-get install -y curl unzip wget

RUN apt-get install -y xvfb


# install geckodriver and firefox

RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver

RUN add-apt-repository -y ppa:ubuntu-mozilla-daily/ppa
RUN apt-get update -y
RUN apt-get install -y firefox


# install phantomjs

RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar -jxf phantomjs-2.1.1-linux-x86_64.tar.bz2 && cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs

RUN pip3 install --upgrade --ignore-installed urllib3
RUN pip3 install selenium beautifulsoup4 requests sqlalchemy sqlalchemy_utils psycopg2 re
RUN pip3 install pyvirtualdisplay


ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

COPY ./hello_world.py $APP_HOME/

CMD tail -f /dev/null
CMD python3 hello_world.py
