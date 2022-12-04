FROM python:3.10-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python3 downloader.py
CMD ["python3", "backtester.py"]