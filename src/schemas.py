from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.models import Workload

class EmployeesAddDTO(BaseModel):
    username: str

class EmployeesDTO(EmployeesAddDTO):
    id: int

class ResumesAddDTO(BaseModel):
    title: str
    compensation: Optional[int]
    workload: Workload
    employee_id: int

class ResumesDTO(ResumesAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime

class ResumesRelDTO(ResumesDTO):
    employee: 'EmployeesDTO'

class EmployeesRelDTO(EmployeesDTO):
    resumes: list['ResumesDTO']