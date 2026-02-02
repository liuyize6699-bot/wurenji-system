# 扣子（Coze）平台对接指南

## 🔗 对接概述

你的福华创新AI飞控指挥系统现在可以作为扣子工作流的后端API服务，接收飞行指令并返回智能调度结果。

## 📋 对接步骤

### 1. 确保服务运行
```bash
py simple_server.py
```
服务地址：`http://localhost:8000`

### 2. 在扣子平台配置HTTP请求节点

#### 基本配置：
- **请求方法**: POST
- **请求URL**: `http://你的服务器IP:8000/drone/command`
- **Content-Type**: `application/json`

#### 如果是本地测试：
- **URL**: `http://localhost:8000/drone/command`

#### 如果需要外网访问：
你需要：
1. 部署到云服务器，或
2. 使用内网穿透工具（如ngrok、frp等）

## 🎯 扣子工作流配置示例

### 方案1：嵌套结构（推荐）
在扣子的HTTP请求节点中配置：

**请求体模板：**
```json
{
  "flight_data": {
    "lat": "{{纬度变量}}",
    "lng": "{{经度变量}}",
    "mission_id": "{{任务ID变量}}",
    "task_type": "{{任务类型变量}}"
  }
}
```

**变量映射示例：**
- `{{纬度变量}}` → 从用户输入或上游节点获取
- `{{经度变量}}` → 从用户输入或上游节点获取  
- `{{任务ID变量}}` → 可以是时间戳或UUID
- `{{任务类型变量}}` → patrol/surveillance/emergency/inspection

### 方案2：扁平结构
```json
{
  "target_coordinate": "{{纬度变量}},{{经度变量}}",
  "mission_id": "{{任务ID变量}}",
  "task_type": "{{任务类型变量}}"
}
```

### 方案3：对象坐标
```json
{
  "target_coordinate": {
    "lat": {{纬度变量}},
    "lng": {{经度变量}}
  },
  "mission_id": "{{任务ID变量}}",
  "task_type": "{{任务类型变量}}"
}
```

## 📤 响应处理

系统会返回以下JSON结构：

```json
{
  "status": "success",
  "message": "指令执行成功",
  "mission_id": "任务ID",
  "selected_airport": "选定的机场名称",
  "target_coordinates": {
    "lat": 22.95,
    "lng": 113.76
  },
  "flight_sequence": ["TAKEOFF", "CLIMB", "CRUISE", "LAND"],
  "timestamp": "2024-01-01T12:00:00"
}
```

### 在扣子中使用响应数据：
- `{{response.selected_airport}}` - 获取选定的起飞机场
- `{{response.mission_id}}` - 获取任务ID
- `{{response.status}}` - 获取执行状态
- `{{response.flight_sequence}}` - 获取飞行阶段序列

## 🌐 部署到云服务器（推荐）

### 选项1：使用云服务器
1. 购买云服务器（阿里云、腾讯云、华为云等）
2. 上传代码文件
3. 安装Python：`sudo apt install python3 python3-pip`
4. 运行服务：`python3 simple_server.py`
5. 配置防火墙开放8000端口

### 选项2：使用内网穿透（测试用）
```bash
# 安装ngrok
# 下载：https://ngrok.com/download

# 启动内网穿透
ngrok http 8000

# 会得到一个公网地址，如：https://abc123.ngrok.io
# 在扣子中使用：https://abc123.ngrok.io/drone/command
```

## 🔧 扣子工作流完整示例

### 工作流设计：
1. **触发器** → 用户输入坐标和任务类型
2. **数据处理** → 格式化输入数据
3. **HTTP请求** → 调用飞控API
4. **结果处理** → 解析响应并格式化输出
5. **回复用户** → 返回调度结果

### 示例对话流程：
```
用户: "我需要在坐标22.95,113.76执行巡逻任务"

扣子工作流:
1. 解析坐标: lat=22.95, lng=113.76
2. 设置任务类型: task_type=patrol
3. 调用API: POST /drone/command
4. 获得响应: selected_airport=顶好大厦
5. 回复: "任务已安排！选定起飞点：顶好大厦，飞行序列：起飞→爬升→巡航→降落"
```

## 📊 监控和日志

### 查看系统状态：
- 访问：`http://你的服务器:8000/health`
- 返回：`{"status": "healthy", "timestamp": "..."}`

### 查看机场信息：
- 访问：`http://你的服务器:8000/airports`
- 返回所有可用机场的坐标信息

## 🛠️ 故障排除

### 常见问题：

1. **连接失败**
   - 检查服务是否启动：`py simple_server.py`
   - 检查端口是否开放：`netstat -an | findstr 8000`

2. **坐标解析失败**
   - 确保坐标格式正确
   - 支持的格式：字符串"22.95,113.76"或对象{"lat":22.95,"lng":113.76}

3. **返回错误**
   - 检查JSON格式是否正确
   - 查看服务器日志了解具体错误

## 🚀 高级功能扩展

### 添加认证（可选）：
```python
# 在simple_server.py中添加API密钥验证
def check_auth(self):
    auth_header = self.headers.get('Authorization')
    return auth_header == 'Bearer your-secret-key'
```

### 添加数据库记录（可选）：
```python
# 记录所有飞行任务到数据库
import sqlite3
def save_mission(mission_data):
    # 保存任务记录
    pass
```

## 📞 技术支持

如果在对接过程中遇到问题：
1. 检查服务器日志
2. 使用测试脚本验证API功能：`py simple_test.py`
3. 确认网络连接和防火墙设置