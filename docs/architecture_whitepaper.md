# Liulianmao 架构白皮书

## 核心设计原则
- **可插拔架构**：所有组件通过配置动态加载
- **技术中立**：无厂商硬编码，仅依赖`series_name`
- **协议透明**：业务逻辑不感知底层通信协议

## 目录结构
```bash
.
├── config.yaml              # 全局配置入口
├── core/
│   ├── dispatcher.py        # 路由核心（根据配置动态加载组件）
├── providers/               # 厂商实现层
│   ├── {series_name}/       # 厂商隔离目录
│   │   ├── official_lib.py  # 原生SDK调用
│   │   └── http_impl.py    # 自实现HTTP
└── agents/
    ├── interfaces.py        # 抽象接口
    ├── text_parser/         # 文本解析模式
    └── external/            # 外部Agent桥接
└── tools/                  # 独立工具集
    ├── geo_utils.py        # 地理工具
    └── data_parser.py      # 数据解析
```

## 关键组件说明

### 1. 配置系统
```yaml
# config.yaml 示例
providers:
  openai:
    adapter: http_impl
    priority: 1
  zhipu:
    adapter: functional_call
    priority: 2

agents:
  weather:
    handler: external
    endpoint: http://weather:8000
```

### 2. 动态加载机制
```python
# core/dispatcher.py
def load_provider(series_name):
    config = load_config()
    adapter = config.providers[series_name]['adapter']
    return import_module(f"providers.{series_name}.{adapter}")
```

### 3. Agent扩展规范
```python
# agents/interfaces.py
class AgentBase:
    @classmethod
    def from_config(cls, config: dict):
        """必须实现的工厂方法"""
        
    def execute(self, task: dict) -> dict:
        """统一执行接口"""
```

## 演进路线
1. v0.1 - 基础协议支持（HTTP/Function Call）
2. v0.2 - 外部Agent集成
3. v0.3 - 性能优化（连接池/缓存）