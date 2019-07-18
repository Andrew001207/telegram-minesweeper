FROM python:3.7

RUN pip install python-telegram-bot==12.0.0b1
RUN pip install opencv-python
RUN pip install numpy
RUN pip install pillow
RUN pip install matplotlib

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/telegram_bot.py