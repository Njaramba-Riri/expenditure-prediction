from flask import Flask, url_for, jsonify, requests

app= Flask()

@app.post("/predict")
def predict():
    
