from pathlib import Path
from gateways import ParsingSyllabusGateway
from entities import Subject

class XLSXParsingSyllabusGateway(ParsingSyllabusGateway):
    def extract_subject_from_syllabus(self, path: Path) -> Subject:
        """
        Extract the information from an XLSX syllabus file, the subject have the following attributes with their respective titles to search in the file:
        name: "Nombre del Espacio Académico"
        program: "Nombre del Programa Académico"
        objective: "PROPÓSITO  DEL ESPACIO ACADÉMICO (Ver instructivo anexo)"
        problemicCore: "NÚCLEO PROBLÉMICO AL QUE TRIBUTA EL ESPACIO ACADÉMICO"
        didacticStrategies: "PRINCIPALES ESTRATEGIAS DIDÁCTICAS DEL ESPACIO ACADÉMICO  (Ver instructivo anexo)"
        competencies: "COMPETENCIAS, RESULTADOS DE APRENDIZAJE, MECANISMOS DE EVALUACIÓN (Ver instructivo anexo)"

        Every competency has the following attributes:
        name: "COMPETENCIAS"
        humanActionDimensions: "DIMENSIONES DE LA ACCIÓN HUMANA"
        learningResults: "RESULTADOS DE APRENDIZAJE"
        contents: "CONTENIDOS"
        time: "TIEMPOS"
        evaluationMechanisms: "MECANISMOS DE EVALUACIÓN"
        didacticResources: "RECURSOS DIDÁCTICOS"
        """
