#!/bin/bash
# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt update
apt install -y ./google-chrome-stable_current_amd64.deb

# Install Chromedriver matching Chrome version
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)
wget -N https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip || \
wget -N https://chromedriver.storage.googleapis.com/LATEST_RELEASE && \
LATEST=$(cat LATEST_RELEASE) && \
wget -N https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip

unzip -o chromedriver_linux64.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
