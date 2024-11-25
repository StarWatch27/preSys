from flask import Blueprint, request
import json
from src.services.AttentionModelService import AttentionModelService

"""
//////////////////////////////////////////
////////////  注意力模型请求相关 ////////////
/////////////////////////////////////////
"""
prefix = "attentionModel"
attention_model_bp = Blueprint(prefix, __name__)
attentionModelService = AttentionModelService()


@attention_model_bp.route(f"/{prefix}/getById/<int:id>", methods=['GET'])
def getById(id):
    ds = attentionModelService.get_by_id(id).to_dict()
    return json.dumps(ds, indent=4)


@attention_model_bp.route(f"/{prefix}/getAll")
def getAll():
    ds = attentionModelService.get_all()
    return json.dumps(ds, indent=4)


@attention_model_bp.route(f"/{prefix}/add", methods=['POST'])
def add():
    name = request.json.get("name")
    abs_path = request.json.get("abs_path").strip()  # 路径
    succ = attentionModelService.add(name, abs_path)
    return json.dumps({"succ": succ}, indent=4)

@attention_model_bp.route(f"/{prefix}/editById", methods=['POST'])
def editDatasetById():
    id = request.json.get("id")
    name = request.json.get("name")  # 名称
    abs_path = request.json.get("abs_path").strip()  # 路径
    succ = attentionModelService.edit_by_id(id, name, abs_path)
    return json.dumps({"succ": succ}, indent=4)

@attention_model_bp.route(f"/{prefix}/deleteById/<int:id>")
def deleteById(id):
    succ = attentionModelService.delete_by_id(id)
    return json.dumps({"succ": succ}, indent=4)
