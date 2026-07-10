from entities import HumanActionDimensions

def test_equality():
    example_1 = HumanActionDimensions(
        comprehend=True,
        act=False,
        do=False,
        communicate=False,
        feel=True
    )

    example_2 = HumanActionDimensions(
        comprehend=True,
        act=False,
        do=False,
        communicate=False,
        feel=True
    )

    assert example_1 == example_2
