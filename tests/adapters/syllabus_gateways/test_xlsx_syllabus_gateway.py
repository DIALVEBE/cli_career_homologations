from pathlib import Path

import pytest

from adapters.parsing_syllabus_gateway.xlsx import XLSXParsingSyllabusGateway
from entities import Competency, HumanActionDimensions, Subject

MARKETING_SYLLABUS_PATH = "tests/adapters/syllabus_gateways/marketing_syllabus.xlsx"

MARKETING_SUBJECT = Subject(
    name="Fundamentos de marketing y transformación digital",
    program="Marketing y Transformación digital",
    objective="Proporcionar a los estudiantes una comprensión profunda y amplia de los conceptos fundamentales del marketing y la transformación digital, así como de las herramientas y tecnologías disponibles para llevar a cabo campañas de marketing en línea efectivas. Al finalizar el curso, los estudiantes podrán comprender cómo se pueden aplicar los principios del marketing y la transformación digital para abordar los desafíos actuales del mercado, mejorar la visibilidad de la marca y el engagement del cliente, y aumentar la eficacia y eficiencia de los procesos de marketing en línea.",
    problemicCore="Núcleo problémico: Marketing Para gestionar el entorno de mercadeo digital, es necesario contar con una comprensión sólida de los fundamentos del marketing y la transformación digital. Esto implica entender cómo los consumidores interactúan con la tecnología y cómo la tecnología está transformando los mercados. Además, se deben conocer las herramientas y técnicas necesarias para desarrollar una estrategia de marketing efectiva en el entorno digital, incluyendo la segmentación de audiencia, la creación de contenidos atractivos y la medición de resultados. También es fundamental estar al tanto de las tendencias en marketing digital, para poder adaptarse a los cambios en el mercado y mantener una ventaja competitiva. En resumen, la gestión efectiva del entorno de mercadeo digital requiere una comprensión profunda de los fundamentos del marketing y la transformación digital, así como de las herramientas y tendencias en el mercado digital.",
    didacticStrategies="El desarrollo metodológico del espacio académico se basa en actividades que van de lo sencillo a lo complejo, de lo teórico a lo práctico y de lo conceptual a lo experimental; estas actividades se clasifican en actividades del proceso de enseñanza y aprendizaje y actividades de evaluación. Este proceso se lleva a cabo mediante los siguientes puntos:   Clases magistrales: El docente explica de forma general los conceptos relacionados con los contenidos temáticos. Trabajo Colaborativo: En el cual los estudiantes en grupo definan tareas, dimensiones, fases o procesos, de manera que las tareas asignadas puedan ser desarrolladas partir del aporte individual de estudiantes y su correspondiente ensamblaje en las entregas finales.  Aprendizaje Basado en Problemas: En el cual los estudiantes, mediante estudios de caso puedan identificar problemáticas, analizarlas según las metodologías ambientales aprendidas en el aula, y propongan estrategias para su solución.  Aprendizaje basado en análisis de casos: En el cual el docente plantea un caso de estudio, creando marcos situacionales, temporales y temáticos, al cual los estudiantes aplican los conocimientos adquiridos, para presentar soluciones o posturas frente al caso, motivando el pensamiento crítico, la autonomía y la argumentación.",
    competencies=[
        Competency(
            name="Comprender los fundamentos del marketing y la transformación digital para aplicarlos en la creación de estrategias de marketing efectivas.",
            humanActionDimensions=HumanActionDimensions(
                comprehend=True,
                act=False,
                do=False,
                communicate=False,
                feel=True
            ),
            learningResults=[
                "Identifica los elementos clave del marketing para la creación de estrategias de marketing efectivas.",
                "Comprende los conceptos de segmentación, targeting y posicionamiento para aplicarlos en la creación de estrategias de marketing efectivas..",
                "Aplica las herramientas de marketing a situaciones empresariales para usarlas en la creación de estrategias de marketing efectivas."
            ],
            contents="Unidad 1:  Fundamentos de marketing Subtemas: Conceptos básicos del marketing y la transformación digital / El papel del marketing y la transformación digital en la estrategia empresarial / Conceptos basicos de marketing / Segmentación, focalización y posicionamiento / Mezcla de marketing: producto, precio, promoción y distribución.",
            time="4 semanas",
            evaluationMechanisms="ENTREGABLE POR CORTE:  Parcial – quices - talleres y demás actividades de clase o autónomas.",
            didacticResources="Bases de datos de la Biblioteca - CRAI USTA Material entregado por el Docente Documentos sugeridos: Vacchiano, C., & Alcaide, J. C. (2018). Transformación digital: La nueva realidad del marketing. Lid Editorial. Gabriel, M. (2018). El nuevo marketing en la era digital. Gestión 2000. \"Marketing digital: Conceptos básicos y estrategias\" de Marcela B. Pérez Silva y María Isabel Otero García (2016) en Revista de Ciencias Sociales, 22(4), 676-689.",
        ),
        Competency(
            name="Conocer el impacto de la transformación digital en el marketing para aplicarlo en el desarrollo de estrategias de marketing efectivas.",
            humanActionDimensions=HumanActionDimensions(
                comprehend=True,
                act=False,
                do=False,
                communicate=False,
                feel=True,
            ),
            learningResults=[
                "Reconoce las oportunidades y desafíos de la transformación digital en el marketing para el desarrollo de estrategias de marketing.",
                "Comprende la relación entre el marketing y las tecnologías digitales para el uso desarrollo de estrategias.",
                "Identifica las herramientas digitales utilizadas en el marketing digital para aplicarlas en proyectos de marketing.",
            ],
            contents="Unidad 2:  Fundamentos transformación digital Subtemas: Transformación digital y marketing / Tecnologías digitales y marketing / Marketing digital y herramientas digitales.",
            time="4 semanas",
            evaluationMechanisms="ENTREGABLE POR CORTE:  Parcial – quices - talleres y demás actividades de clase o autónomas.",
            didacticResources="Bases de datos de la Biblioteca - CRAI USTA Material entregado por el Docente Documentos sugeridos: Kotler, P., Kartajaya, H., & Setiawan, I. (2017). Marketing 4.0: Del tradicional al digital. Deusto. Polo, F., & Somalo, N. (2017). La transformación digital de las empresas. Anaya Multimedia. \"La era digital: Impacto en el marketing y la publicidad\" de Fernando Villalba López (2017) en Cuestiones de Marketing: Revista de Investigación en Marketing y Management, 22(1), 1-17."
        ),
        Competency(
            name="Desarrollar habilidades de análisis de datos en el contexto del marketing para tomar decisiones informadas.",
            humanActionDimensions=HumanActionDimensions(
                comprehend=False,
                act=True,
                do=True,
                communicate=True,
                feel=False,
            ),
            learningResults=[
                "Comprende el papel de los datos en el marketing para tomar decisiones informadas.",
                "Identifica las herramientas y técnicas para el análisis de datos. ",
                "Analiza datos para la toma de decisiones de marketing."
            ],
            contents="Unidad 3:  Analisis de datos Subtemas:Datos y marketing / Herramientas y tecnicas de analisis de datos / Toma de decisiones de marketing basadas en datos.",
            time="4 semanas",
            evaluationMechanisms="ENTREGABLE POR CORTE:  Parcial – quices - talleres y demás actividades de clase o autónomas. Taller caso practico",
            didacticResources="Bases de datos de la Biblioteca - CRAI USTA Material entregado por el Docente Documentos sugeridos: Palomo Zurdo, R. (2016). Marketing Analytics: Big Data en la toma de decisiones empresariales. Ediciones Pirámide. \"Inteligencia Artificial: Su aplicación al marketing\" de María de la Paz Rubio Lapaz y Ana Rubio López (2018) en El profesional de la información, 27(5), 1101-1111. \"Transformación digital y marketing: De la teoría a la práctica\" de José Manuel Ortega Egea y Alicia Izquierdo Yusta (2019) en Revista Internacional de Investigación en Comunicación Audiovisual, 7(14), 52-71."
        ),
        Competency(
            name="Identificar la relación entre el marketing y la experiencia del cliente para mejorar la satisfacción y lealtad de los clientes.",
            humanActionDimensions=HumanActionDimensions(
                comprehend=False,
                act=True,
                do=True,
                communicate=False,
                feel=True,
            ),
            learningResults=[
                "Identifica la importancia de la experiencia del cliente en el marketing para mejorar la satisfacción de los clientes.",
                "Comprende los componentes de la experiencia del cliente para mejorar la lealtad de los clientes.",
                "Desarrolla habilidades para mejorar la experiencia del cliente en el marketing para mejorar  su relación con los clientes."
            ],
            contents="Unidad 4:  Experiencia del cliente Subtemas: Experiencia del cliente y marketing / Componentes de la experiencia del cliente /  Mejora de la experiencia del cliente en el marketing.",
            time="4 semanas",
            evaluationMechanisms="ENTREGABLE POR CORTE:  Parcial – quices - talleres y demás actividades de clase o autónomas. Estudio de caso",
            didacticResources="Bases de datos de la Biblioteca - CRAI USTA Material entregado por el Docente Documentos sugeridos: Kotler, P. (2012). Marketing 3.0: Del producto al cliente. Deusto. \"Transformación digital: Tendencias y oportunidades para el marketing\" de Esteban Kolsky (2017) en Harvard Business Review en Español, 95-103. \"Marketing de contenidos: Creación de valor en la era digital\" de Cristina Salvador (2015) en Investigación y Marketing, 127, 4-17.",
        ),
    ]
)

