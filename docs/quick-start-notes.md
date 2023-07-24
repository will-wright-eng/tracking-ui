# quick start notes

```bash
docker-compose run --rm backend alembic upgrade head
```

- modified flower container
- `npm update` wont update major versions
- python docker image to 3.11

- removed celery and flower entirely
- bash scripts/build.sh

```bash
rm pyproject.toml
cat requirements.txt | xargs poetry add
poetry export -f requirements.txt --output requirements.txt
docker build -t test .
```
