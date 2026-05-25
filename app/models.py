from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Table, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

# Association Table for PromptEntry <-> Tag (Many-to-Many)
prompt_tag = Table(
    'prompt_tag',
    db.Model.metadata,
    Column('prompt_entry_id', ForeignKey('prompt_entry.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    # One-to-many relationship from User to PromptEntry
    prompts: Mapped[List['PromptEntry']] = relationship(back_populates='author', lazy='dynamic')
    # One-to-many relationship from User to AIDiaryEntry
    diary_entries: Mapped[List['AIDiaryEntry']] = relationship(back_populates='author', lazy='dynamic')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class PromptEntry(db.Model):
    __tablename__ = 'prompt_entry'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    original_prompt: Mapped[str] = mapped_column(String(500), nullable=False)
    negative_prompt: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    # Relationships
    author: Mapped['User'] = relationship(back_populates='prompts')
    # Many-to-many relationship with Tag
    tags: Mapped[List['Tag']] = relationship(
        secondary=prompt_tag,
        back_populates='prompts'
    )
    # One-to-many relationship from PromptEntry to AIDiaryEntry (optional log connection)
    diary_entries: Mapped[List['AIDiaryEntry']] = relationship(back_populates='prompt_entry', lazy='dynamic')

class Tag(db.Model):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)

    # Relationships
    # Many-to-many relationship with PromptEntry
    prompts: Mapped[List['PromptEntry']] = relationship(
        secondary=prompt_tag,
        back_populates='tags'
    )

class AIDiaryEntry(db.Model):
    __tablename__ = 'ai_diary_entry'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    content: Mapped[str] = mapped_column(String(2000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    prompt_entry_id: Mapped[Optional[int]] = mapped_column(ForeignKey('prompt_entry.id'), nullable=True)

    # Relationships
    author: Mapped['User'] = relationship(back_populates='diary_entries')
    prompt_entry: Mapped[Optional['PromptEntry']] = relationship(back_populates='diary_entries')

from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

