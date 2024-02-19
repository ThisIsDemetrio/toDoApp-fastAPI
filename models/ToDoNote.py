from datetime import datetime
from pydantic import BaseModel
from typing import List, Union

class ToDoNoteModel(BaseModel):
    """Base model of a note"""
    id: str
    creationDate: Union[None, str] = ""
    title: str
    description: str = ""
    completed: bool = False
    dueDate: Union[None, str] = None
    remainders: List[str]
    tags: List[str]
    category: Union[None, str]
