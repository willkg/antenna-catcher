import sys

from falcon import testing
from freezegun import freeze_time
import pytest

from catcher.main import get_app


@pytest.fixture()
def client():
    return testing.TestClient(get_app())


def test_bad_post(client):
    res = client.simulate_post('/crashid', query_string='crashid=foo')
    assert res.status_code == 400
    assert res.content == b'Bad crashid: foo'


def test_post(client):
    res = client.simulate_post('/crashid', query_string='crashid=00000019-c413-4ada-a50b-4eab40170120')
    assert res.status_code == 200
    assert res.content == b'Ok'


@freeze_time('2017-03-06 16:30:00')
def test_get(client):
    # Post a crashid and then get it
    res = client.simulate_post('/crashid', query_string='crashid=00000019-c413-4ada-a50b-4eab40170120')
    assert res.status_code == 200
    assert res.content == b'Ok'

    res = client.simulate_get('/crashid')
    assert res.status_code == 200
    assert res.content == b'Crash ids: 1\n2017-03-06 16:30:00: 00000019-c413-4ada-a50b-4eab40170120'

    # Post a second and get both
    res = client.simulate_post('/crashid', query_string='crashid=11111111-c413-4ada-a50b-4eab40170120')
    assert res.status_code == 200
    assert res.content == b'Ok'

    res = client.simulate_get('/crashid')
    assert res.status_code == 200
    assert (
        res.content ==
        b'Crash ids: 2\n'
        b'2017-03-06 16:30:00: 00000019-c413-4ada-a50b-4eab40170120\n'
        b'2017-03-06 16:30:00: 11111111-c413-4ada-a50b-4eab40170120'
    )
