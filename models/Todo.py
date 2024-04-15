from typing import List, Union

from pydantic import BaseModel


class ToDoModel(BaseModel):
    """Base model of a \"todo\" """

    id: str
    creationDate: Union[None, str] = ""
    user: Union[None, str] = ""
    title: str
    description: str = ""
    completed: bool = False
    dueDate: Union[None, str] = None
    remainders: List[str]
    tags: List[str]
    category: Union[None, str]
