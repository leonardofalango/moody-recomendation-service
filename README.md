# Installation

```
git clone https://github.com/leonardofalango/moody-recomendation-service/
python -m venv venv
./venv/Scripts/activate
pip install -r ./requirements.txt
fastapi dev app.py 
```

# Using

Just make a request with user id in url like:
```
http://127.0.0.1:8000/user/{user_id}
```
