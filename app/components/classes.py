from pydantic import BaseModel, Field
from typing import Literal, Optional
import operator
from typing import List, Annotated
from typing_extensions import TypedDict




class Coders(BaseModel):
    name: str = Field(
        description="Name of the analyst."
    )
    # model: Literal["gpt-4o","gpt-4o", "gpt-4o"] = Field(
    #     description="Role of the analyst in the context of the topic.",
    # )
    @property
    def persona(self) -> str:
        return f"Name: {self.name}\model: {self.model}"
    

class patient(TypedDict):
  patient_name: str
  patient_date_of_birth: str
  patient_ssn: str
  patient_address_street: str
  patient_address_2: str
  patient_address_city: str
  patient_address_state: str
  patient_address_zip: str

class insurance_company(TypedDict):
  insurance_company_name: str
  insurance_company_contact_number: str
  insurance_company_email: str
  insurance_company_address: str

class patientgraph(TypedDict):
    patient: patient # Research topic
    messages: Annotated[list, operator.add] # Send() API key
    medicalreport: str # Content for the final report
    ediclaim: str # Final report
    max_coders: int
    coders: List[Coders]
    insurance_company: insurance_company
    approved: str
    reviewer_comments: str 
    iteration: int
    coder_comments:str


class Perspectives(BaseModel):
    coders: List[Coders] = Field(
        description="Comprehensive list of coders with their roles and affiliations.",
    )


class pull_pi(TypedDict):
    patient:patient
    insurance_company: insurance_company


class ClaimOutput(TypedDict):
    ediclaim: str =Field(description="Original or Update EDI claim")
    coder_comments: str

class comment_approve(TypedDict):
    review_comments: str
    approval: Literal["yes","no"]