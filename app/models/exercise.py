from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.core.database import Base

class Exercise(Base):
    __tablename__ = "exercises"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    muscle_group: Mapped[str] = mapped_column(String(50))
    equipment: Mapped[str | None] = mapped_column(String(120), nullable=True)
