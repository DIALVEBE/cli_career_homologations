from services import parse_academic_plan_text


def test_parse_academic_plan_text_extracts_courses_and_credits():
    text = """
    •Cálculo diferencial | 3 c
    •Gestión financiera de proyectos | Virtual | 2 c
    •Lengua extranjera I | 2 c
    """

    courses = parse_academic_plan_text(text)

    assert [(course.name, course.credits) for course in courses] == [
        ("Cálculo diferencial", 3),
        ("Gestión financiera de proyectos", 2),
        ("Lengua extranjera I", 2),
    ]
