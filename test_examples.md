# 系统测试示例

## 不需要Python环境的测试方法

### 1. 使用curl命令测试（如果有Git Bash或WSL）

**测试结构A（嵌套型）：**
```bash
curl -X POST http://localhost:8000/drone/command \
  -H "Content-Type: application/json" \
  -d '{
    "flight_data": {
      "lat": "22.9500",
      "lng": "113.7600",
      "mission_id": "test_001",
      "task_type": "patrol"
    }
  }'
```

**测试结构B（扁平型）：**
```bash
curl -X POST http://localhost:8000/drone/command \
  -H "Content-Type: application/json" \
  -d '{
    "target_coordinate": "22.9200,113.8300",
    "mission_id": "test_002",
    "task_type": "surveillance"
  }'
```

### 2. 使用Postman测试

1. 打开Postman
2. 创建新的POST请求
3. URL: `http://localhost:8000/drone/command`
4. Headers: `Content-Type: application/json`
5. Body选择raw，粘贴以下JSON：

```json
{
  "flight_data": {
    "lat": "22.9500",
    "lng": "113.7600", 
    "mission_id": "postman_test",
    "task_type": "patrol"
  }
}
```

### 3. 使用浏览器测试API文档

启动服务后访问：`http://localhost:8000/docs`

这里有交互式API文档，可以直接在浏览器中测试所有接口。

### 4. 预期响应示例

```json
{
  "status": "success",
  "message": "指令执行成功",
  "mission_id": "test_001",
  "selected_airport": "顶好大厦",
  "target_coordinates": {
    "lat": 22.95,
    "lng": 113.76
  },
  "flight_sequence": ["TAKEOFF", "CLIMB", "CRUISE", "LAND"],
  "timestamp": "2024-01-01T12:00:00"
}
```

## 如果你有Python环境

### 快速启动命令：
```bash
# 安装依赖
pip install fastapi uvicorn websockets pydantic

# 启动服务
python main.py
```

### 或者使用我们的启动脚本：
```bash
python start.py
```

## 系统状态检查

访问以下URL检查系统状态：
- 系统首页: http://localhost:8000/
- 健康检查: http://localhost:8000/health  
- 机场信息: http://localhost:8000/airports
- API文档: http://localhost:8000/docs

## WebSocket测试

可以使用在线WebSocket测试工具：
1. 访问 https://www.websocket.org/echo.html
2. 连接到: `ws://localhost:8000/ws`
3. 发送API请求后观察WebSocket消息