import typing

from hypothesis import assume, given
import hypothesis.strategies as st
import pytest

from smpe.smpe import DynamicGame


class MockGame(DynamicGame):
    def static_profits(self, player_ind, state, actions):
        pass

    def state_evolution(self, state, actions):
        pass


def test_init_incorrect_n_players():
    """
    The constructor should raise an expection when the number of
    playes is smaller than 1.
    """
    with pytest.raises(ValueError):
        MockGame(0, 1, .98, 0)


@given(n_players=st.integers(min_value=1))
def test_init_correct_n_players(n_players):
    """
    The constructor should accept any number of players >= 1.
    """
    MockGame(n_players, 1, .98, 0)


@given(
    # max_value to prevent slowness
    n_players=st.integers(min_value=1, max_value=10),
    n_actions=st.integers(min_value=1))
def test_init_int_n_actions(n_players, n_actions):
    """
    The constructor should accept an int as an argument to n_actions.
    """
    game = MockGame(n_players, n_actions, .98, 0)
    assert isinstance(game.n_actions, typing.Sequence)
    assert len(game.n_actions) == n_players
    for x in game.n_actions:
        assert x == n_actions


@given(
    n_players=st.integers(min_value=1),
    n_actions=st.integers(max_value=0))
def test_init_incorrect_int_n_actions(n_players, n_actions):
    """
    When giving an int to n_actions smaller than 1, this raise an error.
    """
    with pytest.raises(ValueError):
        MockGame(n_players, n_actions, .98, 0)


@given(
    n_players=st.integers(min_value=1),
    n_actions=st.lists(elements=st.integers(min_value=1)))
def test_init_n_actions_list_length(n_players, n_actions):
    """
    The constructor should raise an expection when the size of the
    number of actions list is different from the number of players, and no
    expception otherwise.
    """
    if len(n_actions) != n_players:
        with pytest.raises(ValueError):
            MockGame(n_players, n_actions, .98, 0)
    else:
        MockGame(n_players, n_actions, .98, 0)


@given(n_actions=st.lists(
    elements=st.integers(max_value=0),
    min_size=1
))
def test_init_n_actions_list_negative_el(n_actions):
    """
    The constructor should raise an exception if the number of actions
    for one player is < 1.
    """
    with pytest.raises(ValueError):
        MockGame(len(n_actions), n_actions, .98, 0)


@given(n_actions=st.lists(
    elements=st.integers(min_value=1),
    min_size=1
))
def test_init_n_actions_list_positive_el(n_actions):
    """
    The constructor should raise no exception if the number of actions
    for one player is >= 1.
    """
    MockGame(len(n_actions), n_actions, .98, 0)


@given(
    # max_value to prevent slowness
    n_players=st.integers(min_value=1, max_value=10),
    beta=st.floats(min_value=0.01, max_value=0.99))
def test_init_beta_valid_float(n_players, beta):
    """
    The constructor should accept a single valid float as an argument for beta.
    """
    game = MockGame(n_players, 1, beta, 0)
    assert isinstance(game.beta, typing.Sequence)
    assert len(game.beta) == n_players
    for x in game.beta:
        assert x == beta


@given(beta=st.floats())
def test_init_beta_invalid_float(beta):
    """
    The constructor should raise an exception on a single invalid
    float for beta.
    """
    assume(not 0 < beta < 1)
    with pytest.raises(ValueError):
        MockGame(3, 1, beta, 0)


@given(
    n_players=st.integers(min_value=1),
    beta=st.lists(st.floats(min_value=0.01, max_value=0.99))
)
def test_init_beta_length(n_players, beta):
    """
    When beta is passed as a list, raise an exception when its length
    is not n_players, otherwise not.
    """
    if len(beta) != n_players:
        with pytest.raises(ValueError):
            MockGame(n_players, 1, beta, 0)
    else:
        MockGame(n_players, 1, beta, 0)


@given(beta=st.lists(
    elements=st.floats(min_value=0.01, max_value=0.99),
    min_size=1
))
def test_init_beta_correct_list(beta):
    """
    When beta is a list with correct elements, raise no exception.
    """
    MockGame(len(beta), 1, beta, 0)


@given(beta=st.lists(
    elements=st.floats(),
    min_size=1
))
def test_init_beta_incorrect_list(beta):
    """
    When beta is passed as a list with at least one element not in (0, 1),
    raise an exception.
    """
    assume(not all(0 < x < 1 for x in beta))
    with pytest.raises(ValueError):
        MockGame(len(beta), 1, beta, 0)


@given(
    # max_value to prevent slowness
    n_players=st.integers(min_value=1, max_value=10),
    cost_att=st.floats(min_value=0))
def test_init_cost_att_valid_float(n_players, cost_att):
    """
    The constructor should accept a single valid float as an
    argument for cost_att.
    """
    game = MockGame(n_players, 1, .98, cost_att)
    assert isinstance(game.cost_att, typing.Sequence)
    assert len(game.cost_att) == n_players
    for x in game.cost_att:
        assert x == cost_att


@given(cost_att=st.floats())
def test_init_cost_att_invalid_float(cost_att):
    """
    The constructor should raise an exception on a single invalid
    float for cost_att.
    """
    assume(cost_att < 0)
    with pytest.raises(ValueError):
        MockGame(3, 1, .98, cost_att)


@given(
    n_players=st.integers(min_value=1),
    cost_att=st.lists(st.floats(min_value=0))
)
def test_init_cost_att_length(n_players, cost_att):
    """
    When cost_att is passed as a list, raise an exception when its length
    is not n_players, otherwise not.
    """
    if len(cost_att) != n_players:
        with pytest.raises(ValueError):
            MockGame(n_players, 1, .98, cost_att)
    else:
        MockGame(n_players, 1, .98, cost_att)


@given(cost_att=st.lists(
    elements=st.floats(min_value=0),
    min_size=1
))
def test_init_cost_att_correct_list(cost_att):
    """
    When cost_att is a list with correct elements, raise no exception.
    """
    MockGame(len(cost_att), 1, .98, cost_att)


@given(cost_att=st.lists(
    elements=st.floats(),
    min_size=1
))
def test_init_cost_att_incorrect_list(cost_att):
    """
    When cost_att is passed as a list with at least one element < 0,
    raise an exception.
    """
    assume(not all(x >= 0 for x in cost_att))
    with pytest.raises(ValueError):
        MockGame(len(cost_att), 1, .98, cost_att)
