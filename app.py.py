from flask import Flask, request, jsonify

app = Flask(__name__)

# Define an API endpoint for interacting with your Chrome extension
@app.route('/api/my_extension', methods=['POST'])
def my_extension():
    # Retrieve data from the request
    data = request.json

    # Extract relevant information from the data
    url = data['url']
    action = data['action']

    # Perform tasks based on the action
    if action == 'task1':
        # Perform task 1 for the given URL
        # (e.g., interact with a website, perform some operation)

        # Return a response
        response = {'message': 'Task 1 performed successfully for URL: {}'.format(url)}
        return jsonify(response)
    elif action == 'task2':
        # Perform task 2 for the given URL
        # (e.g., perform some other operation)

        # Return a response
        response = {'message': 'Task 2 performed successfully for URL: {}'.format(url)}
        return jsonify(response)
    else:
        # Return an error response if invalid action
        response = {'error': 'Invalid action'}
        return jsonify(response)

# Start the Flask development server
if __name__ == '__main__':
    app.run(debug=True)
