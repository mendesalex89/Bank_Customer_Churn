from pydantic import BaseModel

class CustomerBase(BaseModel):
    credit_score: int
    country: str
    gender: str
    age: int
    tenure: int
    balance: float
    products_number: int
    credit_card: int
    active_member: int
    estimated_salary: float

class CustomerResponse(BaseModel):
    churn_probability: float
    is_likely_to_churn: bool 