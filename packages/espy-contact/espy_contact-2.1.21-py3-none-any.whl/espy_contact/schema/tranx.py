"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

from datetime import datetime, date
from enum import Enum
from typing import Annotated, Optional
from pydantic import BaseModel, Field, model_validator
from espy_contact.util.enums import NigerianBank


class AccountDto(BaseModel):
    id: Optional[int] = None
    bank: NigerianBank
    account_name: str
    account_number: str
    currency: str
    is_active: bool
    account_officer: str
    account_admin: str
    created: datetime
    modified: datetime


class PayStatusEnum(Enum):
    paid = "paid"
    overdue = "overdue"
    due = "due"


class FeeCreate(BaseModel):
    classroom_id: int
    fee_name: str
    amount: Annotated[float, Field(strict=True, gt=0)]
    category: str
    late_fee: float | None = None
    status: PayStatusEnum = Field(default=PayStatusEnum.due)
    due_date: date = Field(description="Due date for fee payment")
    start_date: date = Field(
        description="Start date for fee payment", default=date.today()
    )
    creator_id: int

    @model_validator(mode="after")
    def validate_dates(self: "FeeDto") -> "FeeDto":
        due_date = self.due_date
        start_date = self.start_date
        today = date.today()
        if due_date is not None:
            if due_date <= today:
                raise ValueError("Due date must be greater than today")
            if start_date is not None and due_date <= start_date:
                raise ValueError("Due date must be greater than start date")

        if start_date is not None and start_date < today:
            raise ValueError("Start date cannot be in the past")

        return self


class FeeDto(FeeCreate):
    id: int
    created_on: datetime | None = None
    modified_on: datetime | None = None


class FeeResponse(BaseModel):
    id: int
    classroom_id: int
    fee_name: str
    amount: float
    category: str
    late_fee: float | None = None
    status: PayStatusEnum
    due_date: date
    start_date: date
    creator_id: int
    created_on: datetime | None = None
    modified_on: datetime | None = None
