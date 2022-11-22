FROM python:3.10
WORKDIR /opt
HEALTHCHECK CMD curl -f http://localhost:8080/health_check || exit 1
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["./yellbot.py"]
