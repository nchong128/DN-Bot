FROM python:3.7-slim
RUN apt-get update && apt-get install -y build-essential libpq-dev python3-dev

# Firefox Headless
RUN apt-get update && apt-get install -y python-selenium firefox-esr jq dos2unix curl libnss3-tools
COPY gecko-driver-install.sh /app/
RUN chmod +x /app/gecko-driver-install.sh
RUN /app/gecko-driver-install.sh
RUN mkdir downloads
RUN firefox -Headless -CreateProfile nchong

# python application dependencies
RUN pip install --upgrade pip=="20.1.1"
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY *.py /app/

ENV FLASK_APP=/app/main.py

ENTRYPOINT ["/usr/local/bin/python", "/app/main.py"]