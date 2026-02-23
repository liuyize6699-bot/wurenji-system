# AirSim 无 NumPy 使用指南

## 🎯 问题说明

Python 3.14 目前无法安装 NumPy，但 AirSim 可以在不使用 NumPy 的情况下工作。

## ✅ 解决方案

### 方法1：使用 Python 内置类型

AirSim 的大多数 API 可以接受普通的 Python 类型（float, tuple, dict）而不需要 NumPy 数组。

#### 示例：位置和向量

```python
# ❌ 使用 NumPy（需要安装）
import numpy as np
position = np.array([10.0, 20.0, -5.0])

# ✅ 使用 Python 内置类型（无需 NumPy）
position = (10.0, 20.0, -5.0)  # tuple
# 或
position = [10.0, 20.0, -5.0]  # list
# 或
position = {"x": 10.0, "y": 20.0, "z": -5.0}  # dict
```

#### 示例：数学计算

```python
import math

# 向量长度
v = (3.0, 4.0, 0.0)
length = math.sqrt(sum(x**2 for x in v))

# 两点距离
p1 = (0.0, 0.0, 0.0)
p2 = (10.0, 10.0, -5.0)
distance = math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

# 角度计算
angle_rad = math.atan2(v[1], v[0])
angle_deg = math.degrees(angle_rad)
```

## 🚀 快速开始

### 1. 安装 AirSim（不需要 NumPy）

```bash
pip install airsim
```

### 2. 运行简单测试

```bash
# 最简单的起飞测试
python simple_takeoff.py

# 完整功能测试
python test_no_numpy.py
```

### 3. 基本代码模板

```python
import airsim
import time
import math

# 连接
client = airsim.MultirotorClient()
client.confirmConnection()

# 启用控制
client.enableApiControl(True)
client.armDisarm(True)

# 起飞
client.takeoffAsync().join()

# 移动（使用普通 float）
client.moveToPositionAsync(10.0, 10.0, -5.0, 3.0).join()

# 获取状态
state = client.getMultirotorState()
pos = state.kinematics_estimated.position
x, y, z = pos.x_val, pos.y_val, pos.z_val

# 降落
client.landAsync().join()

# 清理
client.armDisarm(False)
client.enableApiControl(False)
```

## 📚 常用操作（无 NumPy）

### 起飞和降落

```python
# 起飞到默认高度
client.takeoffAsync().join()

# 降落
client.landAsync().join()
```

### 移动控制

```python
# 移动到指定位置（x, y, z, velocity）
client.moveToPositionAsync(10.0, 20.0, -5.0, 3.0).join()

# 按速度移动（vx, vy, vz, duration）
client.moveByVelocityAsync(1.0, 0.0, 0.0, 5.0).join()

# 悬停
client.hoverAsync().join()
```

### 获取状态

```python
# 获取无人机状态
state = client.getMultirotorState()

# 位置
pos = state.kinematics_estimated.position
x = pos.x_val
y = pos.y_val
z = pos.z_val
altitude = -z  # AirSim 中 Z 轴向下

# 速度
vel = state.kinematics_estimated.linear_velocity
vx = vel.x_val
vy = vel.y_val
vz = vel.z_val

# 姿态（四元数）
orientation = state.kinematics_estimated.orientation
w = orientation.w_val
x = orientation.x_val
y = orientation.y_val
z = orientation.z_val
```

### 数学计算（使用 math 库）

```python
import math

# 计算距离
def calculate_distance(p1, p2):
    """计算两点间距离"""
    return math.sqrt(
        (p1[0] - p2[0])**2 + 
        (p1[1] - p2[1])**2 + 
        (p1[2] - p2[2])**2
    )

# 计算角度
def calculate_angle(dx, dy):
    """计算方向角"""
    return math.atan2(dy, dx)

# 向量归一化
def normalize_vector(v):
    """归一化向量"""
    length = math.sqrt(sum(x**2 for x in v))
    if length == 0:
        return v
    return tuple(x / length for x in v)

# 向量点积
def dot_product(v1, v2):
    """计算点积"""
    return sum(a * b for a, b in zip(v1, v2))

# 向量叉积（3D）
def cross_product(v1, v2):
    """计算叉积"""
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    )
```

## 🔧 完整示例

### 示例1：简单巡航

```python
import airsim
import time

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# 起飞
print("起飞...")
client.takeoffAsync().join()

# 巡航路径（使用 tuple）
waypoints = [
    (10.0, 0.0, -5.0),
    (10.0, 10.0, -5.0),
    (0.0, 10.0, -5.0),
    (0.0, 0.0, -5.0)
]

# 访问每个航点
for i, (x, y, z) in enumerate(waypoints, 1):
    print(f"前往航点 {i}: ({x}, {y}, {z})")
    client.moveToPositionAsync(x, y, z, 3.0).join()
    time.sleep(1)

# 降落
print("降落...")
client.landAsync().join()

# 清理
client.armDisarm(False)
client.enableApiControl(False)
print("完成！")
```

### 示例2：圆形飞行

```python
import airsim
import math
import time

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# 起飞
client.takeoffAsync().join()

# 圆形飞行参数
radius = 10.0
altitude = -5.0
num_points = 36
velocity = 3.0

print("开始圆形飞行...")

for i in range(num_points):
    angle = 2 * math.pi * i / num_points
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    
    client.moveToPositionAsync(x, y, altitude, velocity).join()
    time.sleep(0.5)

print("圆形飞行完成")

# 降落
client.landAsync().join()
client.armDisarm(False)
client.enableApiControl(False)
```

## ⚠️ 注意事项

1. **AirSim 模拟器必须运行**
   - 确保 Unreal Engine 中的 AirSim 项目已启动
   - 或运行预编译的 AirSim 可执行文件

2. **配置文件**
   - 检查 `~/Documents/AirSim/settings.json`
   - 确保使用 Multirotor 模式

3. **坐标系统**
   - X: 前方（北）
   - Y: 右方（东）
   - Z: 向下（高度为负值）

4. **异步操作**
   - 大多数操作返回 Future 对象
   - 使用 `.join()` 等待完成

## 🎓 学习资源

- AirSim 官方文档: https://microsoft.github.io/AirSim/
- AirSim Python API: https://microsoft.github.io/AirSim/apis/
- Python math 库: https://docs.python.org/3/library/math.html

## 🐛 故障排除

### 问题：无法连接到 AirSim

```python
# 检查连接
try:
    client = airsim.MultirotorClient()
    client.confirmConnection()
    print("✅ 连接成功")
except Exception as e:
    print(f"❌ 连接失败: {e}")
    print("请确保 AirSim 模拟器正在运行")
```

### 问题：无人机不响应

```python
# 重置无人机
client.reset()
client.enableApiControl(True)
client.armDisarm(True)
```

### 问题：位置不准确

```python
# 使用更低的速度
client.moveToPositionAsync(x, y, z, velocity=1.0).join()

# 增加等待时间
time.sleep(2)
```