FROM python:3.11-slim-buster

# Set the working directory
WORKDIR /home/const/AiTomaton-PriceParser

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies for geckodriver and firefox
RUN apt-get update && \
    apt-get install -y wget bzip2 && \
    apt-get install -y firefox-esr

# Download and install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.32.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-v0.32.0-linux64.tar.gz

# Set environment variables for geckodriver and firefox
ENV GECKODRIVER_PATH=/usr/local/bin/geckodriver
ENV FIREFOX_PATH=/usr/bin/firefox

# Run app.py when the container launches
CMD ["python3", "./main.py"]