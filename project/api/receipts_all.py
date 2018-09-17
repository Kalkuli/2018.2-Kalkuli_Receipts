import os 
from flask import Flask, request, redirect, url_for, jsonify
from project import app

@app.route('/receipts_all', methods =['GET'])
def receipts_all:
    