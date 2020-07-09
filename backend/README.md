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
IMPORTANT: If the above command does not work, create a database in PSQL named 'trivia' and run the following:
'''
psql -U username -d database_name -f trivia.psql
'''

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `app.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

# API Documentation

## Methods
- This API handles calls with three basic HTTP methods: 'GET', 'POST', and 'DELETE'.

## Objects
- There are twp types of objects in this Trivia API:
    - Categories: consisting of Science, Art, Geography, History, Entertainment, and Sports (6 in total)
    - Questions: consisting of the questions themselves, each belonging to a specific category, and with a difficulty from 1 to 5 (easiest to hardest)
        - All questions have a respective answer

### GET examples

#### GET '/categories' (i.e. "curl http://localhost:5000/categories")
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{
    'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    },
    'success': true
}
```

#### GET '/questions' (i.e. "curl http://localhost:5000/questions?page=2")
- Fetches a list (paginated - limit of 10 per page) of questions, including all categories
- Request parameters: page:int
- Returns: a list of questions of every category, success status, and total number of questions in the trivia database
```
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    [...] # Shortened
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

### GET '/categories/<int:category_id>/questions' (i.e. 'curl http://localhost:5000/categories/5/questions')
- Fetches all the questions that belong to a specific category (based on category id)
- Request argument: category_id:int
- Returns a category id, a list of questions in that category, a success status, and the total number of questions in that list
```
  "current_category": 5,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### DELETE example - `/questions/<question_id>` (i.e. `curl -X DELETE http://localhost:5000/questions/2`)
- Deletes an existing question from the trivia database, based on its id (in the example shown, question "2" is deleted)
- Request arguments: question_id:int
```
{
    'deleted': 2,
    'success': true
}
```  

### POST examples

#### POST `/questions` (i.e. `curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d '{"question": "What is the capital of Argentina?", "answer": "Buenos Aires", "category": "3", "difficulty": 1}'`)
- Adds a new question to the trivia database
- Request arguments: requests a body via 'application/json' type, which includes {question:string, answer:string, difficulty:int, category:string}
```
{
  "created": 40, 
  "success": true
}
```

#### POST `/questions/search` (i.e. `curl -X POST http://localhost:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "boxer"}'`)
- Fetches questions via 'application/json' type, where a substring matches with the search term (case insensitive)
- Returns a list of questions that match the search term, the number of total matches found, and a success status
```
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### POST '/quizzes' (i.e. `curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"id": 4, "type": "History"}}'`)
- Fetches a random question via the 'application/json' type, matching the category id and type specified in the data
- Returns a single random question, based on the questions that have been previously answered (and omits them), along with a success status
```
  "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  },
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```