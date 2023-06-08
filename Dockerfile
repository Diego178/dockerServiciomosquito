FROM python
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
ADD mqtt.py /mqtt.py
CMD ["python3", "mqtt.py"]
