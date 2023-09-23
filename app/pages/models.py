from dataclasses import dataclass
from datetime import datetime


@dataclass
class Skill:
    _id: str
    title: str
    icons: list[str]
    description: str
    visible: bool = True


@dataclass
class Experience:
    _id: str
    title_cs: str
    title_en: str
    company: str
    description_cs: str
    description_en: str
    date_from: datetime
    date_to: datetime = None
    visible: bool = True


@dataclass
class Project:
    _id: str
    title: str
    description: str
    added: datetime
    image_id: str
    github_link: str
    project_link: str = ''
    visible: bool = True
    visible_index: bool = False
