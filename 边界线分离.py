#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄色边界线要素分离脚本

功能：将黄色边界分离为两条独立的线要素，生成ArcMap兼容的shapefile格式
作者：自动生成
日期：2024年
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import geopandas as gpd
import os
import json
import math
import warnings
warnings.filterwarnings('ignore')

def main():
    """主函数"""
    print("开始黄色边界线要素分离...")
    
    # 确保输出目录存在
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")
    else:
        print(f"输出目录已存在: {output_dir}")
    
    # 定义两条边界线的起点和终点坐标
    line1_coords = [(463, 176), (632, 377)]  # 边界线1
    line2_coords = [(478, 428), (575, 770)]  # 边界线2
    
    print("边界线坐标定义:")
    print(f"边界线1: 起点{line1_coords[0]} → 终点{line1_coords[1]}")
    print(f"边界线2: 起点{line2_coords[0]} → 终点{line2_coords[1]}")
    
    # 计算线段长度
    def calculate_length(start, end):
        """计算两点间的欧几里得距离"""
        return math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    
    line1_length = calculate_length(line1_coords[0], line1_coords[1])
    line2_length = calculate_length(line2_coords[0], line2_coords[1])
    
    print(f"\n线段长度:")
    print(f"边界线1长度: {line1_length:.2f} 像素")
    print(f"边界线2长度: {line2_length:.2f} 像素")
    
    # 使用Shapely创建LineString几何对象
    line1_geometry = LineString(line1_coords)
    line2_geometry = LineString(line2_coords)
    
    print("线要素几何对象创建完成:")
    print(f"边界线1: {line1_geometry}")
    print(f"边界线2: {line2_geometry}")
    
    # 验证几何对象的有效性
    print(f"\n几何对象有效性检查:")
    print(f"边界线1有效: {'✓' if line1_geometry.is_valid else '✗'}")
    print(f"边界线2有效: {'✓' if line2_geometry.is_valid else '✗'}")
    
    # 创建属性数据
    data = {
        'line_id': [1, 2],
        'name': ['边界线1', '边界线2'],
        'start_x': [line1_coords[0][0], line2_coords[0][0]],
        'start_y': [line1_coords[0][1], line2_coords[0][1]],
        'end_x': [line1_coords[1][0], line2_coords[1][0]],
        'end_y': [line1_coords[1][1], line2_coords[1][1]],
        'length': [line1_geometry.length, line2_geometry.length],
        'geometry': [line1_geometry, line2_geometry]
    }
    
    # 创建GeoDataFrame
    gdf = gpd.GeoDataFrame(data, crs='EPSG:4326')
    
    print("GeoDataFrame创建完成:")
    print(gdf)
    print(f"\n数据类型: {type(gdf)}")
    print(f"坐标参考系统: {gdf.crs}")
    print(f"要素数量: {len(gdf)}")
    
    # 导出文件
    export_files(gdf, output_dir)
    
    # 验证输出文件
    verify_files(output_dir, gdf)
    
    print("\n" + "="*80)
    print("🎯 黄色边界线要素分离完成")
    print("="*80)

