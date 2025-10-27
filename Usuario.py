from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    criacao = Column(DateTime, default=datetime.utcnow)

    pontos = relationship("Ponto", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario(nome={self.nome}, criado_em={self.criado_em})>"