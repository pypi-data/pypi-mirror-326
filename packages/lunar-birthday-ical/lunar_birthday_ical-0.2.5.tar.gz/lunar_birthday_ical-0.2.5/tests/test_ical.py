import datetime
import zoneinfo

import yaml
from pathlib import Path

from icalendar import Calendar, Event, vCalAddress

from lunar_birthday_ical.ical import (
    add_attendees_to_event,
    add_event_to_calendar,
    add_reminders_to_event,
    create_calendar,
    get_local_datetime,
    local_datetime_to_utc_datetime,
)
from tests.__init__ import config


def test_get_local_datetime():
    local_date = "2023-10-01"
    local_time = "12:00:00"
    timezone = zoneinfo.ZoneInfo("UTC")
    result = get_local_datetime(local_date, local_time, timezone)
    expected = datetime.datetime(2023, 10, 1, 12, 0, tzinfo=timezone)
    assert result == expected


def test_local_datetime_to_utc_datetime():
    local_datetime = datetime.datetime(
        2023, 10, 1, 12, 0, tzinfo=zoneinfo.ZoneInfo("Asia/Shanghai")
    )
    result = local_datetime_to_utc_datetime(local_datetime)
    expected = datetime.datetime(2023, 10, 1, 4, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
    assert result == expected


def test_add_reminders_to_event():
    event = Event()
    reminders = [1, 2]
    summary = "Test Event"
    add_reminders_to_event(event, reminders, summary)
    assert len(event.subcomponents) == 2


def test_add_attendees_to_event_one():
    event = Event()
    attendees = ["test@example.com"]
    add_attendees_to_event(event, attendees)
    assert (
        len(
            [event.get("ATTENDEE")]
            if isinstance(event.get("ATTENDEE"), vCalAddress)
            else event.get("ATTENDEE")
        )
        == 1
    )


def test_add_attendees_to_event_multi():
    event = Event()
    attendees = ["test@example.com", "test@example.net"]
    add_attendees_to_event(event, attendees)
    assert (
        len(
            [event.get("ATTENDEE")]
            if isinstance(event.get("ATTENDEE"), vCalAddress)
            else event.get("ATTENDEE")
        )
        == 2
    )


def test_add_event_to_calendar():
    calendar = Calendar()
    dtstart = datetime.datetime(2023, 10, 1, 12, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
    dtend = dtstart + datetime.timedelta(hours=1)
    summary = "Test Event"
    reminders = [1]
    attendees = ["test@example.com"]
    add_event_to_calendar(calendar, dtstart, dtend, summary, reminders, attendees)
    assert len(calendar.subcomponents) == 1


def test_create_calendar(tmp_path: Path):
    calendar_name = "test-calendar"
    config_file = tmp_path / f"{calendar_name}.yaml"
    output = tmp_path / f"{calendar_name}.ics"
    with config_file.open("w") as f:
        f.write(yaml.safe_dump(config))
    create_calendar(config_file, output)
    assert output.exists()
    with output.open("rb") as f:
        calendar_data = f.read()
    calendar = Calendar.from_ical(calendar_data)
    assert len(calendar.subcomponents) > 0
    assert calendar.get("X-WR-CALNAME") == calendar_name
