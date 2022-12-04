# Mess Assistant

A Task-Oriented Pipeline Based Dialogue System to provide a front end to
the IIIT Hyderabad institute mess portal.

## Requirements

- python 3.8
- rasa
- docker


## Running the Assistant

### First Time

- Install all dependencies in a virtual environment
```shell
pip install -r requirements.txt
```
- Train the model
```shell
rasa train
```

### Run in terminal

- Run Duckling Docker Container
```shell
docker run -p 8000:8000 rasa/duckling
```
- Run Actions in a separate terminal

```shell
rasa run actions
```
- Launch assistant in another terminal
```shell
rasa shell
```
- Launch Rasa backend
```shell
rasa run --cors "*"
```