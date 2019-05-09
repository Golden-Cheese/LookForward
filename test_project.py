from project import Project
from random import randint


def test_cost_n0():
    cost = {}
    p = Project(name="test_cost")
    assert p.cost == cost


def test_cost_simple():
    v = randint(0, 100)
    cost = {'quantity': v}
    p = Project(name="test_cost", cost=cost)
    assert p.cost == cost


def test_cost_double():
    v1 = randint(0, 100)
    v2 = randint(0, 100)
    cost = {'q1': v1, 'q2': v2}
    p = Project(name="test_cost", cost=cost)
    assert p.cost == cost


def test_cost_n1_no():
    v1 = randint(0, 100)
    v2 = randint(0, 100)
    cost = {'q1': v1, 'q2': v2}
    p = Project(name="test_cost", cost=cost)
    p_1 = Project(name="test_cost")
    p.add_subproject(p_1)
    assert p.cost == cost


def test_cost_n1_double():
    v1 = randint(0, 100)
    v2 = randint(0, 100)
    cost = {'q1': v1, 'q2': v2}
    p = Project(name="test_cost")
    p_1 = Project(name="test_cost", cost=cost)
    p.add_subproject(p_1)
    assert p.cost == cost


def test_cost_n2_double_double():
    v1 = randint(0, 100)
    v2 = randint(0, 100)
    cost = {'q1': v1, 'q2': v2}
    p = Project(name="test_cost")
    p_1 = Project(name="test_cost", cost=cost)
    p_2 = Project(name="test_cost", cost=cost)
    p.add_subproject(p_1)
    p.add_subproject(p_2)
    assert p.cost == {'q1': 2 * v1, 'q2': 2 * v2}


def test_cost_n1_n1_double():
    v1 = randint(0, 100)
    v2 = randint(0, 100)
    cost = {'q1': v1, 'q2': v2}
    p = Project(name="test_cost")
    p_1 = Project(name="test_cost")
    p_2 = Project(name="test_cost", cost=cost)
    p.add_subproject(p_1)
    p_1.add_subproject(p_2)
    assert p.cost == cost


def test_cost_n1_double_n1_double():
    v1 = randint(0, 100)
    v2 = randint(0, 100)
    cost = {'q1': v1, 'q2': v2}
    p = Project(name="test_cost")
    p_1 = Project(name="test_cost", cost=cost)
    p_2 = Project(name="test_cost", cost=cost)
    p.add_subproject(p_1)
    p_1.add_subproject(p_2)
    assert p.cost == {'q1': 2 * v1, 'q2': 2 * v2}
