# Truth or Dare

## Setup
```
python3 -m pip install pipenv
pipenv install
```

If pipenv is not found, you can try to add `python3 -m ` before pipenv

```
python3 -m pipenv --version
```

## Run
```
pipenv run invoke simpletod
```
## Notes

`export BG_VAR_log_level="ERROR"`
or
`export BG_VAR_log_level="INFO"`

python3 -m pipenv run pip freeze > requirements.txt

## Docker
docker build -t hneil/tod .
docker run -it --rm --name TruthOrDare hneil/tod

## TODO:

- Add Unit Tests
- Add Better GUI