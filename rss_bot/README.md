## Build the image
```
docker build -t rss-bot .
```

## Run with token
```
docker run --restart always -d -e GITHUB_TOKEN=$GITHUB_TOKEN rss-bot
```
