# promobot-appeal-api-backend

Web API wrapper for the module - backend part

### [Module](https://github.com/digital-fracture/promobot-appeal-processing)
#### [Documentation](https://digital-fracture.github.io/promobot-appeal-processing)

### [Website](https://front-7.vercel.app)

### [Jupyter notebook with training code](extra/training.ipynb)

### [GitHub repository with front-end code](https://github.com/digital-fracture/promobot-appeal-api-frontend)


## Run by yourself

### Python package (available at [PyPI](https://pypi.org/project/promobot-appeal-processing))
```shell
pip install promobot-appeal-processing
```

### Pipenv

```shell
git clone https://github.com/digital-fracture/promobot-appeal-api-backend
cd promobot-appeal-api-backend
pipenv install
pipenv run uvicorn main:app
```

### Pure python 3.11

Windows (PowerShell) (not tested):
```powershell
git clone https://github.com/digital-fracture/promobot-appeal-api-backend.git
cd promobot-appeal-api-backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app
```

Linux / MacOS:
```shell
git clone https://github.com/digital-fracture/promobot-appeal-api-backend.git
cd promobot-appeal-api-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app
```

## Stack

- [python 3.11](https://python.org) - programming language
- [promobot-appeal-processing](https://pypi.org/project/promobot-appeal-processing) - ML processor
- [FastAPI](https://pypi.org/project/fastapi) - web server engine
- [aiosqlite](https://pypi.org/project/aiosqlite) - asynchronous database handling
- [aiocsv](https://pypi.org/project/aiocsv) - asynchronous `.csv` files handling 
- And more
