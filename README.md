# 黄色边界线要素分离项目

本项目用于将黄色边界分离为两条独立的线要素，生成ArcMap兼容的shapefile格式。

## 功能特性

- 将原有黄色边界分离为两条指定的线要素
- 支持多种输出格式：Shapefile、GeoJSON、CSV、JSON、TXT
- 完全兼容ArcMap导入
- 自动计算线段长度和几何属性
- 提供详细的坐标信息和属性表

## 项目文件

### 核心文件
- `边界线分离.ipynb` - Jupyter Notebook版本的完整实现
- `边界线分离.py` - Python脚本版本，可直接执行
- `边界提取.ipynb` - 原有的面要素提取功能（保留作为参考）

### 输出文件
所有生成的文件都保存在 `output/` 目录中：
- `黄色边界线要素.shp` - ArcMap兼容的Shapefile主文件
- `黄色边界线要素.shx` - Shapefile索引文件
- `黄色边界线要素.dbf` - Shapefile属性表文件
- `黄色边界线要素.cpg` - Shapefile编码文件
- `黄色边界线要素.prj` - Shapefile投影文件
- `黄色边界线要素.geojson` - GeoJSON格式文件
- `黄色边界线要素坐标.csv` - CSV格式的坐标数据
- `黄色边界线要素.json` - JSON格式的要素数据
- `黄色边界线要素坐标.txt` - 文本格式的详细坐标信息

## 线要素规格

### 边界线1
- 起点坐标：(463, 176)
- 终点坐标：(632, 377)
- 长度：262.61 像素

### 边界线2
- 起点坐标：(478, 428)
- 终点坐标：(575, 770)
- 长度：355.49 像素

## 使用方法

### 方法1：运行Python脚本
```bash
python 边界线分离.py
```

### 方法2：使用Jupyter Notebook
1. 启动Jupyter Notebook
2. 打开 `边界线分离.ipynb`
3. 逐个执行代码单元

### 方法3：手动安装依赖后执行
```bash
pip install pandas numpy matplotlib shapely geopandas opencv-python pillow
python 边界线分离.py
```

## 依赖库

- pandas
- numpy  
- matplotlib
- shapely
- geopandas
- opencv-python
- pillow

## ArcMap导入指南

1. 打开ArcMap
2. 点击 "Add Data" 按钮
3. 导航到项目的 `output` 目录
4. 选择 `黄色边界线要素.shp` 文件
5. 点击 "Add" 添加到地图
6. 线要素将显示为线条
7. 右键图层 → Properties → Symbology 设置线条样式
8. 右键图层 → Open Attribute Table 查看属性

## 属性字段说明

生成的Shapefile包含以下属性字段：

- `line_id`: 线要素唯一标识符 (1或2)
- `name`: 线要素名称 ("边界线1"或"边界线2")
- `start_x`, `start_y`: 起点坐标
- `end_x`, `end_y`: 终点坐标
- `length`: 线段长度（像素单位）

## 坐标系统

- 当前使用图像坐标系（像素坐标）
- 默认CRS：EPSG:4326 (WGS84)
- 如需地理坐标，请在ArcMap中进行坐标转换
- 可通过地理配准将图像与实际地理位置对应

## 注意事项

- 生成的线要素适用于长度、方向等线性分析
- 支持缓冲区分析和邻近度计算
- 可与其他要素进行空间叠加分析
- 适合网络分析和路径规划

## 更新历史

- v1.0: 初始版本，实现基本的线要素分离功能
- v1.1: 增加多格式输出支持
- v1.2: 完善ArcMap兼容性和属性表