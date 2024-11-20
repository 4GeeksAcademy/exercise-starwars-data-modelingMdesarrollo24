import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Tabla intermedia para favoritos de personajes
user_character_favorites = Table(
    'user_character_favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True)
)

# Tabla intermedia para favoritos de planetas
user_planet_favorites = Table(
    'user_planet_favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planet.id'), primary_key=True)
)

# Modelo Usuario
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)

    # Relaciones
    favorite_characters = relationship(
        'Character',
        secondary=user_character_favorites,
        back_populates='favorited_by_users'
    )
    favorite_planets = relationship(
        'Planet',
        secondary=user_planet_favorites,
        back_populates='favorited_by_users'
    )

# Modelo Personaje
class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    species = Column(String(50), nullable=True)
    gender = Column(String(20), nullable=True)
    homeworld = Column(String(100), nullable=True)

    # Relaciones
    favorited_by_users = relationship(
        'User',
        secondary=user_character_favorites,
        back_populates='favorite_characters'
    )

# Modelo Planeta
class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    climate = Column(String(50), nullable=True)
    terrain = Column(String(50), nullable=True)
    population = Column(Integer, nullable=True)

    # Relaciones
    favorited_by_users = relationship(
        'User',
        secondary=user_planet_favorites,
        back_populates='favorite_planets'
    )

# Modelo Post (contenido del blog)
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(500), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Relación con Usuario
    author = relationship('User')

# Generar diagrama UML
def to_dict(self):
    return {}

if __name__ == "__main__":
    from eralchemy import render_er
    try:
        result = render_er(Base, 'diagram.png')
        print("¡Diagrama generado!")
    except Exception as e:
        print("Ocurrió un error:", e)
