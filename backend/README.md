# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
# API DOCUMENTATION
## Getting started
- Base URL: This projected is hosted locally and so uses the default http://127.0.0.1:5000
- authentication: this app does not use Authentication (at least for this version)

## Error handling
expected errors are formatted in JSON like the example shown bellow:
```
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

bellow are the expected error cases for the API
- 400 : "Bad request"
- 404 : "Resource not found"
- 500 : "Internal Server Error"
- 422 : "could not process recource"
## Endpoints
GET  '/categories'
GET '/questions?page=<pageNumber>'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'


### GET  '/categories'
- fetches the categories of questions in a dictionary with the id and Category type as key and value respectively 
- **Request arguments**: None
- **Sample request**: `curl http://127.0.0.1:5000/categories`
- **Sample response**:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```


### GET '/questions?page=<pageNumber>'
- Fetches a list of paginated formated questions of maximum of ten questions per page along with the dictionary of categories
- **Request arguments**: page=int(Not required)
- **sample request**: `curl http://127.0.0.1:5000/questions?page=3`
- **sample response**:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 68,
      "question": "Who discovered penicilin?"
    },
    {
      "answer": "gravity",
      "category": 1,
      "difficulty": 1,
      "id": 69,
      "question": "what makes thing fall?"
    }
  ],
  "success": true,
  "total_questions": 22
}
```


### DELETE '/questions/<int:question_id>'
- gets a question using the question_id from the URL and deletes it
-**Request arguments**: question_id,int(required) 
- **Sample request**: `curl -X DELETE http://127.0.0.1:5000/questions/1`
- **Sample response**:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "deleted": 1,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
}
```


### POST '/questions'
- Creates new questions by accepting question, answer , difficulty and category from the user
- **Request arguments**: question:string(required) , answer:string(required) , category:number string(required) , difficulty:int(required)
- **Sample request**: `curl -X POST http://127.0.0.1:5000/questions  -H "Content-Type:application/json "  -d "{\"question\":\"What year did Michael Jackson Die? \" , \"answer\":\"2009\" , \"difficulty\":\"2\" , \"category\":\"2\"}"`
- **Sample response**: 
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "created": 70,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
}
```


### POST '/questions/search'
- Fetches question(s) that match the search term or questions of which the search term is a substring of , the search mechanism is case insensitive.
- **Request arguments**: searchTerm:string(required) 
- **Sample request**:`curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type:application/json"  -d "{\"searchTerm\":\"what\"}"`
- **Sample response**:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Age",
      "category": 4,
      "difficulty": 2,
      "id": 27,
      "question": "What rises but never falls?"
    }
  ],
  "searchTerm": "what",
  "success": true,
  "total_questions": 1
}
```


### GET '/categories/<int:category_id>/questions'
- Returns questions of a selected category based off of the category_id argument
- **Request arguments**: category_id ,data type=int (required) 
- **Sample request**:`curl http://127.0.0.1:5000/categories/1/questions`
- **Sample response**:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    }
}
```

### POST '/quizzes'
- Fetches a question to play the game based on the category selected. No one question gets repeated and user gets a maximum of five questions per play.
- **Request arguments**: previous_questions:List(required) ,quiz_category:dict,of category id and type  (required) 
- **Sample request**:`curl -X POST http://127.0.0.1:5000/quizzes  -H "Content-Type:application/json "  -d "{\"previous_questions\":[], \"quiz_category\":{\"id\":"2" , \"type\":\"art\"} }"`
- **Sample response**:
```
{
  "previousQuestions": [],
  "question": {
    "answer": "2009",
    "category": 2,
    "difficulty": 2,
    "id": 70,
    "question": "What year did Michael Jackson Die? "
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
