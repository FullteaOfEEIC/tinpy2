FROM python:3.8.1

RUN pip install --upgrade pip setuptools\
 requests\
 robobrowser\
 Werkzeug==0.16.1\
 mysqlclient
 
ADD *.py /
ADD infos.json /

CMD python main.py

