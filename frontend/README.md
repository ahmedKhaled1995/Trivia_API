# Full Stack Trivia API Frontend

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: **npm i** is shorthand for **npm install**

## Required Tasks

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Request Formatting

The frontend should be fairly straightforward and disgestible. You'll primarily work within the `components` folder in order to edit the endpoints utilized by the components. While working on your backend request handling and response formatting, you can reference the frontend to view how it parses the responses.

After you complete your endpoints, ensure you return to and update the frontend to make request and handle responses appropriately:

- Correct endpoints
- Update response body handling

## Optional: Styling

In addition, you may want to customize and style the frontend by editing the CSS in the `stylesheets` folder.

## Optional: Game Play Mechanics

Currently, when a user plays the game they play up to five questions of the chosen category. If there are fewer than five questions in a category, the game will end when there are no more questions in that category.

You can optionally update this game play to increase the number of questions or whatever other game mechanics you decide. Make sure to specify the new mechanics of the game in the README of the repo you submit so the reviewers are aware that the behavior is correct.

## Optional: Api Documentation

## 1] Introduction:

This is an introduction section to Trivia api. Trivia api is used to create questions, each question has the following
field:
a) id: int ---> You don't provide it. It is provided automatically by the server.
b) question: string ---> the question itself. Must be provided.
c) answer: string ---> the answer of the question. Must be provided.
d) difficulty: int ---> the difficulty of the question, an int between 0 and 5. Must be provided. 3) category: int ---> an int between 1 and 6. Must be provided. Further detail:
1 ---> Science
2 ---> Art
3 ---> Geography
4 ---> History
5 ---> Entertainment
6 ---> Sports

## 2] Getting started:

a) Base url: http://127.0.0.1:5000/ (localhost)
b) Api keys and authentication: this api doesn't use api keys or authentication.

## 3] Errors:

    Trivia api use http status code. 2xx indicates success of the request, 4xx indicates request received but there
    was an error with the request body and finally, 5xx indicates a server related error.

    ===============================================
    error status     |  description
    ===============================================
    400              |  Bad request
    -----------------------------------------------
    404              |  Resource not found
    -----------------------------------------------
    422              |  Un-processible request body
    -----------------------------------------------
    500              |  Server error
    -----------------------------------------------

## -> error attributes:

1. success: boolean: 'False' in case of error to indicate failure of request.
2. error: int: the http status code of the error.
3. message: string: description of the error.

## 4] Endpoints:

