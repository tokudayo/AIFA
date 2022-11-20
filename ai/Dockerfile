FROM python:3.9

# Create workdir directory
RUN mkdir -p /app
WORKDIR /app

# Copying source files
COPY . /app

# Install dependencies
# RUN apt-get update
# RUN apt-get install ffmpeg libsm6 libxext6 -y

# Install Python packages
RUN python -m pip install --upgrade pip
RUN pip install kafka-python==2.0.2
RUN pip install .

CMD ["python", "run.py"]
