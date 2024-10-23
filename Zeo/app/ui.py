# app/ui.py
from flask import render_template, request, redirect , flash,session,Flask
from app import app, SessionLocal
from app.models import Rule
from app.ast_logic import create_rule, combine_rules, Node
import json
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
# Establish a session for database interaction
db_session = SessionLocal()

@app.route('/')
def home():
    # Fetch all rules from the database
    rules = db_session.query(Rule).all()
    return render_template('index.html', rules=rules)


# @app.route('/add_rule', methods=['POST'])
# def add_rule():
#     rule_name = request.form.get('rule_name')
#     rule_string = request.form.get('rule_string')
    
#     # Generate the AST for the rule
#     rule_ast = create_rule(rule_string)

#     # Store the rule in the database
#     new_rule = Rule(
#         rule_name=rule_name,
#         rule_string=rule_string,
#         rule_ast=json.dumps(rule_ast, default=lambda o: o.__dict__)
#     )
#     db_session.add(new_rule)
#     db_session.commit()

#     return redirect('/')

# @app.route('/add_rule', methods=['POST'])
# def add_rule():
#     rule_name = request.form.get('rule_name')
#     rule_string = request.form.get('rule_string')

#     try:
#         # Try to generate the AST for the rule
#         rule_ast = create_rule(rule_string)

#         # If successful, store the rule in the database
#         new_rule = Rule(
#             rule_name=rule_name,
#             rule_string=rule_string,
#             rule_ast=json.dumps(rule_ast, default=lambda o: o.__dict__)
#         )
#         db_session.add(new_rule)
#         db_session.commit()

#         # Redirect to the home page after successful addition
#         return redirect('/')

#     except Exception as e:
#         # Handle errors and display a clean error message
#         error_message = "Invalid rule string. Please check the syntax and try again."
#         # Optionally, log the full error message to the server for debugging
#         app.logger.error(f"Error creating rule: {str(e)}")
        
#         # Render the home page again but with the error message
#         rules = db_session.query(Rule).all()
#         return render_template('index.html', rules=rules, error_message=error_message)

@app.route('/add_rule', methods=['POST'])
def add_rule():
    rule_name = request.form.get('rule_name')
    rule_string = request.form.get('rule_string')

    try:
        # Try to generate the AST for the rule
        rule_ast = create_rule(rule_string)

        # If successful, store the rule in the database
        new_rule = Rule(
            rule_name=rule_name,
            rule_string=rule_string,
            rule_ast=json.dumps(rule_ast, default=lambda o: o.__dict__)
        )
        db_session.add(new_rule)
        db_session.commit()

        # Redirect to the home page after successful addition
        return redirect('/')

    except Exception as e:
        # Handle errors and display a clean error message
        add_rule_error = "Invalid rule string. Please check the syntax and try again."
        app.logger.error(f"Error creating rule: {str(e)}")
        
        # Render the home page again but with the error message
        rules = db_session.query(Rule).all()
        return render_template('index.html', rules=rules, add_rule_error=add_rule_error)



def node_from_dict(data):
    """
    Helper function to map the JSON dictionary back to a Node object.
    Maps 'type' in JSON to 'node_type' in Node class.
    """
    if 'type' in data:
        node_type = data.pop('type')  # Extract 'type' from JSON and map it to 'node_type'
        return Node(node_type=node_type, **data)  # Use the remaining keys as other arguments
    return data

# @app.route('/evaluate_rule', methods=['POST'])
# def evaluate_rule():
#     # Get the user data in JSON format
#     user_data = json.loads(request.form.get('data'))

#     # Fetch all rules from the database
#     rules = db_session.query(Rule).all()

#     if not rules:
#         return "No rules found to evaluate!"

#     # Combine the rule ASTs
#     combined_ast = None

#     for rule in rules:
#         rule_ast = json.loads(rule.rule_ast, object_hook=node_from_dict)
#         if combined_ast is None:
#             combined_ast = rule_ast
#         else:
#             combined_ast = Node('operator', left=combined_ast, right=rule_ast, value='AND')

#     # Evaluate the combined AST with the provided user data
#     result = combined_ast.evaluate(user_data)

#     return f"Evaluation Result: {result}"

# For Error Handling
# @app.route('/evaluate_rule', methods=['POST'])
# def evaluate_rule():
#     # Get the user data in JSON format
#     try:
#         user_data = json.loads(request.form.get('data'))
#     except json.JSONDecodeError as e:
#         return render_template('index.html', rules=db_session.query(Rule).all(), error="Invalid JSON format: " + str(e))

#     # Fetch all rules from the database
#     rules = db_session.query(Rule).all()

#     if not rules:
#         return render_template('index.html', rules=rules, error="No rules found to evaluate!")

