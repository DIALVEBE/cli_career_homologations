from pathlib import Path

import pytest

from adapters.parsing_syllabus_gateway.xlsx import XLSXParsingSyllabusGateway

MARKETING_SYLLABUS_PATH = "./marketing_syllabus.xlsx"

@pytest.fixture
def xlsx_parsing_syllabus_gateway():
    return XLSXParsingSyllabusGateway()

def test_marketing_syllabus(xlsx_parsing_syllabus_gateway):
    syllabus_path = Path(MARKETING_SYLLABUS_PATH)

    syllabus = xlsx_parsing_syllabus_gateway.extract_subject_from_syllabus(syllabus_path)
