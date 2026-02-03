# 轻语AI飞控指挥系统 - 云端部署指南

## 🚀 Zeabur 部署

### 1. 准备工作
确保项目包含以下文件：
- `zbpack.json` - Python版本锁定
- `requirements.txt` - 依赖包列表
- `app.py` - Zeabur部署入口
- `main.py` - 主应用文件
- `Procfile` - 进程配置（可选）

### 2. 部署步骤

#### 方法1：GitHub 自动部署
1. 将代码推送到 GitHub 仓库
2. 在 Zeabur 控制台连接 GitHub 仓库
3. 选择项目并部署
4. Zeabur 会自动识别 Python 项目并使用 `zbpack.json` 配置

#### 方法2：直接部署
1. 登录 [Zeabur](https://zeabur.com)
2. 创建新项目
3. 选择 "Deploy from GitHub" 或上传代码
4. 等待自动构建和部署

### 3. 环境配置

#### 自动配置
- Python 版本：3.11（通过 zbpack.json 锁定）
- 端口：自动从环境变量 PORT 获取
- 主机：0.0.0.0（适配云端）

#### 手动配置（如需要）
在 Zeabur 环境变量中设置：
```
PORT=8080
PYTHON_VERSION=3.11
```

### 4. 访问服务

部署成功后，Zeabur 会提供一个公网域名，例如：
- 系统状态: `https://your-app.zeabur.app/`
- API接口: `https://your-app.zeabur.app/drone/command`
- 健康检查: `https://your-app.zeabur.app/health`
- API文档: `https://your-app.zeabur.app/docs`

### 5. 扣子平台对接

将 Zeabur 提供的域名配置到扣子工作流中：
```
POST https://your-app.zeabur.app/drone/command
Content-Type: application/json

{
  "flight_data": {
    "lat": "22.95",
    "lng": "113.76",
    "mission_id": "coze_mission_001",
    "task_type": "patrol"
  }
}
```

## 🔧 故障排除

### 常见问题

1. **Python版本不兼容**
   - 确保 `zbpack.json` 存在且配置正确
   - 检查 `requirements.txt` 中的包版本

2. **端口绑定失败**
   - 确保使用 `os.environ.get("PORT", 8080)`
   - 主机地址使用 `0.0.0.0`

3. **依赖安装失败**
   - 检查 `requirements.txt` 格式
   - 确保所有包版本兼容 Python 3.11

### 日志查看
在 Zeabur 控制台的 "Logs" 标签页查看部署和运行日志。

## 📊 性能监控

部署后可以通过以下方式监控：
- Zeabur 控制台的监控面板
- 访问 `/health` 端点检查服务状态
- 查看应用日志了解请求处理情况

## 🔄 更新部署

1. 修改代码并推送到 GitHub
2. Zeabur 会自动检测更改并重新部署
3. 或在 Zeabur 控制台手动触发重新部署