def export_files(gdf, output_dir):
    """导出为多种格式"""
    print(f"\n开始导出文件到 {output_dir}...")
    
    # 定义输出文件路径
    shapefile_path = os.path.join(output_dir, "黄色边界线要素.shp")
    geojson_path = os.path.join(output_dir, "黄色边界线要素.geojson")
    csv_path = os.path.join(output_dir, "黄色边界线要素坐标.csv")
    json_path = os.path.join(output_dir, "黄色边界线要素.json")
    txt_path = os.path.join(output_dir, "黄色边界线要素坐标.txt")
    
    # 导出为Shapefile (ArcMap兼容格式)
    try:
        gdf.to_file(shapefile_path, driver='ESRI Shapefile', encoding='utf-8')
        print(f"✅ Shapefile导出成功: {shapefile_path}")
    except Exception as e:
        print(f"❌ Shapefile导出失败: {e}")
    
    # 导出为GeoJSON
    try:
        gdf.to_file(geojson_path, driver='GeoJSON', encoding='utf-8')
        print(f"✅ GeoJSON导出成功: {geojson_path}")
    except Exception as e:
        print(f"❌ GeoJSON导出失败: {e}")
    
    # 导出坐标数据为CSV
    try:
        coords_df = gdf[['line_id', 'name', 'start_x', 'start_y', 'end_x', 'end_y', 'length']].copy()
        coords_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV坐标文件导出成功: {csv_path}")
    except Exception as e:
        print(f"❌ CSV导出失败: {e}")
    
    # 导出为JSON
    try:
        json_data = {
            "type": "FeatureCollection",
            "features": []
        }
        
        for idx, row in gdf.iterrows():
            feature = {
                "type": "Feature",
                "properties": {
                    "line_id": int(row['line_id']),
                    "name": row['name'],
                    "start_x": int(row['start_x']),
                    "start_y": int(row['start_y']),
                    "end_x": int(row['end_x']),
                    "end_y": int(row['end_y']),
                    "length": round(row['length'], 2)
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": list(row['geometry'].coords)
                }
            }
            json_data["features"].append(feature)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON文件导出成功: {json_path}")
    except Exception as e:
        print(f"❌ JSON导出失败: {e}")
    
    # 导出详细的TXT坐标文件
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("黄色边界线要素坐标详情\n")
            f.write("=" * 50 + "\n\n")
            
            for idx, row in gdf.iterrows():
                f.write(f"【{row['name']}】\n")
                f.write(f"线要素ID: {row['line_id']}\n")
                f.write(f"起点坐标: ({row['start_x']}, {row['start_y']})\n")
                f.write(f"终点坐标: ({row['end_x']}, {row['end_y']})\n")
                f.write(f"线段长度: {row['length']:.2f} 像素\n")
                f.write(f"几何类型: LineString\n")
                f.write(f"坐标序列: {list(row['geometry'].coords)}\n")
                f.write("-" * 30 + "\n\n")
            
            f.write(f"总计线要素数量: {len(gdf)}\n")
            f.write(f"总长度: {gdf['length'].sum():.2f} 像素\n")
            f.write(f"导出时间: {pd.Timestamp.now()}\n")
        
        print(f"✅ TXT坐标文件导出成功: {txt_path}")
    except Exception as e:
        print(f"❌ TXT导出失败: {e}")

def verify_files(output_dir, gdf):
    """验证输出文件"""
    print("\n文件验证结果:")
    print("=" * 50)
    
    # 检查生成的文件
    output_files = [
        ("黄色边界线要素.shp", "Shapefile主文件"),
        ("黄色边界线要素.shx", "Shapefile索引文件"),
        ("黄色边界线要素.dbf", "Shapefile属性文件"),
        ("黄色边界线要素.cpg", "Shapefile编码文件"),
        ("黄色边界线要素.prj", "Shapefile投影文件"),
        ("黄色边界线要素.geojson", "GeoJSON文件"),
        ("黄色边界线要素坐标.csv", "CSV坐标文件"),
        ("黄色边界线要素.json", "JSON文件"),
        ("黄色边界线要素坐标.txt", "TXT坐标文件")
    ]
    
    total_size = 0
    for filename, description in output_files:
        file_path = os.path.join(output_dir, filename)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            total_size += file_size
            print(f"✅ {filename:<35} ({description}) - {file_size:>6} bytes")
        else:
            print(f"❌ {filename:<35} ({description}) - 文件不存在")
    
    print(f"\n📊 总文件大小: {total_size:,} bytes ({total_size/1024:.1f} KB)")
    
    # 验证Shapefile完整性
    shapefile_components = [".shp", ".shx", ".dbf"]
    shapefile_complete = all(os.path.exists(os.path.join(output_dir, f"黄色边界线要素{ext}")) for ext in shapefile_components)
    
    print(f"\n🗺️ Shapefile完整性: {'✅ 完整' if shapefile_complete else '❌ 不完整'}")
    
    print(f"\n📊 线要素统计:")
    print(f"   • 数量: {len(gdf)} 条线要素")
    print(f"   • 边界线1长度: {gdf.iloc[0]['length']:.2f} 像素")
    print(f"   • 边界线2长度: {gdf.iloc[1]['length']:.2f} 像素")
    print(f"   • 总长度: {gdf['length'].sum():.2f} 像素")
    print(f"   • 几何类型: LineString")
    
    print(f"\n📍 坐标信息:")
    for idx, row in gdf.iterrows():
        print(f"   • {row['name']}: ({row['start_x']}, {row['start_y']}) → ({row['end_x']}, {row['end_y']})")
    
    print(f"\n🗺️ ArcMap导入指南:")
    print(f"   1. 打开ArcMap")
    print(f"   2. 点击 'Add Data' 按钮")
    print(f"   3. 导航到: {os.path.abspath(output_dir)}")
    print(f"   4. 选择: 黄色边界线要素.shp")
    print(f"   5. 点击 'Add' 添加到地图")
    print(f"   6. 线要素将显示为线条")
    print(f"   7. 右键图层 → Properties → Symbology 设置线条样式")
    print(f"   8. 右键图层 → Open Attribute Table 查看属性")

if __name__ == "__main__":
    main()