#     try:
#         # Combine and evaluate the rule ASTs
#         combined_ast = None
#         for rule in rules:
#             rule_ast = json.loads(rule.rule_ast, object_hook=node_from_dict)
#             if combined_ast is None:
#                 combined_ast = rule_ast
#             else:
#                 combined_ast = Node('operator', left=combined_ast, right=rule_ast, value='AND')

#         result = combined_ast.evaluate(user_data)
#     except Exception as e:
#         # Catch any other evaluation errors
#         return render_template('index.html', rules=rules, error=f"Error during evaluation: {e}")

#     return render_template('result.html', result=result)


# @app.route('/evaluate_rule', methods=['POST'])
# def evaluate_rule():
#     try:
#         # Get the user data in JSON format from the form
#         user_data = json.loads(request.form.get('data'))

#         # Fetch all rules from the database
#         rules = db_session.query(Rule).all()

#         if not rules:
#             return "No rules found to evaluate!"

#         # Combine the rule ASTs
#         combined_ast = None
#         for rule in rules:
#             rule_ast = json.loads(rule.rule_ast, object_hook=node_from_dict)
#             if combined_ast is None:
#                 combined_ast = rule_ast
#             else:
#                 combined_ast = Node('operator', left=combined_ast, right=rule_ast, value='AND')

#         # Evaluate the combined AST with the provided user data
#         result = combined_ast.evaluate(user_data)

#         return f"Evaluation Result: {result}"

#     except json.JSONDecodeError as e:
#         error_message = "Invalid user data format. Please provide valid JSON."
#         app.logger.error(f"Error parsing user data: {str(e)}")
#     except Exception as e:
#         error_message = "An error occurred during rule evaluation. Please check the rule or user data."
#         app.logger.error(f"Evaluation error: {str(e)}")

#     # If an error occurs, render the UI with the error message
#     rules = db_session.query(Rule).all()
#     return render_template('index.html', rules=rules, error_message=error_message)

@app.route('/delete_rule/<int:rule_id>', methods=['POST'])
def delete_rule(rule_id):
    try:
        rule_to_delete = db_session.query(Rule).get(rule_id)
        if rule_to_delete:
            db_session.delete(rule_to_delete)
            db_session.commit()
            flash('Rule deleted successfully', 'success')
        else:
            flash('Rule not found', 'error')
    except Exception as e:
        app.logger.error(f"Error deleting rule: {str(e)}")
        flash('An error occurred while deleting the rule.', 'error')

    return redirect('/')

@app.route('/update_rule/<int:rule_id>', methods=['GET'])
def update_rule_form(rule_id):
    rule_to_update = db_session.query(Rule).get(rule_id)
    if not rule_to_update:
        flash('Rule not found', 'error')
        return redirect('/')

    return render_template('update_rule.html', rule=rule_to_update)

@app.route('/update_rule/<int:rule_id>', methods=['POST'])
def update_rule(rule_id):
    rule_name = request.form.get('rule_name')
    rule_string = request.form.get('rule_string')

    try:
        rule_ast = create_rule(rule_string)
        rule_to_update = db_session.query(Rule).get(rule_id)
        if rule_to_update:
            rule_to_update.rule_name = rule_name
            rule_to_update.rule_string = rule_string
            rule_to_update.rule_ast = json.dumps(rule_ast, default=lambda o: o.__dict__)
            db_session.commit()
            flash('Rule updated successfully', 'success')
        else:
            flash('Rule not found', 'error')
    except Exception as e:
        app.logger.error(f"Error updating rule: {str(e)}")
        flash('An error occurred while updating the rule.', 'error')

    return redirect('/')




@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    try:
        # Get the user data in JSON format from the form
        user_data = json.loads(request.form.get('data'))

        # Fetch all rules from the database
        rules = db_session.query(Rule).all()

        if not rules:
            return "No rules found to evaluate!"

        # Combine the rule ASTs
        combined_ast = None
        for rule in rules:
            rule_ast = json.loads(rule.rule_ast, object_hook=node_from_dict)
            if combined_ast is None:
                combined_ast = rule_ast
            else:
                combined_ast = Node('operator', left=combined_ast, right=rule_ast, value='AND')

        # Evaluate the combined AST with the provided user data
        result = combined_ast.evaluate(user_data)

        # return f"Evaluation Result: {result}"
        return render_template('result.html', result=result)

    except json.JSONDecodeError as e:
        evaluate_rule_error = "Invalid user data format. Please provide valid JSON."
        app.logger.error(f"Error parsing user data: {str(e)}")
    except Exception as e:
        evaluate_rule_error = "An error occurred during rule evaluation. Please check the rule or user data."
        app.logger.error(f"Evaluation error: {str(e)}")

    # If an error occurs, render the UI with the error message
    rules = db_session.query(Rule).all()
    return render_template('index.html', rules=rules, evaluate_rule_error=evaluate_rule_error)
