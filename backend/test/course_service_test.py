import os
import sys
from pathlib import Path

import mongomock
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.course_service import CourseService


def test_create_course_unique_enforced():
    client = mongomock.MongoClient()
    service = CourseService(client=client)

    service.create_course("ASE")
    # second insert with same name should raise
    with pytest.raises(ValueError):
        service.create_course("ASE")


def test_create_course_success_assigns_incrementing_ids():
    client = mongomock.MongoClient()
    service = CourseService(client=client)

    service.create_course("Course A")
    service.create_course("Course B")

    courses = service.get_course_list()
    names = [c.name for c in courses]
    assert names == ["Course A", "Course B"]
    ids = [c.course_id for c in courses]
    assert ids == [1, 2]
