# 福华创新AI飞控指挥系统

## 项目简介
该系统作为 Coze（扣子）平台上"福华创新AI飞控指挥系统"的对接后端，负责接收来自 Coze 工作流的 JSON 指令，进行起飞点智能调度，并为前端 3D 可视化界面提供实时数据支持。

## 核心功能

### 1. RESTful API 接口
- **路径**: `POST /drone/command`
- **功能**: 接收飞行指令，进行智能调度
- **支持两种JSON结构**:
  - 结构A（嵌套型）: `{"flight_data": {"lat": "...", "lng": "...", "mission_id": "...", "task_type": "..."}}`
  - 结构B（扁平型）: 包含 `target_coordinate` 及其他任务元数据

### 2. 智能调度算法
- 使用 Haversine 公式计算距离
- 自动选择最近的起飞点
- **东莞地区虚拟机场**:
  - 顶好大厦 (22.9944, 113.7258)
  - 创投大厦 (22.9242, 113.8401)
  - 怡丰昌盛 (23.0180, 113.7500)

### 3. 飞行序列模拟
自动生成四阶段飞行序列：
- TAKEOFF (起飞)
- CLIMB (爬升)
- CRUISE (巡航)
- LAND (降落)

### 4. WebSocket 实时通信
- 路径: `ws://localhost:8000/ws`
- 功能: 实时推送飞行数据到前端可视化界面

### 5. 安全验证
- 预留安全审计函数
- 支持气象和禁飞区校验扩展

## 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python main.py
```

服务将在 `http://localhost:8000` 启动

### API 文档
启动后访问 `http://localhost:8000/docs` 查看自动生成的 API 文档

## API 端点

### POST /drone/command
接收飞行指令并返回调度结果

**请求示例1（结构A）**:
```json
{
  "flight_data": {
    "lat": "22.9500",
    "lng": "113.7600",
    "mission_id": "mission_001",
    "task_type": "patrol"
  }
}
```

**请求示例2（结构B）**:
```json
{
  "target_coordinate": "22.9500,113.7600",
  "mission_id": "mission_002",
  "task_type": "surveillance"
}
```

**响应示例**:
```json
{
  "status": "success",
  "message": "指令执行成功",
  "mission_id": "mission_001",
  "selected_airport": "顶好大厦",
  "target_coordinates": {"lat": 22.95, "lng": 113.76},
  "flight_sequence": ["TAKEOFF", "CLIMB", "CRUISE", "LAND"],
  "timestamp": "2024-01-01T12:00:00"
}
```

### WebSocket /ws
实时数据推送，消息格式：
```json
{
  "event": "flight_start",
  "payload": {
    "mission_id": "mission_001",
    "selected_airport": "顶好大厦",
    "airport_coordinates": {"lat": 22.9944, "lng": 113.7258, "name": "顶好大厦"},
    "target_coordinates": {"lat": 22.95, "lng": 113.76},
    "task_type": "patrol",
    "flight_sequence": ["TAKEOFF", "CLIMB", "CRUISE", "LAND"],
    "timestamp": "2024-01-01T12:00:00"
  }
}
```

### 其他端点
- `GET /` - 系统状态
- `GET /airports` - 获取所有机场信息
- `GET /health` - 健康检查

## 技术特性
- **高鲁棒性**: 支持多种JSON结构解析
- **智能调度**: 基于Haversine距离算法
- **实时通信**: WebSocket支持
- **自动文档**: FastAPI自动生成API文档
- **CORS支持**: 跨域请求支持
- **日志记录**: 完整的操作日志

## 扩展说明
- 安全审计函数可扩展气象API集成
- 支持添加更多虚拟机场
- WebSocket可扩展更多事件类型
- 支持数据库持久化扩展