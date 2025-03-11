# Prometheus exporter for tqdm

Publish your pretty CLI stats for monitoring elsewhere

## Usage

```sh
TqdmPromProxy().start(3000)

curl http://localhost:3000/metrics
```

## Todo

@Todo: move these to gh

Poll tqdm for juicy stats
Publish over http
Add options for https
