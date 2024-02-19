from pydantic import BaseModel
from typing import List, Union

class ToDoModel(BaseModel):
    """Base model of a \"todo\""""
    id: str
    creationDate: Union[None, str] = ""
    title: str
    description: str = ""
    completed: bool = False
    dueDate: Union[None, str] = None
    remainders: List[str]
    tags: List[str]
    category: Union[None, str]
