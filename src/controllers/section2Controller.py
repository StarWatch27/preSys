import json
import os
import pickle
import random
import sys
import threading
import time
import subprocess

from flask import Blueprint, request
from src.services.FLDatasetService import FLDatasetService

import subprocess


prefix = "section3Api"
section3Api_bp = Blueprint(prefix, __name__)
fLDatasetService = FLDatasetService()


@section3Api_bp.route(f"/{prefix}/getAllModels", methods=['GET'])
def getAllModels():
    # """ 清空表"""
    # fLDatasetService.clear_table()
    #
    # """ 写入表"""
    # model_dir = "/home/xiongq_2023/proj/HJW/MyDL/data/Subjects"
    # models = []
    # for model_name in os.listdir(model_dir):
    #     if "mutant" in model_name or os.path.isfile(os.path.join(model_dir, model_name)):
    #         continue
    #     elif model_name in ["37624102", "50079585", "58237726", "59282996", "FacialKeypointsDetection",
    #                         "MovieReviews_Keras", "Traffic-Sign-Classifier", "gol_nn", "kaggle-melbourne_properties"]:
    #         continue
    #     else:
    #         models.append(model_name)
    # models = sorted(models)
    #
    #
    # for model in models:
    #     fLDatasetService.add(model,os.path.abspath(os.path.join(model_dir, model)))
    ds = fLDatasetService.get_all()
    return json.dumps(ds, indent=4)

@section3Api_bp.route(f"/{prefix}/getMutantRunDataByModelName", methods=['POST'])
def getMutantRunDataByModelName():
    time.sleep(1)
    # 模型名称
    name = request.json.get("body")['name']
    print(f"model_name:{name}")

    """ 检查是否已存在"""
    tgt_path = f"/home/xiongq_2023/proj/HJW/MyDL/codes/run_data/20241129_preSys/XY_{name}.pkl"
    if not os.path.exists(tgt_path) :
        print(f"模型’{name}‘的故障特征不存在：{tgt_path}！")
        return json.dumps({"result": "", "flag": "fail"}, indent=4)


    """ 获取随机50个数据，构造前端需要的数据格式"""
    with open(tgt_path, "rb") as f:
        dt = pickle.load(f)
    ids = random.Random(42).sample(range(len(dt)), 50)
    data = []
    for id in ids:
        vec_spm = dt[id]['X'][:30]
        vec_ast = dt[id]['X'][30:530]
        _vec_ecfg = dt[id]['X'][530:]
        vec_ecfg = [(_vec_ecfg[_ * 2], _vec_ecfg[_ * 2 + 1]) for _ in range(250)]
        data.append({
            "mutant_name": str(dt[id]['mutant_name']),
            "vec_ast": str(vec_ast),
            "vsc_ecfg": str(vec_ecfg),
            "vec_spm": str(vec_spm),
            "Y": str(dt[id]['Y'])

        })
    return json.dumps({"result": data}, indent=4)

