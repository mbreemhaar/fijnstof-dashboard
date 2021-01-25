FROM ubuntu:latest
COPY . /
COPY update_schedule /etc/cron.d/update_schedule
RUN apt-get update && apt-get -y install cron python3-pip 
RUN chmod 0644 /etc/cron.d/update_schedule
RUN chmod 0744 /get_data.py
RUN crontab /etc/cron.d/update_schedule
RUN pip3 install -r requirements.txt
EXPOSE 80
CMD cron && python3 server.py -d output
