
from pydantic import BaseModel

class EligibilitySend(BaseModel):
    userID: str
    status: str
    reason: str
    discoverInput: str
    accessInput: str


class Eligibility(BaseModel):
    submissionID: str
    userID: str
    status: str
    reason: str
