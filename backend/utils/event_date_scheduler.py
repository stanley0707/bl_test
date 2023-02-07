import calendar

from typing import Union, Optional, Dict
from enum import Enum
from datetime import timedelta, time, datetime, date

from pydantic import validator, ValidationError, BaseModel

DEFAULT_TIME = {
    "start": "10:00:00",
    "end": "18:00:00",
    "break_start": "12:00:00",
    "break_end": "13:00:00",
}


def get_current_week():
    week_day = datetime.today().weekday()
    past_monday = date.today() - timedelta(days=-week_day, weeks=1)
    return {v: past_monday + timedelta(days=i) for i, v in enumerate(calendar.day_name)}


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


class EventTimeFrame(BaseModel):
    Monday: WorkTimeFrameField = WorkTimeFrameField(**DEFAULT_TIME)
    Tuesday: WorkTimeFrameField = WorkTimeFrameField(**DEFAULT_TIME)
    Wednesday: WorkTimeFrameField = WorkTimeFrameField(**DEFAULT_TIME)
    Thursday: WorkTimeFrameField = WorkTimeFrameField(**DEFAULT_TIME)
    Friday: WorkTimeFrameField = WorkTimeFrameField(**DEFAULT_TIME)
    Saturday: Optional[WorkTimeFrameField]
    Sunday: Optional[WorkTimeFrameField]


class BookingType(str, Enum):
    time_off = "day_off"
    time_work = "work"


class Booking:
    def __init__(
        self,
        booking_id,
        time_start: datetime,
        time_end: datetime,
        booking_type: BookingType,
        title,
    ):
        self.booking_id = booking_id
        self.time_start = time_start
        self.time_end = time_end
        self.booking_type = booking_type
        self.title = title
        self.left_item = None
        self.right_item = None

    def __repr__(self):
        return "<start: {start} | end: {end} | type: {btype} | title: {title}>".format(
            start=self.time_start,
            end=self.time_end,
            btype=self.booking_type,
            title=self.title,
        )


class WorkSchedule:
    def __init__(self, schedule: Dict):
        self.week_frame = EventTimeFrame(**schedule)
        self._schedule = []

    def set_item(
        self, booking_id, time_start, time_end, booking_type: BookingType, title
    ):
        if not self.validate(time_start, time_end):
            raise ValueError("Timeframe intersected or past")
        self._schedule.append(
            Booking(booking_id, time_start, time_end, booking_type, title)
        )

    @staticmethod
    def comparison_conditions(item, time_start, time_end):
        return (
            time_end >= item.time_start <= time_start <= item.time_end >= time_end
            or item.time_end
            >= time_start
            <= item.time_start
            <= time_end
            >= item.time_end
        )

    def validate(self, time_start, time_end):
        for item in self._schedule:
            if self.comparison_conditions(item, time_start, time_end):
                return False
        if work_day := (self.week_frame[time_end.strftime("%A")]):
            return (
                datetime.now() < time_start < time_end
                and time_start.time() >= work_day.start
                and time_end.time() <= work_day.end
            )

        return False

    @property
    def currently(self):
        current_week = get_current_week()
        return {
            d_name: {
                "start": datetime.combine(current_week[d_name], time_frame.start),
                "end": datetime.combine(current_week[d_name], time_frame.end),
                "break_start": datetime.combine(
                    current_week[d_name], time_frame.break_start
                ),
                "break_end": datetime.combine(
                    current_week[d_name], time_frame.break_end
                ),
            }
            for d_name, time_frame in self.week_frame
            if time_frame is not None
        }

    def __repr__(self):
        return str(self._schedule)
