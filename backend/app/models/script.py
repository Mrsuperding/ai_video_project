"""
脚本相关模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, JSON, Text, DECIMAL, Index, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Script(Base):
    """脚本表"""
    __tablename__ = "scripts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    title = Column(String(200), nullable=False, comment="脚本标题")
    description = Column(Text, nullable=True, comment="脚本描述")

    content = Column(JSON, nullable=False, comment="脚本内容")
    plain_text = Column(Text, nullable=True, comment="纯文本内容")
    word_count = Column(BigInteger, nullable=True, comment="字数")
    estimated_duration = Column(DECIMAL(8, 2), nullable=True, comment="预估时长(秒)")

    language = Column(String(10), default="zh", comment="主要语言")
    voice_id = Column(BigInteger, ForeignKey("voice_clones.id", ondelete="SET NULL"), nullable=True, comment="关联音色ID")
    base_tts_speed = Column(DECIMAL(3, 2), default=1.00, comment="基础语速")

    tags = Column(JSON, nullable=True, comment="标签")
    category = Column(String(50), nullable=True, comment="分类")
    template_id = Column(BigInteger, ForeignKey("script_templates.id", ondelete="SET NULL"), nullable=True, comment="来源模板ID")
    is_template = Column(Boolean, default=False, comment="是否为模板")

    ai_generated = Column(Boolean, default=False, comment="是否AI生成")
    ai_prompt = Column(Text, nullable=True, comment="AI生成时的提示词")
    ai_model = Column(String(50), nullable=True, comment="使用的AI模型")

    status = Column(Enum("draft", "published", "archived"), default="draft", comment="状态")

    usage_count = Column(BigInteger, default=0, comment="使用次数")
    view_count = Column(BigInteger, default=0, comment="查看次数")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True, comment="软删除时间")

    __table_args__ = (
        Index("idx_scripts_user_id", "user_id"),
        Index("idx_scripts_status", "status"),
        Index("idx_scripts_category", "category"),
        Index("idx_scripts_is_template", "is_template"),
    )


class ScriptTemplate(Base):
    """脚本模板表"""
    __tablename__ = "script_templates"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="模板名称")
    description = Column(Text, nullable=True, comment="模板描述")
    cover_image_url = Column(String(500), nullable=True, comment="封面图URL")

    category = Column(String(50), nullable=False, comment="分类")
    subcategory = Column(String(50), nullable=True, comment="子分类")
    tags = Column(JSON, nullable=True, comment="标签")

    content = Column(JSON, nullable=False, comment="模板内容结构")
    example_text = Column(Text, nullable=True, comment="示例文本")
    prompt_template = Column(Text, nullable=True, comment="AI生成提示词模板")

    language = Column(String(10), default="zh", comment="支持语言")
    input_fields = Column(JSON, nullable=True, comment="需要的输入字段")

    source = Column(Enum("platform", "user", "market"), default="platform", comment="来源")
    creator_id = Column(BigInteger, nullable=True, comment="创建者ID")
    price = Column(DECIMAL(10, 2), nullable=True, comment="价格")

    usage_count = Column(BigInteger, default=0, comment="使用次数")
    favor_count = Column(BigInteger, default=0, comment="收藏次数")
    rating = Column(DECIMAL(3, 2), nullable=True, comment="评分")
    rating_count = Column(BigInteger, default=0, comment="评分人数")

    status = Column(Enum("active", "inactive", "deleted"), default="active", comment="状态")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_script_templates_category", "category"),
        Index("idx_script_templates_source", "source"),
        Index("idx_script_templates_status", "status"),
        Index("idx_script_templates_usage_count", "usage_count"),
    )


class AIWritingTask(Base):
    """AI写作任务表"""
    __tablename__ = "ai_writing_tasks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    script_id = Column(BigInteger, ForeignKey("scripts.id", ondelete="CASCADE"), nullable=True, comment="关联脚本ID")

    task_type = Column(Enum("generate", "rewrite", "expand", "shrink", "translate", "polish"), nullable=False, comment="任务类型")

    input_prompt = Column(Text, nullable=True, comment="提示词")
    input_text = Column(Text, nullable=True, comment="输入文本")
    source_language = Column(String(10), nullable=True, comment="源语言")
    target_language = Column(String(10), nullable=True, comment="目标语言")
    template_id = Column(BigInteger, ForeignKey("script_templates.id", ondelete="SET NULL"), nullable=True, comment="使用的模板ID")

    output_text = Column(Text, nullable=True, comment="生成的内容")
    output_segments = Column(JSON, nullable=True, comment="分段后的内容")

    status = Column(Enum("queued", "processing", "completed", "failed"), default="queued", comment="状态")
    progress = Column(BigInteger, default=0, comment="进度 0-100")

    ai_model = Column(String(50), nullable=True, comment="使用的AI模型")
    emotion = Column(Enum("neutral", "happy", "serious", "humorous"), nullable=True, comment="情感倾向")
    style = Column(String(50), nullable=True, comment="风格")

    input_tokens = Column(BigInteger, nullable=True, comment="输入token数")
    output_tokens = Column(BigInteger, nullable=True, comment="输出token数")
    cost_cents = Column(BigInteger, nullable=True, comment="成本(分)")

    error_message = Column(Text, nullable=True, comment="错误信息")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_ai_writing_tasks_user_id", "user_id"),
        Index("idx_ai_writing_tasks_script_id", "script_id"),
        Index("idx_ai_writing_tasks_status", "status"),
    )