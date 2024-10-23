# Rule Engine Application

This is a web-based Rule Engine application that allows users to create, update, evaluate, and delete rules based on user-defined conditions. It uses PostgreSQL for data storage and provides a simple UI for rule management.

## Features
- **Add New Rules:** Users can create rules by providing a name and a rule string, which is converted to an Abstract Syntax Tree (AST) for evaluation.
- **View Rules:** Displays a list of all existing rules in the database.
- **Update Rules:** Users can update the rule name and rule string using the update functionality.
- **Delete Rules:** Users can delete existing rules.
- **Evaluate Rules:** Rules can be evaluated based on user-provided conditions.

## Technologies Used
- **Backend:** Python (Flask framework)
- **Frontend:** HTML, CSS (for basic styling)
- **Database:** PostgreSQL
- **AST Parsing:** Custom logic for parsing rule strings into ASTs

## Project Structure

```bash
app/
│
├── static/
│   └── styles.css          # CSS file for styling the UI
├── templates/
│   ├── index.html          # Main UI template for rule management
│   └── update_rule.html    # Form to update an existing rule
├── create_tables.py        # Script for creating the PostgreSQL 'rule' table
├── ui.py                   # Flask app to handle routes and logic for CRUD operations
├── config.py               # Configuration file for database connection
└── rule_engine.py          # Logic for rule parsing and AST generation
```
## Database Schema

The application uses PostgreSQL with the following schema for the rule table:

| Column      | Type            | Constraints               |
|-------------|-----------------|---------------------------|
| id          | SERIAL           | Primary Key               |
| rule_name   | VARCHAR(100)     | Not Null                  |
| rule_string | VARCHAR(200)     | Not Null                  |
| rule_ast    | JSON             | Not Null (AST structure)  |

## API Endpoints
- **GET /**: Home page to view and manage rules.
- **POST /add_rule**: Add a new rule to the database.
- **GET /update_rule/<id>**: Fetch the rule to be updated by ID.
- **POST /update_rule/<id>**: Update the rule with new values.
- **POST /delete_rule/<id>**: Delete a rule by its ID.



## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/rule-engine.git
   cd rule-engine
   ```
2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up PostgreSQL and create the rule_engine_db:**
   ```bash
   CREATE DATABASE rule_engine_db;
   ```
4. **Update the database connection string in config.py:**
   ```bash
   DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/rule_engine_db'
   ```
5. **Run the script to create the required table:**
   ```bash
   python create_tables.py
   ```
6. **Start the Flask app:**
   ```bash
   python run.py
   ```
7. **Access the app at**
    ``` http://127.0.0.1:5000/ ```

## Screenshots

### Add Rule
![Add Rule](path/to/add_success.png)
*This screenshot shows the successful addition of a new rule.*

### Update Rule
![Update Rule](path/to/update_success.png)
*This screenshot displays the successful update of an existing rule.*

### Delete Rule
![Delete Rule](path/to/delete_success.png)
*This screenshot confirms that a rule has been successfully deleted.*

### Evaluate Rule
![Evaluate Rule](path/to/evaluation_success.png)
*This screenshot illustrates the successful evaluation of a rule.*

