from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Store chat messages in memory (replace with a database in a production app)
messages = []

# Replace this with your actual n8n webhook URL
n8n_webhook_url = 'http://16.16.104.13:5678/webhook-test/b1be6c20-a827-4bfc-b719-f0b560df21ae'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    if request.is_json:
        user_message = request.json['message']
        
        # Send the user's message to n8n
        try:
            n8n_response = requests.post(n8n_webhook_url, json={'message': user_message})
            if n8n_response.ok:
                n8n_data = n8n_response.json()
                response_message = n8n_data.get('response', 'No response from assistant')
                # Append the n8n response to the messages list
                messages.append({'user': user_message, 'response': response_message})
            else:
                response_message = "Error communicating with assistant"
        except requests.RequestException as e:
            response_message = f"An error occurred: {e}"
        
        return jsonify({'response': response_message})
    
    return 'Unsupported Media Type', 415


@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)
