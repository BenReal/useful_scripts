import os
import pandas as pd
from datetime import datetime

# 配置目录和要读取的文件名称
directory = r'H:\《XXXX》《XXXX》2023年10月27日\词频2023年12月13日'
filename = '词频_无人系统V2.xlsx'

# 读取原始Excel文件
file_path = os.path.join(directory, filename)
df = pd.read_excel(file_path)


# 定义门限值字典
thresholds = {"Unmanned Aerial Vehicle" : 1, 
"UAV" : 5, 
"Unmanned Aircraft Systems" : 1, 
"UAS" : 5, 
"Drone" : 5, 
"unmanned surface vehicle" : 1, 
"unmanned surface vessel" : 1, 
"USV" : 5, 
"unmanned underwater vehicle" : 1, 
"UUV" : 5, 
"Unmanned ground vehicle" : 1, 
"UGV" : 5, 
"artificial intelligence" : 1, 
"C4ISR" : 3, 
"electronic war" : 3, }

# thresholds = {"laser weapon":1, "missile":1, "Hypersonic":1, "High Supersonic":1, "Supersonic":1, "High.{0,1}energy laser":1, "Chemical laser weapon":1, "Solid-state laser weapon":1, "Free-electron laser":1, "Beam control transmission":1, "Strong laser atmospheric transmission":1, "High-efficiency damage":1, "Laser synthesis technology research":1, "High-efficiency thermal management technology research":1, "Adaptive optics":1, "airforce laser weapon":1, "HEL-LADS":1, "ALTB":1, "AHEL":1, "KRET":1, "SHIELD":1, "Navy laser weapon":1, "SSL-TM":1, "RHEL":1, "ODIN":1, "SNLWS":1, "HELIOS":1, "NFLoS":1, "LaWS":1, "CLWS":1, "HELCAP":1, "NLFoS":1, "ASCM":1, "ASBM":1, "Army laser weapon":1, "HEMTT":1, "MEHEL":1, "HELWS":1, "HEL-TVD":1, "ATHENA":1, "CLAWS":1, "C-UAS HELWS":1, "HELSI":1, "IFPC-HEL":1, "THEL":1, "JHPSSL":1, "HELLADS":1, "RELI":1, "HELMTT":1, "HELTVD":1, "MMHEL":1, "BMDS":1, "DEM-SHORAN":1, "Stryker":1, "M-SHORAN":1, "Gray Wolf":1, "HOPLITE":1, "MSET":1, "FlexiS":1, "MMT":1, "MAD-FIRES":1, "MHTK":1, "Pike":1, "SM-3":1, "JASSM":1, "TACTOM":1, "LRASM":1, "Циркон":1, "Сармат":1, "Калибр":1, "Триумф":1, "Aster":1, "Meteor":1, "Stormshadow":1, "KEPD 350":1, "Python-5":1, "Iron Dome":1, "A-Darter":1, "Brahmos":1, "AGM-129":1, "AGM-158":1, "AIM-260":1, "Kh-101":1, "Kh-31P":1, "Kh-58":1, "KH-59MK2":1, "NSM":1, "S-500":1, "SCALP/MdCN":1, "NASAMS":1, "SAMP/T":1, "JNAAM":1, "HARM":1, "AARGM ER":1, "ARMIGER":1, "THAAD":1, "GMD":1, "MEADS":1, "Rapier":1, "Starstreak/laser":1, "FLAADS":1, "David's Sling":1, "Arrow":1, "FCAAM":1, "MICA NG":1, "PrSM":1, "LRHW":1, "GBSD":1, "HAWC":1, "ARRW":1, "Peregrine":1, "AARGM":1, "NGLAW":1, "CPS":1, "NGI":1, "GPI":1, "Kinzhal hypersonic cruise missile":1, "BrahMos cruise missile":1, "PL-12 air-to-air missile":1, "C-802 anti-ship cruise missile":1, "YJ-12 supersonic anti-ship cruise missile":1, "DF-17 hypersonic glide vehicle":1, "Kalibr cruise missile":1, "Hsiung Feng III cruise missile":1, "Exocet anti-ship missile":1, "Tomahawk cruise missile":1, "Patriot surface-to-air missile system":1, "Standard Missile 3":1, "THAAD (Terminal High Altitude Area Defense) missile system":1, "SAMP/T (Sol-Air Moyenne Portée Terrestre) air defense system":1, "Pantsir-S1 air defense system":1, "S-300 surface-to-air missile system":1, "Astra BVRAAM (Beyond Visual Range Air-to-Air Missile) project":1, "Hypersonic Vehicles":1, "Typical Aerodynamic Layout Design for Hypersonic Aircraft":1, "Integrated Design Technology for Hypersonic Aircraft":1, "Guidance Technology for Hypersonic Aircraft":1, "Flight Control Technology for Hypersonic Aircraft":1, "Thermal Protection Technology for Hypersonic Aircraft":1, "Khinzal Hypersonic Air-Launched Missile System":1, "BrahMos II":1, "BrahMos Mark II":1, "Hyper Velocity Gliding Projectile":1, "HVGP":1, "Zircon Hypersonic Cruise Missile System":1, "Avangard Hypersonic Boost-Glide Missile System":1, "Hypersonic Air-breathing Weapon Concept":1, "OpFires":1, "Operational Fires":1, "R-37M Hypersonic Air-to-Air Missile":1, "SR-72":1, "X-43A":1, "X-51A Waverider":1, "HTV":1, "Hypersonic Technology Vehicle":1, "hypersonic HAWC":1, "Dual-Mode Scramjet Engine":1, "Dual Combustion Chamber Scramjet Engine":1, "Center Combustion Scramjet Engine":1, "Solid Fuel Scramjet Engine":1, "Mode Transition":1, "Integrated Flight and Engine Design":1, "Thermal Protection":1, "Scramjet Combustion Chamber Design":1, "Rocket/Scramjet Engine Integrated Design":1, "Wide-Range Adjustable Forebody/Inlet Design":1, "Injection and Mixing Enhancement":1, "Variable Structure Combustion Chamber":1, "Active Thermal Protection":1, "Precooler":1, "Reheater":1, "High-Performance Rotating Component":1, "Thrust Chamber":1, "Pulse Detonation Engine":1, "Rotating Detonation Engine":1, "Inclined Detonation Engine":1, "Internal Combustion Wave Rotor Detonation Engine":1, "Rocket Engine":1, "Scramjet Engine":1, "Turbine-Based Combined Cycle Engine":1, "Rocket-Based Combined Cycle Engine":1, "Precooled Combined Cycle Engine":1, "Detonation Engine":1, "X-51A and HAWC Program":1, "HyFly and HyFly2 Programs":1, "THOR-ER":1, "Tactical High-speed Offensive Ramjet Engine":1, "Zircon Missile Scramjet Engine":1, "RTA":1, "Revolutionary Turbine Accelerator":1, "FaCET":1, "Falcon Combined-Cycle Engine":1, "SR-72 New Turbine-Based Combined-Cycle Engine":1, "AFRE":1, "Advanced Full Range Engine":1, "HYPR":1, "Hypersonic/High Supersonic Transport Propulsion System":1, "Strutjet Engine":1, "ISTAR Engine":1, "A5-RBCC Engine":1, "GTX-RBCC Engine":1, "RBCC Engine for Single-Stage-to-Orbit Vehicles":1, "PEITO Engine":1, "BANDO Engine":1, "ATREX Engine":1, "PCTJ Engine":1, }

