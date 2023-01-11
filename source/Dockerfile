FROM python:3.9
# NGIX CONFIG
RUN apt update
RUN apt install nginx -y
RUN  rm /etc/nginx/nginx.conf
COPY test.db    /tmp
COPY nginx.conf /etc/nginx
COPY cert.pem /etc/nginx
COPY key.pem /etc/nginx
# PYTHON CONFIG
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install uwsgi bcrypt flask-login flask-sqlalchemy pbkdf2 bleach pycryptodome
# COPY PYTHON APP
RUN mkdir -p /opt/custom/flaskapp
COPY app /opt/custom/flaskapp

# CONFIG UWSGI
ENV UWSGI_INI /opt/custom/flaskapp/uwsgi.ini
ENV KEY c741d3e2fa1865992687d548d735cf533381
WORKDIR /opt/custom/flaskapp
EXPOSE 443
EXPOSE 80
CMD ["./startup.sh"]
