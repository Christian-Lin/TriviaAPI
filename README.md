# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

This Trivia based API directly ties its backend in order to allow the frontend to:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. The file app.py contains all endpoints and models.py can be referenced for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server.

[View the README.md within ./frontend for more details.](./frontend/README.md)

## Quick Setup

### Frontend
- To start the frontend, while on the 'frontend' folder that contains the 'package.json' file, run:
```bash
npm install
npm start
```
This should open a browser window on [http://localhost:3000](http://localhost:3000) to view the frontend of the API

### Backend
- To initialize the backend server, first start a virtual environment to install dependencies:
```bash
source env/Scripts/activate
```
More details about virtual environment installation and setup can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
- Second, install requirements:
```bash
pip install -r requirements.txt
```
- Third, set up or restore the trivia database:
```bash
createdb -U <username> trivia
psql -U <username> trivia < trivia.psql
```
- And fourth, setup and run the Flask app:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
IMPORTANT: Windows users need to use 'set' instead of 'export'