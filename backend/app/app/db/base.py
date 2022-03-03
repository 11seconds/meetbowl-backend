# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.color import Color  # noqa
from app.models.scheduleblock import ScheduleBlock  # noqa
from app.models.timetable import TimeTable  # noqa
from app.models.user import User  # noqa
