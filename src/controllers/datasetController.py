from flask import Blueprint, request
import json
from src.services.DatasetService import DatasetService

"""
//////////////////////////////////////////
//////////////  数据库请求相关 /////////////
/////////////////////////////////////////
"""
dataset_bp = Blueprint('dataset', __name__)
datasetsManager = DatasetService()


@dataset_bp.route("/dataset/getDatasetById/<int:id>", methods=['GET'])
def getDatasetById(id):
    ds = datasetsManager.get_by_id(id).to_dict()
    return json.dumps(ds, indent=4)


@dataset_bp.route("/dataset/getAllDatasets")
def getAllDatasets():
    ds = datasetsManager.get_all()
    return json.dumps(ds, indent=4)


@dataset_bp.route("/dataset/addDataset", methods=['POST'])
def addDataset():
    name = request.json.get("name")  # 数据集名称
    abs_path = request.json.get("abs_path").strip()  # 路径
    succ = datasetsManager.add(name, abs_path)
    return json.dumps({"succ": succ}, indent=4)


@dataset_bp.route("/dataset/editDatasetById", methods=['POST'])
def editDatasetById():
    id = request.json.get("id")
    name = request.json.get("name")  # 数据集名称
    abs_path = request.json.get("abs_path").strip()  # 路径
    succ = datasetsManager.edit_by_id(id, name, abs_path)
    return json.dumps({"succ": succ}, indent=4)


@dataset_bp.route("/dataset/deleteDatasetById/<int:id>")
def deleteDatasetById(id):
    succ = datasetsManager.delete_by_id(id)
    return json.dumps({"succ": succ}, indent=4)
