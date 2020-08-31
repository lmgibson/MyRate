FROM python:3.8

# Meta-Data
LABEL maintainer="Landon Gibson <landon.g42@gmail.com>" \
      description="Docker container for scraping with Selenium and BeautifulSoup"

# Set working directory to /app
WORKDIR /app

# Copy current directory contents into /app
COPY . /app


# Creating a mounted volume so I can move scraped data out
VOLUME /app

# Install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port to avoid crash
ENV DISPLAY=:99

# Install required libraries
# RUN pip install --upgrade pip
RUN pip --no-cache-dir install selenium bs4 pandas numpy requests

# Make port 8888 available to the outside world
EXPOSE 8888

#RUN pip install -r requirements.txt

CMD ["python", "./scrape.py"]
