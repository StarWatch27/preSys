from flask import Blueprint, request
import json
from src.services.DatasetService import DatasetService

"""
//////////////////////////////////////////
//////////////  数据库请求相关 /////////////
/////////////////////////////////////////
"""
prefix = "dataset"
dataset_bp = Blueprint(prefix, __name__)
datasetsManager = DatasetService()


@dataset_bp.route(f"/{prefix}/getById/<int:id>", methods=['GET'])
def getById(id):
    ds = datasetsManager.get_by_id(id).to_dict()
    return json.dumps(ds, indent=4)


@dataset_bp.route(f"/{prefix}/getAll")
def getAll():
    ds = datasetsManager.get_all()
    return json.dumps(ds, indent=4)


@dataset_bp.route(f"/{prefix}/add", methods=['POST'])
def add():
    name = request.json.get("name")  # 数据集名称
    abs_path = request.json.get("abs_path").strip()  # 路径
    succ = datasetsManager.add(name, abs_path)
    return json.dumps({"succ": succ}, indent=4)


@dataset_bp.route(f"/{prefix}/editById", methods=['POST'])
def editById():
    id = request.json.get("id")
    name = request.json.get("name")  # 数据集名称
    abs_path = request.json.get("abs_path").strip()  # 路径
    succ = datasetsManager.edit_by_id(id, name, abs_path)
    return json.dumps({"succ": succ}, indent=4)


@dataset_bp.route(f"/{prefix}/deleteById/<int:id>")
def deleteById(id):
    succ = datasetsManager.delete_by_id(id)
    return json.dumps({"succ": succ}, indent=4)
