# config.py —— Day6 Part B：用 pydantic-settings 读 .env
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # model_config 告诉它：去项目根目录读 .env 文件（utf-8 编码）
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "正斗收货单服务"        # 服务名（默认值，可被 .env 覆盖）
    debug: bool = False                     # 调试开关
    secret_key: str = "dev-placeholder"     # 密钥（真实值放 .env，绝不写死这里）
    db_url: str = "sqlite:///./catering.db" # 数据库连接地址


# 直接实例化；之后全项目用 settings.xxx 读取，不写死
settings = Settings()
