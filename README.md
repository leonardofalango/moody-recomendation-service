# Personalized Recommendation Project

🎉 This is a personalized recommendation project that utilizes a custom recommendation model to provide recommendations of places for users based on their profiles and preferences.

## Base API Link

🌐 The API is hosted at: https://moody-recomendation-service.vercel.app
📚 You can find the API documentation here.


## Instalação

1. Clone this repository to your local environment::

```bash
git clone https://github.com/leonardofalango/moody-recomendation-service/
```

2. Navigate to the project directory:

```bash
cd moody-recomendation-service
```

3. Install the necessary dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

🚀🚀 To start the server and access the API routes, run the following command:
```bash
uvicorn app:app --reload
```
🚀 Usage of any commands below will work samely:
````
python ./app.py
fastapi run
```

🔍 This will start the FastAPI server locally. You can then access the API documentation at http://localhost:8000/docs in your browser to see all available routes and test them interactively.

## Example Routes:
- **GET /docs for documentation
- **GET /v1/status**: Returns the server status.
- **GET /v1/get_all**: Returns all data from the database.
- **GET /v1/user/{user_id}**: Returns user data with the provided ID.
- **GET /v1/recommend/{user_id}**: Returns recommendations for the user with the provided ID.
- **GET /v1/recommend/{user_id}/{n_recommendations}/{k_neighboors}**: Returns recommendations for the user with the provided ID, specifying the desired number of recommendations and the number of neighbors to consider.
- **GET /v1/recommend/{user_id}/places={n_recommendations}**: Returns recommendations for the user with the provided ID, specifying only the desired number of recommendations.
