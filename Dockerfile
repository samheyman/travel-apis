FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ADD . /code/
# ENV AMADEUS_CLIENT_ID
# ENV AMADEUS_CLIENT_SECRET
# ENV GOOGLE_MAPS_KEY
# ENV SKYSCANNER_KEY
# ENV AMADEUS_SANDBOX_KEY