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

# install chromedriver and google-chrome
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/bin && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver_linux64.zip

RUN CHROME_SETUP=google-chrome.deb && \
    wget -O $CHROME_SETUP "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    dpkg -i $CHROME_SETUP && \
    apt-get install -y -f && \
    rm $CHROME_SETUP


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

CMD ["python3", "./scrape_dynamic.py"]
