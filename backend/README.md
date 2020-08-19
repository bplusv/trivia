# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Documentation

### GET /categories
Returns all the available categories for the questions in a dictionary with category ID keys

Request
- Query params: None
- URL params: None
```
curl -X GET "http://127.0.0.1:5000/categories"
```

Response
```
{
    'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography"
    }
}
```

### GET /questions
Return all the questions, paginated by groups of 10 questions.

Request
- Query params:
    - page: int
- URL params: None
```
curl -X GET "http://127.0.0.1:5000/questions?page=1"
```

Response
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography"
  },
  "current_category": 0,        
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "total_questions": 17
}
```

### DELETE /questions/{question_id}
Delete the specified question by question id.

Request
- Query params: None
- URL params: question_id: int
```
curl -X DELETE "http://127.0.0.1:5000/questions/1"
```

Response
```
{
  "success": true
}
```

### POST /questions
Create a new question by sending the required json data.

Request
- Query params: None
- URL params: None
- Body: JSON
```
curl -X POST "http://127.0.0.1:5000/questions" -H "Content-Type: application/json" -d "{\"question\": \"What color is sky?\", \"answer\": \"Blue\", \"difficulty\": 1, \"category\": 1}"
```

Response
```
{
  "success": true,
  "question_id": 23
}
```

### POST /questions
Search for questions by using the searchTerm property in json data.

Request
- Query params: None
- URL params: None
- Body: JSON
```
curl -X POST "http://127.0.0.1:5000/questions" -H "Content-Type: application/json" -d "{\"searchTerm\": \"world\"}"
```

Response
```
{
  "current_category": 0,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "total_questions": 19
}
```

### GET /categories/{category_id}/questions
Get questions from the specified category only.

Request
- Query params: None
- URL params: category_id: int
```
curl -X GET "http://127.0.0.1:5000/categories/6/questions"
```

Response
```
{
  "current_category": 6,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "total_questions": 19
}
```

### POST /quizzes
Play a quiz game by getting a random next question from a category, ommiting previous questions in the same play session. The game ends when there's no more available questions.

Request
- Query params: None
- URL params: None
- Body: JSON
```
curl -X POST "http://127.0.0.1:5000/quizzes" -H "Content-Type: application/json" -d "{\"previous_questions\": [10], \"quiz_category\": {\"id\": 6, \"type\": \"Sports\"}}"
```

Response
```
{
  "question": {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
  }
}
```

### POST /categories
Add a new category by sending the required json data

Request
- Query params: None
- URL params: None
- Body: JSON
```
curl -X POST http://127.0.0.1:5000/categories -H "Content-Type: application/json" -d "{\"new_category\": \"animation\"}"
```

Response
```
{
  "category_id": 8,
  "success": true
}
``

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": false, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Entity Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error

## Authors
Luis Salazar

## Acknowledgements
Thanks to Udacity team.