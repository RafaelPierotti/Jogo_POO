import pygame
from abc import ABC, abstractmethod

class Objetos(ABC):
    @abstractmethod
    def desenhar(self, tela):
        pass