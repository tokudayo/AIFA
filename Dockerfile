FROM python:3.9

# Create workdir directory
RUN mkdir -p /app/ai
WORKDIR /app

# Install Python packages
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Install dependencies
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Copying source files
COPY ./ai /app/ai
COPY main.py /app/
COPY utils.py /app/

CMD ["python", "main.py"]