@section3Api_bp.route(f"/{prefix}/genFeaturesByModelName", methods=['POST'])
def genFeaturesByModelName():
    time.sleep(1)
    # 模型名称
    model_name = request.json.get("body")['name']
    print(f"model_name:{model_name}")
    logs_dir = "/home/xiongq_2023/proj/HJW/preSys/logs/features_gen"

    """ 检查是否正在执行"""
    result = subprocess.check_output('ps -aux | grep "features_gen"', shell=True, stderr=subprocess.STDOUT)
    out = result.decode()
    for line in out.splitlines():
        if "features_gen" in line and model_name in line :
            print("线程已存在")
            return json.dumps({"result": "running", "data": line}, indent=4)

    """ 检查是否已存在"""
    tgt_path = f"/home/xiongq_2023/proj/HJW/MyDL/codes/run_data/20241129_preSys/XY_{model_name}.pkl"
    if os.path.exists(tgt_path) :
        print(f"故障特征已存在：{tgt_path}")
        return json.dumps({"result": "exists", "data": tgt_path}, indent=4)

    """ 生成"""
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    def run_feature_by_model_gen():
        process = subprocess.Popen([f"/home/xiongq_2023/anaconda3/envs/DeepFD/bin/python",
                                    f"/home/xiongq_2023/proj/HJW/MyDL/codes/APIs/features_gen.py",
                                    "-m", f"{model_name}"],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(f"{logs_dir}/gen_features_{model_name}.log", 'wb') as f:
            f.write(b'\n\n\n****************** NEW RUN ******************\n')
            for output in process.stdout:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                f.write((current_time + " - ").encode('utf-8') + output)
        return_code = process.wait()
        if return_code == 0:
            print("命令执行成功")
        else:
            print("命令执行出错，返回码:", return_code)
        print(process.stderr)
        print(process.stdout)

    thread = threading.Thread(target=run_feature_by_model_gen)
    thread.start()
    return json.dumps({"result": "start"}, indent=4)

@section3Api_bp.route(f"/{prefix}/genMutantPredsByModelName", methods=['POST'])
def genMutantPredsByModelName():
    time.sleep(1)
    # 模型名称
    model_name = request.json.get("body")['name']
    print(f"model_name:{model_name}")
    logs_dir = "/home/xiongq_2023/proj/HJW/preSys/logs/preds_gen"

    """ 检测故障特征是否存在"""
    tgt_path = f"/home/xiongq_2023/proj/HJW/MyDL/codes/run_data/20241129_preSys/XY_{model_name}.pkl"
    if not os.path.exists(tgt_path):
        print(f"故障特征不存在,请先生成！")
        return json.dumps({"result": "fail"}, indent=4)

    """ 检查是否正在执行"""
    result = subprocess.check_output('ps -aux | grep "preds_gen"', shell=True, stderr=subprocess.STDOUT)
    out = result.decode()
    for line in out.splitlines():
        if "preds_gen" in line and model_name in line:
            print("线程已存在")
            return json.dumps({"result": "running", "data": line}, indent=4)

    """ 检查是否已存在"""
    tgt_path = f"/home/xiongq_2023/proj/HJW/MyDL/codes/run_data/20241129_preSys/model_mutants_preds_{model_name}.pkl"
    if os.path.exists(tgt_path):
        print(f"故障预测结果已存在：{tgt_path}")
        return json.dumps({"result": "exists", "data": tgt_path}, indent=4)

    """ 生成"""
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    def run_preds_by_model_gen():
        process = subprocess.Popen([f"/home/xiongq_2023/anaconda3/envs/DeepFD/bin/python",
                                    f"/home/xiongq_2023/proj/HJW/MyDL/codes/APIs/preds_gen.py",
                                    "-m", f"{model_name}"],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(f"{logs_dir}/gen_preds_{model_name}.log", 'wb') as f:
            f.write(b'\n\n\n****************** NEW RUN ******************\n')
            for output in process.stdout:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                f.write((current_time + " - ").encode('utf-8') + output)
        return_code = process.wait()
        if return_code == 0:
            print("命令执行成功")
        else:
            print("命令执行出错，返回码:", return_code)
        print(process.stderr)
        print(process.stdout)

    thread = threading.Thread(target=run_preds_by_model_gen)
    thread.start()
    return json.dumps({"result": "start"}, indent=4)

@section3Api_bp.route(f"/{prefix}/getMutantPredsByModelName", methods=['POST'])
def getMutantPredsByModelName():
    time.sleep(1)
    # 模型名称
    name = request.json.get("body")['name']
    print(f"model_name:{name}")

    """ 检查是否已存在"""
    tgt_path = f"/home/xiongq_2023/proj/HJW/MyDL/codes/run_data/20241129_preSys/model_mutants_preds_{name}.pkl"
    if not os.path.exists(tgt_path) :
        print(f"模型’{name}‘的故障预测结果不存在：No {tgt_path}！")
        return json.dumps({"result": "", "flag": "fail"}, indent=4)

    """ 获取随机50个数据，构造前端需要的数据格式"""
    with open(tgt_path, "rb") as f:
        dt = pickle.load(f)
    ids = random.Random(42).sample(range(len(dt)), 50)
    data = [dt[id] for id in ids]
    return json.dumps({"result": data}, indent=4)

@section3Api_bp.route(f"/{prefix}/genMutantFLLogByModelName", methods=['POST'])
def genMutantFLLogByModelName():
    time.sleep(1)
    # 模型名称
    model_name = request.json.get("body")['name']
    print(f"model_name:{model_name}")
    logs_dir = "/home/xiongq_2023/proj/HJW/preSys/logs/fl_logs_gen"

    """ 检测故障特征是否存在"""
    tgt_path = f"/home/xiongq_2023/proj/HJW/MyDL/codes/run_data/20241129_preSys/XY_{model_name}.pkl"
    if not os.path.exists(tgt_path):
        print(f"故障特征不存在,请先生成！")
        return json.dumps({"result": "fail"}, indent=4)

    """ 检查是否正在执行"""
    result = subprocess.check_output('ps -aux | grep "fl_logs_gen"', shell=True, stderr=subprocess.STDOUT)
    out = result.decode()
    for line in out.splitlines():
        if "fl_logs_gen" in line and model_name in line:
            print("线程已存在")
            return json.dumps({"result": "running", "data": line}, indent=4)

    """ 检查是否已存在"""
    tgt_path = f"/home/xiongq_2023/proj/HJW/MyDL/codes/run_data/20241129_preSys/model_mutants_fl_logs_{model_name}.pkl"
    if os.path.exists(tgt_path):
        print(f"模型’{model_name}‘的故障定位结果已存在：{tgt_path}！")
        return json.dumps({"result": "exists", "data": tgt_path}, indent=4)

    """ 生成"""
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    def run_fl_log_by_model_gen():
        process = subprocess.Popen([f"/home/xiongq_2023/anaconda3/envs/DeepFD/bin/python",
                                    f"/home/xiongq_2023/proj/HJW/MyDL/codes/APIs/fl_logs_gen.py",
                                    "-m", f"{model_name}"],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(f"{logs_dir}/gen_fl_logs_{model_name}.log", 'wb') as f:
            f.write(b'\n\n\n****************** NEW RUN ******************\n')
            for output in process.stdout:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                f.write((current_time + " - ").encode('utf-8') + output)
        return_code = process.wait()
        if return_code == 0:
            print("命令执行成功")
        else:
            print("命令执行出错，返回码:", return_code)
        print(process.stderr)
        print(process.stdout)

    thread = threading.Thread(target=run_fl_log_by_model_gen)
    thread.start()
    return json.dumps({"result": "start"}, indent=4)

@section3Api_bp.route(f"/{prefix}/getMutantFLLogByModelName", methods=['POST'])
def getMutantFLLogByModelName():
    time.sleep(1)
    # 模型名称
    model_name = request.json.get("body")['name']
    print(f"model_name:{model_name}")

    """ 检查是否已存在"""
    tgt_path = f"/home/xiongq_2023/proj/HJW/MyDL/codes/run_data/20241129_preSys/model_mutants_fl_logs_{model_name}.pkl"
    if not os.path.exists(tgt_path) :
        print(f"模型’{model_name}‘的故障定位结果不存在：No {tgt_path}！")
        return json.dumps({"result": "", "flag": "fail"}, indent=4)

    """ 获取随机50个数据，构造前端需要的数据格式"""
    with open(tgt_path, "rb") as f:
        dt = pickle.load(f)
    ids = random.Random(42).sample(range(len(dt)), 50)
    data = [dt[id] for id in ids]
    print(data[1])
    return json.dumps({"result": data}, indent=4)
