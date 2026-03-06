from pydantic import BaseModel
from typing import Optional

class UserForm(BaseModel):
    state: str
    age: int
    gender: str
    employment_status: Optional[str] = None
    marital_status: Optional[str] = None
    category: Optional[str] = None
    disability: Optional[bool] = False
