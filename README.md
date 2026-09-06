catering-ai
正斗粤厨 · 「AI 行业落地专家」转型学习项目（苏德忠）
本仓库用于练习与沉淀工程能力：FastAPI 服务、数据清洗、LLM 应用、Agent 工作流等。
当前已落地：收货单（receipt）管理 API + SQLite 存储 + 接口鉴权 + 结构化日志 + Docker 容器化。
技术栈
- Python 3.13（虚拟环境 ./.venv）
- FastAPI（Web 框架）
- SQLAlchemy + SQLite（数据持久化，库文件 catering.db，已含 115 条真实收货单）
- pydantic-settings（读 .env 配置）
- Docker（可移植部署）
目录结构
catering-ai/
├── main.py            # 入口：创建 FastAPI app、挂中间件与全局异常、注册路由
├── middleware.py      # Day18：request_id 结构化日志中间件
├── config.py          # 用 pydantic-settings 读 .env（API Key、app 名等）
├── auth.py            # 接口鉴权：校验 X-API-Key 请求头
├── database.py        # SQLAlchemy 引擎 / Session / 建表
├── models/            # 数据模型（receipt 收货单、response 统一返回）
├── routers/           # 路由层（items.py：收货单 CRUD + 分页/筛选/排序）
├── services/          # 业务逻辑层（receipt_service.py）
├── data/              # 原始数据 receipts.json、清洗报告 cleaning_report.md
├── tests/             # pytest 用例（Day13：12 用例，覆盖率 76%）
├── Dockerfile         # Day19：把服务打包成镜像
├── .dockerignore
├── requirements.txt
└── catering.db        # SQLite 数据库（115 条记录，随仓库分发）
  另有 src/、init_db.py、seed_data.py、cleaned.csv 等为早期练习 / 种子数据，非运行必需。
环境准备
source .venv/bin/activate
pip install -r requirements.txt
配置（API Key）
鉴权钥匙放在项目根目录的 .env 文件里（本地配置，请勿提交）：
API_KEY=你的真实钥匙
所有接口都要求在请求头带 X-API-Key，值等于上面 .env 里的 API_KEY。
本地运行
source .venv/bin/activate
uvicorn main:app --reload
启动后访问 http://localhost:8000 ；交互式文档在 http://localhost:8000/docs 。
接口一览
      方法
      路径
      说明
      GET
      /hello
      健康检查，返回 app 名与 debug 开关
      POST
      /echo
      原样回显请求体（调试用）
      POST
      /items
      新增一条收货单
      GET
      /items?page=1&size=10&supplier=&date=&order_by=created_at&desc=false
      列表（分页 + 供应商 / 日期筛选 + 排序）
      GET
      /items/{id}
      查单条
      PUT
      /items/{id}
      改单条
      DELETE
      /items/{id}
      删单条
      GET
      /boom
      故意抛错，用于验证全局 500 兜底
  以上接口均需请求头 X-API-Key。
快速验证
curl -H "X-API-Key: <你的API_KEY>" "http://localhost:8000/items?page=1&size=3"
返回示例：
{"code":0,"msg":"ok","data":{"total":115,"page":1,"size":3,"items":[...]}}
Docker 运行（Day19）
构建镜像：
docker build -t catering-ai .
后台启动容器（8080 为本机映射端口，避免与本地 uvicorn 的 8000 冲突）：
docker run -d -p 8080:8000 -e "API_KEY=<你的API_KEY>" catering-ai
验证容器接口：
curl -H "X-API-Key: <你的API_KEY>" "http://localhost:8080/items?page=1&size=3"
提交规范
- 每完成一个 Day / 一项验收，及时 git add + git commit + git push 固化进度。
- .env、*.bak、日志等本地文件不要提交。