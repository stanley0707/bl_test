from typing import Union, Optional
from datetime import time, datetime

from pydantic import validator, ValidationError, BaseModel

DEFAULT_TIME = {
    "start": "10:00:00",
    "end": "18:00:00",
    "break_start": "12:00:00",
    "break_end": "13:00:00",
}


class WorkTimeFrameField(BaseModel):
    start: Union[str, time]
    end: Union[str, time]
    break_start: Union[str, time]
    break_end: Union[str, time]

    @validator("*", pre=True)
    def to_datetime(cls, v):
        try:
            return datetime.strptime(v, "%H:%M:%S").time()
        except Exception as exc:
            raise ValidationError() from exc


class WorkDayFrame(BaseModel):
    Monday: WorkTimeFrameField = WorkTimeFrameField(**DEFAULT_TIME)
    Tuesday: WorkTimeFrameField = WorkTimeFrameField(**DEFAULT_TIME)
    Wednesday: WorkTimeFrameField = WorkTimeFrameField(**DEFAULT_TIME)
    Thursday: WorkTimeFrameField = WorkTimeFrameField(**DEFAULT_TIME)
    Friday: WorkTimeFrameField = WorkTimeFrameField(**DEFAULT_TIME)
    Saturday: Optional[WorkTimeFrameField]
    Sunday: Optional[WorkTimeFrameField]