This api has only one public resource (question). Here are the http methods available, what they expect to receive and
what they return: 1) GET '/categories' 2) GET '/questions' 3) GET '/categories/{category_id}/questions' 4) DELETE '/questions/{question_id}' 5) POST '/questions' 6) POST '/questions/search' 7) POST '/quizzes'

    -> Endpoints further detail:
    ----------------------------
    1) GET '/categories'
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Request Body: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
        {
        'categories':
                    {
                        '1' : "Science",
                        '2' : "Art",
                        '3' : "Geography",
                        '4' : "History",
                        '5' : "Entertainment",
                        '6' : "Sports"
                    }
        }

    2) GET '/questions?page=PAGE_NUMBER'
    - Fetches a dictionary of questions, total_questions, categories, current_category in which:
        questions is a list of questions in the page specified in the request as params, gets questions on page 1 if no page is specified. Each page has 10 questions.
        total_questions is the number of all the questions available in the database.
        categories is a dictionary of which the keys are the ids and the value is the corresponding string of the category.
        current_category is an int that represents the category. Gets randomly chosen.
    - Request Arguments: has an optional 'page' argument to get the questions on that page. Each page has 10 questions. If no page is specified, questions on page 1 are returned.
    - Request Body: None
    - Returns: An object with four keys, questions, total_questions, categories, current_category , there content is described above in the 'Fetches' section.
        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "current_category": 6,
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
                ...
            ],
            "total_questions": 21
        }

    3) GET '/categories/{category_id}/questions'
    - Fetches a dictionary of questions, total_questions, current_category in which:
        questions is a list of questions in the category specified in the request.
        total_questions is the number of all the questions available in the database of that category.
        current_category is an int that represents the category specified in the request.
    - Request Arguments: None
    - Request Body: None
    - Returns: An object with three keys, questions, total_questions, current_category , there content is described above in the 'Fetches' section.
        {
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
            ],
            "total_questions": 2
        }

    4) DELETE '/questions/{question_id}'
    - Fetches a dictionary of success, deleted_question_id, total_questions in which:
        success is a boolean that represents the success or the failure of the delete operation.
        deleted_question_id is the number that represents the id of book deleted.
        total_questions is a number that represents the total number of questions left after the deletion operation.
    - Request Arguments: None
    - Request Body: None
    - Returns: An object with three keys, success, deleted_question_id, total_questions , there content is described above in the 'Fetches' section.
        {
            "success": True,
            "deleted_question_id": 52,
            "total_questions": 60
        }

    5) POST '/questions'
    - Fetches a dictionary of success, question_id, total_questions in which:
        success is a boolean that represents the success or the failure of the post operation.
        question_id is the number that represents the id of book posted.
        total_questions is a number that represents the total number of questions left after the post operation.
    - Request Arguments: None
    - Request Body: takes a JSON object of question, answer, difficulty, category. ex:
        {
            'question': "Who is the tennis player with the most grand slams as of 2019?",
            'answer': "Roger Federer",
            'difficulty': 3,
            'category': 6
        }
    - Returns: An object with three keys, success, question_id, total_questions , there content is described above in the 'Fetches' section.
        {
            "success": True,
            "question_id": 52,
            "total_questions": 60
        }


    6) POST '/questions/search'
    - Fetches a dictionary of questions, total_questions, current_category in which:
        questions is a list of questions whose 'question' field is a super string of the search term provided in the request.
        total_questions is the number of all the questions that matches the search term.
        current_category is an int that represents the category, chosen randomly.
    - Request Arguments: None
    - Request Body: takes a JSON object of searchTerm. ex:
        {
            'searchTerm': 'tennis'
        }
    - Returns: An object with three keys, questions, total_questions, current_category , there content is described above in the 'Fetches' section.
        {
            "current_category": 2,
            "questions": [
                {
                    "answer": "Roger Federer",
                    "category": 6,
                    "difficulty": 3,
                    "id": 52,
                    "question": "Who is the tennis player with the most grand slams as of 2019?"
                }
            ],
            "total_questions": 1
        }

    7) POST '/quizzes'
    - Fetches a dictionary with a single key, that key is the next question in the game. That question's category is specified in
        the request and that question must also be not asked before.
    - Request Arguments: None
    - Request Body: takes a JSON object of quiz_category, previous_questions. quiz_category is the category object (keys id and type) you want the question to be asked from,
        previous_questions is a list of the previous questions asked Ids.
        {
            'quiz_category': {
                "id": 6,
                "type": "Sports"
            },
            'previous_questions': [12, 7, 5, 42]
        }
    - Returns: An object with a single key 'question', whose value is a JSON object of id, answer, question, difficulty, category.
        {
        "question": {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
            }
        }

    -> Error example to the endpoints:
    -------------------------------------

    1) GET '/questions?page=PAGE_NUMBER'
    - Throws error 404 if no data is found or you specify a page that doesn't exist. example: GET '/questions?page=1000'
    - Returns: An object with three keys: success, error, message.
        {
            'success': False,
            'error': 404,
            'message': "Not found"
        }


    2) GET '/categories/{category_id}/questions'
    - Throws error 404 if no data is found or you specify a page that doesn't exist duo to providing an invalid category id.
         example: GET '/categories/13/questions'
    - Returns: An object with three keys: success, error, message.
        {
            'success': False,
            'error': 404,
            'message': "Not found"
        }

    3) DELETE '/questions/{question_id}'
    - Throws error 404 if no question to delete duo to providing an invalid id.
         example: DELETE '/questions/558'
    - Returns: An object with three keys: success, error, message.
        {
            'success': False,
            'error': 404,
            'message': "Not found"
        }

    4) POST '/questions'
    - Throws error 400, 422. 400 if the data sent can't be parsed to json, 422 if the fields in the request body are invalid.
         example: POST: POST '/questions' , request body: 'post this question'   ---> throws 400 because the request body can't be parsed to JSON.
         example: POST: POST '/questions'' , request body: {'title": "Which pjanet in the solar system is the biggest?", ...}   ---> throws 422 because title in an invalid field.
    - Returns: An object with three keys: success, error, message.
        for 400:
            {
                'success': False,
                'error': 400,
                'message': "bad request"
            }
        for 422:
            {
                'success': False,
                'error': 422,
                'message': "please provide valid fields in your request body"
            }


    5) POST '/questions/search'
    - Throws error 400, 404. 400 if the data sent can't be parsed to json, 404 if no data found in the database.
         example: POST: POST '/questions/search' , request body: 'post this question'   ---> throws 400 because the request body can't be parsed to JSON.
         example: POST: POST '/questions/search' , request body: {'seatchTitle": "Foo"}  ---> throws 404 because no data is found.
    - Returns: An object with three keys: success, error, message.
        for 400:
            {
                'success': False,
                'error': 400,
                'message': "bad request"
            }
        for 404:
            {
                'success': False,
                'error': 404,
                'message': "Not found"
            }

    6) POST '/quizzes'
    - Throws error 400, 422. 400 if the data sent can't be parsed to json, 422 if the fields in the request body are invalid.
         example: POST: POST '/quizzes' , request body: 'post this question'   ---> throws 400 because the request body can't be parsed to JSON.
         example: POST: POST '/quizzes' , request body: {'title": "Which pjanet in the solar system is the biggest?", ...}   ---> throws 422 because title in an invalid field.
    - Returns: An object with three keys: success, error, message.
        for 400:
            {
                'success': False,
                'error': 400,
                'message': "bad request"
            }
        for 422:
            {
                'success': False,
                'error': 422,
                'message': "please provide valid fields in your request body"
            }
