# Experiment with downloading stuff.


Get the package dependencies updated with:

```bash
uv sync --upgrade
```


Run service with:

```bash
./main.py
```

Access service with:

```bash
curl -X POST http://localhost:8000/download -H "Content-Type: application/json" -d '{"url":"https://www.youtube.com/watch?v=TYZGSDaVu_0"}'
```
