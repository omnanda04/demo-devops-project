from flask import Blueprint, jsonify


main = Blueprint("main", __name__)


@main.get("/")
def index():
    return jsonify(message="Welcome to demo-devops-project")


@main.get("/health")
def health():
    return jsonify(status="ok")


@main.get("/api/info")
def info():
    return jsonify(name="demo-devops-project", version="0.1.0")
