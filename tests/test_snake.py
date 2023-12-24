import pytest

from src.assets import snake, map
from src.game import game_event


def test_cross_map_x():
    m = map.Map(x = 3, y = 1)
    s = snake.Snake(x = 0, direction = 'R', map = m, max_size = 1)
    input = ['R' for i in range(m.x)]
    for i in input:
        s.Move()

    assert s.x == 0

def test_cross_map_y():
    m = map.Map(x = 1, y = 3)
    s = snake.Snake(y = m.y, direction='D', map = m, max_size = 1)
    input = ['D' for i in range(m.y)]
    for i in input:
        s.Move()

    assert s.y == m.y - 1

def test_collision():
    m = map.Map(x = 3, y = 1)
    s = snake.Snake(map = m, max_size = 4)

    for i in range(m.x):
        s.Move()

    assert s.can_move is False

def test_input_validation():
    s = snake.Snake()

    with pytest.raises(game_event.Error):
        _, err = s.SetDirectionInput('1')
        if err:
            raise(err)

    with pytest.raises(game_event.Error):
        _, err = s.SetDirectionInput('RR')
        if err:
            raise(err)

def test_input_reverse_rule():
    m = map.Map(x = 5,y = 5)
    s = snake.Snake(x = 0, y = 0, direction='R', max_size = 1)

    dir_inputs = ['RL', 'UD', 'LR', 'DU']
    for i in dir_inputs:
        x = i[0]
        for ii in i:
            _, err = s.SetDirectionInput(ii)
        if err:
            raise(err)

        s.Move()
        assert s.direction == x

def test_pick_up_food():
    m = map.Map(x = 2,y = 1)
    s = snake.Snake(x = 0, y = 0, map=m, direction='R', max_size = 1)
    s.food.x, s.food.y = s.x + 1, s.y
    assert len(s.pos) == 1
    assert s.max_size == 1

    s.Move()

    assert len(s.pos) == 2
    assert s.max_size == 2

    #Test full map
    assert s.food.x == -1
    assert s.food.y == -1