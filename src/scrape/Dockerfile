# Run command: docker run -v /Users/Metaverse/Desktop/Personal/Insight/projects/myrate/src/scrape:/app test
FROM ubuntu:bionic

# Meta-Data
LABEL maintainer="Landon Gibson <landon.g42@gmail.com>" \
      description="Docker container for scraping with Selenium and BeautifulSoup"

# Set working directory to /app
WORKDIR /app

# Copy current directory contents into /app
COPY . /app

# Creating a mounted volume so I can move scraped data out
VOLUME /app

# Installing xvfb and dependencies to download geckodriver and firefox
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 libgbm1 \
    curl unzip wget xvfb

# install geckodriver and firefox

RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver

ARG FIREFOX_VERSION=79.0
RUN apt-get update -qqy \
  && apt-get -qqy --no-install-recommends install firefox \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
  && wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 \
  && apt-get -y purge firefox \
  && rm -rf /opt/firefox \
  && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
  && rm /tmp/firefox.tar.bz2 \
  && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
  && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox

# install chromedriver and google-chrome
# RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
#     wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
#     unzip chromedriver_linux64.zip -d /usr/bin && \
#     chmod +x /usr/bin/chromedriver && \
#     rm chromedriver_linux64.zip

# RUN CHROME_SETUP=google-chrome.deb && \
#     wget -O $CHROME_SETUP "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
#     dpkg -i $CHROME_SETUP && \
#     apt-get install -y -f && \
#     rm $CHROME_SETUP

# Environment Variables
# ENV DISPLAY=:99
# ENV LANG C.UTF-8
# ENV LC_ALL C.UTF-8
# ENV PYTHONUNBUFFERED=1

# Install required libraries
# RUN pip install --upgrade pip
RUN pip3 install selenium bs4 pandas numpy requests pyvirtualdisplay

# Make port 8888 available to the outside world
EXPOSE 8888

CMD ["python3", "./scrape_dynamic_oop.py"]