@pytest.fixture
def xlsx_parsing_syllabus_gateway():
    return XLSXParsingSyllabusGateway()

def test_marketing_syllabus(xlsx_parsing_syllabus_gateway):
    syllabus_path = Path(MARKETING_SYLLABUS_PATH)

    want = MARKETING_SUBJECT

    got = xlsx_parsing_syllabus_gateway.extract_subject_from_syllabus(syllabus_path)

    assert want.name == got.name
    assert want.program == got.program
    assert want.problemicCore == got.problemicCore
    assert want.didacticStrategies == got.didacticStrategies

    for index, want_competency in enumerate(want.competencies):
        got_competency = got.competencies[index]

        assert want_competency.name == got_competency.name

        assert want_competency.humanActionDimensions == got_competency.humanActionDimensions

        assert _clean_list(want_competency.learningResults) == _clean_list(got_competency.learningResults)
        assert _clean(want_competency.contents) == _clean(got_competency.contents)
        assert _clean(want_competency.time) == _clean(got_competency.time)
        assert _clean(want_competency.evaluationMechanisms) == _clean(got_competency.evaluationMechanisms)
        assert _clean(want_competency.didacticResources) == _clean(got_competency.didacticResources)


def _clean_list(values: list[str]) -> list[str]:
    return [value.strip() for value in values]


def _clean(value: str) -> str:
    return value.strip()
