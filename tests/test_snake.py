import pytest

from src.assets import snake, map
from src.game import game_event


def test_cross_map_x():
    m = map.Map(x = 2, y = 1)
    s = snake.Snake(x = 0, direction = 'R', map = m, max_size = 1)
    input = ['R' for i in range(m.x + 1)]
    for i in input:
        s.Move()

    assert s.x == 0

def test_cross_map_y():
    m = map.Map(x = 1, y = 2)
    s = snake.Snake(y = m.y, direction='D', map = m, max_size = 1)
    input = ['D' for i in range(m.y + 1)]
    for i in input:
        s.Move()

    assert s.y == m.y

def test_collision():
    m = map.Map(x = 5, y =5)
    s = snake.Snake(map = m, max_size = 4)

    dir_input = 'UURDL'

    with pytest.raises(game_event.GameOver):
        for i in dir_input:
            _, err = s.SetDirectionInput(i)
            if err:
                raise(err)

            s.Move()

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