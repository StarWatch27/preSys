from flask import Blueprint, request
import json
from src.services.AttackMethodService import AttackMethodService

"""
//////////////////////////////////////////
/////////////  攻击方法请求相关 ////////////
/////////////////////////////////////////
"""
prefix = "attackMethod"
attack_method_bp = Blueprint(prefix, __name__)
attackManager = AttackMethodService()


@attack_method_bp.route(f"/{prefix}/getById/<int:id>", methods=['GET'])
def getById(id):
    ds = attackManager.get_by_id(id).to_dict()
    return json.dumps(ds, indent=4)


@attack_method_bp.route(f"/{prefix}/getAll")
def getAll():
    ds = attackManager.get_all()
    return json.dumps(ds, indent=4)


@attack_method_bp.route(f"/{prefix}/add", methods=['POST'])
def add():
    name = request.json.get("name")
    succ = attackManager.add(name)
    return json.dumps({"succ": succ}, indent=4)


@attack_method_bp.route(f"/{prefix}/deleteById/<int:id>")
def deleteById(id):
    succ = attackManager.delete_by_id(id)
    return json.dumps({"succ": succ}, indent=4)
