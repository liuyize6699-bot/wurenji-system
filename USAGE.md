# 使用指南

## 快速启动

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务
```bash
python start.py
```
或者
```bash
python main.py
```

### 3. 测试系统
```bash
python test_client.py
```

## Coze平台集成

### 在Coze工作流中调用
```json
POST http://your-server:8000/drone/command
Content-Type: application/json

{
  "flight_data": {
    "lat": "22.9500",
    "lng": "113.7600",
    "mission_id": "coze_mission_001",
    "task_type": "patrol"
  }
}
```

### 响应处理
系统会返回包含以下信息的JSON：
- `status`: 执行状态
- `selected_airport`: 选定的起飞点
- `target_coordinates`: 目标坐标
- `flight_sequence`: 飞行阶段序列
- `mission_id`: 任务ID

## WebSocket集成

### 前端连接示例
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.event === 'flight_start') {
        // 处理飞行开始事件
        console.log('新飞行任务:', data.payload);
        // 更新3D可视化界面
        updateVisualization(data.payload);
    }
};
```

## 支持的JSON格式

### 格式1: 嵌套结构
```json
{
  "flight_data": {
    "lat": "22.9944",
    "lng": "113.7258",
    "mission_id": "mission_001",
    "task_type": "patrol"
  }
}
```

### 格式2: 扁平结构（字符串坐标）
```json
{
  "target_coordinate": "22.9944,113.7258",
  "mission_id": "mission_002",
  "task_type": "surveillance"
}
```

### 格式3: 扁平结构（对象坐标）
```json
{
  "target_coordinate": {"lat": 22.9944, "lng": 113.7258},
  "mission_id": "mission_003",
  "task_type": "emergency"
}
```

### 格式4: 直接坐标
```json
{
  "lat": 22.9944,
  "lng": 113.7258,
  "mission_id": "mission_004",
  "task_type": "inspection"
}
```

## 机场信息

系统预配置了东莞地区三个虚拟机场：

1. **顶好大厦** (22.9944, 113.7258)
2. **创投大厦** (22.9242, 113.8401)  
3. **怡丰昌盛** (23.0180, 113.7500)

系统会自动选择距离目标点最近的机场作为起飞点。

## 扩展开发

### 添加新机场
修改 `config.py` 中的 `AIRPORTS` 配置：

```python
AIRPORTS = {
    "新机场": {
        "lat": 22.xxxx,
        "lng": 113.xxxx,
        "name": "新机场",
        "code": "XX"
    }
}
```

### 集成气象API
在 `main.py` 的 `security_audit` 函数中添加气象检查逻辑：

```python
def security_audit(target_lat: float, target_lng: float, task_type: str) -> bool:
    # 添加气象API调用
    weather_ok = check_weather_conditions(target_lat, target_lng)
    if not weather_ok:
        return False
    
    # 其他安全检查...
    return True
```

### 添加禁飞区检查
```python
def check_no_fly_zones(lat: float, lng: float) -> bool:
    # 实现禁飞区检查逻辑
    for zone in NO_FLY_ZONES:
        if point_in_zone(lat, lng, zone):
            return False
    return True
```