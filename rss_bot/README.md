## Build the image
```
docker build -t rss-bot .
```

## Run with token
```
docker run -d -e GITHUB_TOKEN=$GITHUB_TOKEN rss-bot
```
