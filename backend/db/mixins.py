import json

from utils import WorkSchedule, EventTimeFrame
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import DateTime, Column


class TimeCreateUpdateMixin:
    time_created = Column(
        "time_created", DateTime(timezone=True), server_default=func.now()
    )
    time_updated = Column("time_updated", DateTime(timezone=True), onupdate=func.now())


class ScheduleAccountMixin:
    work_timing = Column("work_timing", JSON, default=EventTimeFrame().json())

    @property
    def work_timing_dict(self):
        return json.loads(self.work_timing)

    @property
    def get_schedule(self):
        return WorkSchedule(self.work_timing)
