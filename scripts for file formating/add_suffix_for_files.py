# -*- coding: UTF-8 -*-
import os
import sys
# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 如果当前目录是 'useful_scripts'，将当前目录加入搜索路径，否则，将父目录加入搜索路径
if os.path.basename(script_dir) == 'useful_scripts':
    sys.path.append(script_dir)
else:
    parent_dir = os.path.dirname(script_dir)
    sys.path.append(parent_dir)
# 导入其他模块
import shutil
import logging
import time
from local_modules.local_functions import configure_logging
from local_modules.local_functions import add_timestamp

log_file_path = ''
configure_logging(log_file_path)

# 记录日志信息
logging.info('程序开始运行')


filenames_without_suffix = [
"25-5-1956", "AAAAA-《风洞结构设计》-刘政崇", "AAAAA-《国外风洞试验》", "AAAAA-5-1983_G-ASPL_Append", "AAAAA-07_040", "AAAAA-254", "AAAAA-444", "AAAAA-503", "AAAAA-594", "AAAAA-718", "AAAAA-1947_Vol1_No1", "AAAAA-87920main_H-1079", "AAAAA-87933main_AIAA812475", "AAAAA-88071main_H-1214", "AAAAA-88290main_H-1894", "AAAAA-00195182", "AAAAA-00557425", "AAAAA-0627441_Miniature_Pressure_Transducers", "AAAAA-6185535D1E4EE6CDDD36142EC501C91B.freisthler-statement", "AAAAA-A_D-风洞测试0416CN", "AAAAA-AeroLabWindTun_Operator", "AAAAA-AFD-100929-006", "AAAAA-AIOLOS-Job-Posting", "AAAAA-Application for tax Incentives - Calspan 2020", "AAAAA-AR_FR_2010", "AAAAA-B 3-03", "AAAAA-BART Stability Study Compressed_0", "AAAAA-Bottom-upReview", "AAAAA-Calculating", "AAAAA-Chapter 17 Student Handout Answers", "AAAAA-CIA-RDP85T00313R000300040006-1", "AAAAA-Class23_Ex2_old", "AAAAA-conf_poster", "AAAAA-Construction of Numerical Wind Tunnel on the e-Science Infrastructure", "AAAAA-declass_fy12_1959_01_15", "AAAAA-digidepo_8615945_po_e331044", "AAAAA-DOC_0000254288", "AAAAA-EGSR-40th-Anniversary", "AAAAA-Engineering Directorate Presentation", "AAAAA-FFFSCR97", "AAAAA-FlightTest", "AAAAA-FULL BROCHURE - Shang Salcedo Place", "AAAAA-HW_3", "AAAAA-ICAS-82-5.7.2", "AAAAA-ICAS-94-0.5", "AAAAA-ICAS-94-3.1.4", "AAAAA-ICAS-1996-3.3.2", "AAAAA-Intercom+March+84+-+HSWT+20000th+Run+++Silver+Jubilee[1]", "AAAAA-jenkins_playgroud-_supporting_documentation", "AAAAA-JV1N2P5-StJohn", "AAAAA-Manual of CWOs - 1965", "AAAAA-Mitsubishi", "AAAAA-Mitsubishi_Heavy_Industries-2-17-04-BM", "AAAAA-mitsubishi-vrf-system", "AAAAA-New-ICAT-Overall-Brochure-1", "AAAAA-notice-17-jan-18", "AAAAA-OUIT WindTunnel", "AAAAA-P3253", "AAAAA-Pope_Goin_1965", "AAAAA-PREM19-1411", "AAAAA-Race_Car_Aerodynamics-Joseph Katz-1st Edition", "AAAAA-rep460", "AAAAA-rep492", "AAAAA-RNCBW_USABWP", "AAAAA-robi_01", "AAAAA-spc_mccg_000025_000059", "AAAAA-Technical-Report-11-Wind-Tunnel-Research-on-Low-Rise-Buildings", "AAAAA-Technical-Report-38-Simulation-of-Cyclonic-Wind-Forces-on-Roof-Claddings-By-Random-Block-Load-Testing", "AAAAA-Togami_k_1993", "AAAAA-UTAls1968", "AAAAA-VERTEX_ML_Performance_final", "AAAAA-Villain_France", "AAAAA-VRF-2019", "AAAAA-Wind Tunnel Performance Data for Two- and Three-Bucket Savonius Rotors", "AAAAA-Wind-tunnels", "AAAAA-风洞结构设计-刘政崇", "AAAAA-现代战斗机非定常空气动力学及其风洞实验研究_孙海生", "plastics-in-defense-safety", "AAAAA-低噪声风洞设计研究", "AAAAA-jh_fgh_firstfloor_evacplan", 
]


def add_pdf(filenames):
    result = []
    for i in filenames:
        result.append(f"{i}.pdf")
    return result


def add_doc(filenames):
    result = []
    for i in filenames:
        result.append(f"{i}.doc")
    return result


def add_docx(filenames):
    result = []
    for i in filenames:
        result.append(f"{i}.docx")
    return result


def add_txt(filenames):
    result = []
    for i in filenames:
        result.append(f"{i}.txt")
    return result


# results = add_doc(filenames_without_suffix)

# results = add_docx(filenames_without_suffix)

# results = add_pdf(filenames_without_suffix)

# results = add_txt(filenames_without_suffix)

results = add_pdf(filenames_without_suffix) + add_txt(filenames_without_suffix)

# results = add_doc(filenames_without_suffix) + add_docx(filenames_without_suffix) + add_txt(filenames_without_suffix)

# results = add_doc(filenames_without_suffix) + add_docx(filenames_without_suffix) + add_pdf(filenames_without_suffix) + add_txt(filenames_without_suffix)


file_name = "names.txt"
file_name = add_timestamp(file_name)


file_name = os.path.join("H:\\", file_name)

with open(file_name, 'w', encoding='utf8') as f:
    for i in results:
        print(f"\"{i}\", ")
        f.write(f"\"{i}\", ")

