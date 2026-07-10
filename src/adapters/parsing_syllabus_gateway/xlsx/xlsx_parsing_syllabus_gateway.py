from pathlib import Path
from gateways import ParsingSyllabusGateway
from entities import Subject

class XLSXParsingSyllabusGateway(ParsingSyllabusGateway):
    def extract_subject_from_syllabus(self, path: Path) -> Subject:
        pass
