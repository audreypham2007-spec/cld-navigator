# database.py - the "filing cabinet" that saves every case

import os
from datetime import datetime

from sqlalchemy import ForeignKey, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

# Where the database is saved (a file on your computer for now)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///cld_navigator.db")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# Table 1: one row per child (a code, never a real name)
class Case(Base):
    __tablename__ = "cases"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_code: Mapped[str] = mapped_column(unique=True)
    age_months: Mapped[int]
    concerns: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    languages: Mapped[list["Language"]] = relationship(
        back_populates="case", cascade="all, delete-orphan")


# Table 2: one row per language the child hears or speaks
class Language(Base):
    __tablename__ = "languages"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"))
    name: Mapped[str]
    percent_hears: Mapped[int | None]
    percent_speaks: Mapped[int | None]
    case: Mapped[Case] = relationship(back_populates="languages")


# Create the tables if they don't exist yet
Base.metadata.create_all(engine)


# Quick test: only runs when you type "python database.py"
if __name__ == "__main__":
    with Session() as s:
        test = Case(case_code="TEST-001", age_months=48, concerns="Vocabulary")
        test.languages.append(Language(name="Vietnamese", percent_hears=70, percent_speaks=60))
        s.add(test)
        s.commit()
        print("Saved:", test.case_code, "-", test.languages[0].name)
        s.delete(test)
        s.commit()
        print("Database works!")