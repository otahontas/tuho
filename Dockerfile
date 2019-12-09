FROM python:3
MAINTAINER Otto Ahoniemi "otto@ottoahoniemi.fi"
ADD run.py /
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
