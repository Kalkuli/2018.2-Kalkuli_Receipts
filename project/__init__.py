import os
from flask import Flask, jsonify

# Instantiate the app
app	=	Flask(__name__)

# Set Configuration
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

@app.route('/',	methods=['GET'])
def	ping_pong():
	return	jsonify({
		'data':	'Welcome to Kalkuli Receipts Service'
	})