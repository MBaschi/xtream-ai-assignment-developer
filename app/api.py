
from flask import Blueprint, request
from utils import load_model
api_bp = Blueprint('api', __name__)

@api_bp.route('/predict_price', methods=['GET'])
def predict_diamon_price(request):
    input_data = request.get("input_data")
    model = request.get("model")
    load_model(model)

@api_bp.route('/similar_diamonds', methods=['GET'])
def find_similar_diamonds():
    # Logic for API 2
    return "Response from API 2"
