import os
from typing import Optional

from pydantic import BaseModel


class Config(BaseModel):
    """HelloAgents配置类"""
    # LLM配置
    default_model: str = "gpt-3.5-turbo"
    default_provider: str = "openai"
    temperature: float = 0.7
    max_token: Optional[int] = None

    # 系统配置
    debug: bool = False
    log_level: str = "INFO"

    # 其它配置
    max_history_length: int = 100

    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量创建配置"""
        return cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_token=int(os.getenv("MAX_TOKEN")) if os.getenv("MAX_TOKEN") else None,
        )

    def to_dict(self) -> dict[str, any]:
        return self.dict()
