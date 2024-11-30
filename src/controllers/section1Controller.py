import json
import os
import threading
import time

from flask import Blueprint, request
import subprocess

prefix = "section1Api"
section1Api_bp = Blueprint(prefix, __name__)


@section1Api_bp.route(f"/{prefix}/genAdvDataset", methods=['POST'])
def genAdvDataset():
    time.sleep(1)
    recipe = request.json.get("body")
    model_type = recipe["model"]
    raw_dataset_name = recipe["dataset"]
    atk_method = recipe["atk_method"]
    csv_dir = "/home/xiongq_2023/proj/HJW/TPGD/HJW/adv_csvs"
    dataset_dir = "/home/xiongq_2023/proj/HJW/TPGD/HJW/datasets_tmp"
    logs_dir = "/home/xiongq_2023/proj/HJW/preSys/logs"

    """ 检查是否正在执行"""
    result = subprocess.check_output('ps -aux | grep "adv_gen"', shell=True, stderr=subprocess.STDOUT)
    out = result.decode()
    for line in out.splitlines():
        if model_type in line and atk_method in line and raw_dataset_name in line:
            print("线程已存在")
            return json.dumps({"result": "running", "data": line}, indent=4)



    """ 检查是否已存在"""
    tgt_csv_path = f"{csv_dir}/{model_type}-{raw_dataset_name}-{atk_method}-log.csv"
    tgt_dataset_path = f"{dataset_dir}/{model_type}-{raw_dataset_name}-{atk_method}"
    if os.path.exists(tgt_csv_path) and os.path.exists(tgt_dataset_path):
        print(f"对抗样本已存在：{tgt_csv_path}")
        return json.dumps({"result": "exists","data":tgt_dataset_path}, indent=4)


    """ 生成"""
    def run_adv_gen():

        process = subprocess.Popen([f"/home/xiongq_2023/anaconda3/envs/TPGD/bin/python",
                                    f"/home/xiongq_2023/proj/HJW/TPGD/HJW/APIs/adv_gen.py",
                                    "-m", f"{model_type}",
                                    "-d", f"{raw_dataset_name}",
                                    "-a", f"{atk_method}",
                                    "--csv_dir", f"{csv_dir}",
                                    "--dataset_dir", f"{dataset_dir}"],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(f"{logs_dir}/adv_gen/{model_type}-{raw_dataset_name}-{atk_method}.log", 'wb') as f:
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

    thread = threading.Thread(target=run_adv_gen)
    thread.start()
    return json.dumps({"result": "start"}, indent=4)

@section1Api_bp.route(f"/{prefix}/genFocus", methods=['POST'])
def genFocus():
    time.sleep(1)
    recipe = request.json.get("body")
    model_type = recipe["model"]
    raw_dataset_name = recipe["dataset"]
    atk_method = recipe["atk_method"]
    attns_dir = "/home/xiongq_2023/proj/HJW/TPGD/HJW/pair_attns/20241129_trace_preSys/0"
    focus_dir = "/home/xiongq_2023/proj/HJW/TPGD/HJW/focus_trace/20241129_trace_preSys/0_entropy"
    logs_dir = "/home/xiongq_2023/proj/HJW/preSys/logs"

    """ 检查是否正在执行"""
    result = subprocess.check_output('ps -aux | grep "focus_gen"', shell=True, stderr=subprocess.STDOUT)
    out = result.decode()
    for line in out.splitlines():
        if model_type in line and atk_method in line and raw_dataset_name in line:
            print("线程已存在")
            return json.dumps({"result": "running", "data": line}, indent=4)

    """ 检查是否已存在"""
    attns_file_name = f"{model_type}-{raw_dataset_name}-{atk_method}-ori-adv-pair-attns-dict.pkl"
    focus_file_name = f"{model_type}-{raw_dataset_name}-{atk_method}-ori-adv-focus-trace.pkl"
    tgt_attns_path = f"{attns_dir}/{attns_file_name}"
    tgt_focus_path = f"{focus_dir}/{focus_file_name}"
    if os.path.exists(tgt_attns_path) and os.path.exists(tgt_focus_path):
        print(f"Focus已存在：{tgt_focus_path}")
        return json.dumps({"result": "exists", "data": tgt_focus_path}, indent=4)


    """ 开始计算Focus"""
    def run_focus_gen():
        process = subprocess.Popen([f"/home/xiongq_2023/anaconda3/envs/TPGD/bin/python",
                                    f"/home/xiongq_2023/proj/HJW/TPGD/HJW/APIs/focus_gen.py",
                                    "-m", f"{model_type}",
                                    "-d", f"{raw_dataset_name}",
                                    "-a", f"{atk_method}"],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(f"{logs_dir}/focus_gen/{model_type}-{raw_dataset_name}-{atk_method}.log", 'wb') as f:
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

    thread = threading.Thread(target=run_focus_gen)
    thread.start()
    return json.dumps({"result": "start"}, indent=4)


@section1Api_bp.route(f"/{prefix}/advDetect", methods=['POST'])
def advDetect():
    time.sleep(1)
    recipe = request.json.get("body")
    model_type = recipe["model"]
    raw_dataset_name = recipe["dataset"]
    atk_method = recipe["atk_method"]
    ml_model_dir = "/home/xiongq_2023/proj/HJW/TPGD/HJW/ml_models/20241129_trace_preSys/0_entropy"
    logs_dir = "/home/xiongq_2023/proj/HJW/preSys/logs"
    log_path = f"{logs_dir}/adv_detect/{model_type}-{raw_dataset_name}-{atk_method}.log"

    """ 检查是否正在执行"""
    result = subprocess.check_output('ps -aux | grep "adv_detect"', shell=True, stderr=subprocess.STDOUT)
    out = result.decode()
    for line in out.splitlines():
        if model_type in line and atk_method in line and raw_dataset_name in line:
            print("线程已存在")
            return json.dumps({"result": "running", "data": line}, indent=4)

    """ 检查是否已存在"""
    model_name = f"{model_type}-{raw_dataset_name}-{atk_method}.pkl"  # 是否存在训练好的模型
    ml_model_path = f"{ml_model_dir}/{model_name}"
    if os.path.exists(ml_model_path):
        print(f"检测模型已存在：{ml_model_path}")

        def rtn_data_1():
            with open(log_path, "rb") as f:
                content = f.readlines()[-1].strip().decode('utf-8')
            f1, auc, acc = content.split(" ")[-3:]
            strr = f"f1:{float(f1):.2%}, auc:{float(auc):.2%}, acc:{float(acc):.2%}"
            rtn_data = f"{strr}"
            return rtn_data

        rtn_data = rtn_data_1()
        print(rtn_data)
        return json.dumps({"result": "exists", "data": rtn_data}, indent=4)


    """ 开始执行"""
    def run_focus_gen():
        process = subprocess.Popen([f"/home/xiongq_2023/anaconda3/envs/TPGD/bin/python",
                                    f"/home/xiongq_2023/proj/HJW/TPGD/HJW/APIs/adv_detect.py",
                                    "-m", f"{model_type}",
                                    "-d", f"{raw_dataset_name}",
                                    "-a", f"{atk_method}"],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(log_path, 'wb') as f:
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

    thread = threading.Thread(target=run_focus_gen)
    thread.start()
    return json.dumps({"result": "start"}, indent=4)
