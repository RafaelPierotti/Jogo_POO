from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from Usuario import Base

class Ponto(Base):
    __tablename__ = 'Ponto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    pontuacao = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="pontos")

    def __repr__(self):
        return f"<Ponto(usuario={self.usuario.nome}, pontuacao={self.pontuacao}, data={self.data})>"