# thresholds = {"Department of Energy":1, "DOE":3, "Advanced Research Projects Agency-Energy":1, "ARPA-E":1, "Ames Laboratory":1, "Argonne National Laboratory":1, "ANL":3, "Brookhaven National Laboratory":1, "BNL":3, "Fermi National Accelerator Laboratory":1, "Fermilab":1, "Idaho National Laboratory":1, "INL":3, "Los Alamos National Laboratory":1, "LANL":3, "Lawrence Berkeley National Laboratory":1, "LBNL":3, "Lawrence Livermore National Laboratory":1, "LLNL":3, "National Energy Technology Laboratory":1, "NETL":3, "National Renewable Energy Laboratory":1, "NREL":3, "Oak Ridge National Laboratory":1, "ORNL":3, "Pacific Northwest National Laboratory":1, "PNNL":3, "Princeton Plasma Physics Laboratory":1, "PPPL":3, "Sandia National Laboratories":1, "SNL":3, "SLAC National Accelerator Laboratory":1, "Savannah River National Laboratory":1, "SRNL":3, "Thomas Jefferson National Accelerator Facility":1, "Office of the Secretary of Defense":1, "Irregular Warfare Technical Support Directorate":1, "Space Development Agency":1, "SDA":3, "Defense Innovation Unit":1, "DIU":3, "Intelligence Advanced Research Projects Activity":1, "IARPA":3, "Combat Capabilities Development Command":1, "CCDC":3, "National Aeronautics and Space Administration":1, "Defense Advanced Research Projects Agency":1, "DARPA":3, "Department of the Army":1, "Army Rapid Capabilities and Critical Technologies Office":1, "RCCTO":3, "Army Futures Command Positioning, Navigation and Timing Cross-Functional Team":1, "Army Applications Laboratory":1, "Army AI Integration Center":1, "Army Futures Command Support Command":1, "Air and Missile Defense Cross-Functional Team of Army Futures Command":1, "Army Capability Development Command":1, "Army Research Laboratory":1, "United States Naval Research Laboratory":1, "NRL":3, "Office of Naval Research, Department of the Navy":1, "ONR":3, "Naval Information Warfare Systems Command":1, "NAVWAR":3, "Naval Surface Warfare Center":1, "NSWC":3, "Strategic Systems Programs":1, "SSP":3, "Naval Undersea Warfare Center":1, "NUWC":3, "Air Force Materiel Command Digital Transformation Office":1, "Air Force Research Laboratory":1, "Air Force Materiel Command Enterprise Capability Collaboration Team":1, "ECCT":3, "Air Combat Command":1, "Arnold Engineering Development Complex":1, "AEDC":3, "NASA":3, "National Aeronautics and Space Administration NASA":1, "NATO Support and Procurement Agency":1, "NSPA":3, "NATO Science and Technology Organization":1, "STO":3, "Russian Foundation for Basic Research":1, "RFBR":3, "European Defence Agency":1, "EDA":3, "European Union Agency for the Space Programme":1, "EUSPA":3, "European Space Agency":1, "ESA":3, }


# 处理数据
processed_data = []
for index, row in df.iterrows():
    first_column = row.iloc[0]
    values = []
    for col in row.index[1:]:
        if col not in thresholds:
            continue
        if pd.notnull(row[col]) and row[col] > thresholds[col]:
            values.append((col, row[col]))
    values.sort(key=lambda x: x[1], reverse=True)
    print(values)
    processed_data.append([first_column, values])

# 创建新的数据框架
new_df = pd.DataFrame(processed_data, columns=['First Column', 'Values'])

# 生成输出文件名（添加时间戳）
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_filename = f"固定关键词词频整理_{timestamp}.xlsx"
output_path = os.path.join(directory, output_filename)

# 保存到新的Excel文件
new_df.to_excel(output_path, index=False)

print("处理完成！结果已保存到", output_path)


