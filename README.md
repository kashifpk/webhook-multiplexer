# Dev Testing

Create a `.env` file (see `env_example` for sample).

```shell
poetry run uvicorn webhook_multiplexer.api_main:app --host 0.0.0.0 --port 9999 --reload
```


## Get current forward rules

```shell
# Using curl
curl -H "Authorization: your-auth-token" localhost:9999/_

# Using httpx
httpx -h "Authorization" "your-auth-token" "http://localhost:9999/_"
```

## Create new forward rule

```shell
# Using curl

# Using httpx
httpx -m post -h "Authorization" "your-auth-token" -j '{"incoming": "/data-payload", "outgoing": "http://127.0.0.1:9998/data-payload"}' "http://localhost:9999/_"
```


## Delete a forward rule

```shell
# Using curl


# Using httpx
httpx -m delete -h "Authorization" "your-auth-token" "http://localhost:9999/_/<rule-key>"

```
