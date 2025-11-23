FROM alpine:latest

# Install dependencies
RUN apk add --no-cache curl git

# Install supercronic
RUN curl -fsSLO https://github.com/aptible/supercronic/releases/download/v0.2.1/supercronic-linux-amd64 \
    && chmod +x supercronic-linux-amd64 \
    && mv supercronic-linux-amd64 /usr/local/bin/supercronic

# Set working directory
WORKDIR /app

# Copy repository files
COPY . .

# Make the script executable
RUN chmod +x update_rss.sh

# Configure Git (will use env var for token)
RUN git config --global user.email "rssbot@example.com" && \
    git config --global user.name "rssbot"

# Create crontab entry (every 10 minutes)
# RUN echo '*/10 * * * * cd /app && ./update_rss.sh' > /etc/crontab
RUN echo '0 * * * * cd /app && ./update_rss.sh' > /etc/crontab

# Start supercronic
CMD ["supercronic", "/etc/crontab"]
