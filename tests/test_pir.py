from typing import Any
from aiohttp import web
from aiohttp.test_utils import TestClient
from pymystrom.pir import MyStromPir
import pytest
from unittest.mock import Mock

MOCK_KEY = web.AppKey("get_settings", Mock)

def handler(mock: Mock, data: Any):
    async def handler(request: web.Request):
        mock(str(request.rel_url))
        return web.json_response(data=data)
    
    return handler

@pytest.fixture
async def cli(aiohttp_client) -> TestClient:
    app = web.Application()
    mock = Mock()

    app[MOCK_KEY] = mock

    app.router.add_route("GET", "/api/v1/settings", handler(mock, {"rest":True,"panel":True,"hap_disable":False,"name":"","temp_offset":-1}))
    app.router.add_route("GET", "/api/v1/action", handler(mock, {"pir":{"generic":"","night":"","twilight":"","day":"","rise":"","fall":""}}))
    app.router.add_route("GET", "/api/v1/settings/pir", handler(mock, {"backoff_time":30,"led_enable":True}))
    app.router.add_route("GET", "/api/v1/sensors", handler(mock, {"motion":False,"light":84,"temperature":23.25}))
    app.router.add_route("GET", "/temp", handler(mock, {"measured":45.68,"compensation":22.43,"compensated":23.25,"offset":0}))
    app.router.add_route("GET", "/api/v1/motion", handler(mock, {"success":True,"motion":False}))
    app.router.add_route("GET", "/api/v1/light", handler(mock, {"success":True,"intensity":11,"day":False,"raw":{"adc0":11,"adc1":1}}))

    return await aiohttp_client(app)

async def test_get_settings(cli):
    host = f"{cli.host}:{cli.port}"
    device = MyStromPir(host=host, session=cli.session)

    await device.get_settings()

    cli.app[MOCK_KEY].assert_called_with("/api/v1/settings")

async def test_get_actions(cli):
    host = f"{cli.host}:{cli.port}"
    device = MyStromPir(host=host, session=cli.session)

    await device.get_actions()

    cli.app[MOCK_KEY].assert_called_with("/api/v1/action")

async def test_get_pir(cli):
    host = f"{cli.host}:{cli.port}"
    device = MyStromPir(host=host, session=cli.session)

    await device.get_pir()

    cli.app[MOCK_KEY].assert_called_with("/api/v1/settings/pir")

async def test_get_sensors_state(cli):
    host = f"{cli.host}:{cli.port}"
    device = MyStromPir(host=host, session=cli.session)

    await device.get_sensors_state()

    cli.app[MOCK_KEY].assert_called_with("/api/v1/sensors")

async def test_get_temperatures(cli):
    host = f"{cli.host}:{cli.port}"
    device = MyStromPir(host=host, session=cli.session)

    await device.get_temperatures()

    cli.app[MOCK_KEY].assert_called_with("/temp")

async def test_get_motion(cli):
    host = f"{cli.host}:{cli.port}"
    device = MyStromPir(host=host, session=cli.session)

    await device.get_motion()

    cli.app[MOCK_KEY].assert_called_with("/api/v1/motion")

async def test_get_light(cli):
    host = f"{cli.host}:{cli.port}"
    device = MyStromPir(host=host, session=cli.session)

    await device.get_light()

    cli.app[MOCK_KEY].assert_called_with("/api/v1/light")