# -*- coding: utf-8 -*-

# FLEDGE_BEGIN
# See: http://fledge-iot.readthedocs.io/
# FLEDGE_END

"""Unit test for fledge.plugins.south.cc2650/cc2650.py"""
import copy
import pytest
from unittest.mock import call

from fledge.plugins.south.cc2650.sensortag_cc2650 import SensorTagCC2650
from fledge.plugins.south.cc2650 import cc2650

__author__ = "Amarendra K Sinha"
__copyright__ = "Copyright (c) 2018 Dianomic Systems"
__license__ = "Apache 2.0"
__version__ = "${VERSION}"


_NEW_CONFIG = {
    'plugin': {
        'description': 'TI SensorTag South Plugin',
        'type': 'string',
        'default': 'cc2650'
    },
    'pollInterval': {
        'description': 'The interval between poll calls to the SensorTag poll routine expressed in milliseconds.',
        'type': 'integer',
        'default': '1000'
    },
    'bluetoothAddress': {
        'description': 'Bluetooth address',
        'type': 'string',
        'default': 'C0:92:23:EB:80:05'
    },
    'connectionTimeout': {
        'description': 'BLE connection timeout value in seconds',
        'type': 'integer',
        'default': '3'
    },
    'shutdownThreshold': {
        'description': 'Time in seconds allowed for shutdown to complete the pending tasks',
        'type': 'integer',
        'default': '10'
    },
    'temperatureSensor': {
        'description': 'Enable temperature sensor',
        'type': 'boolean',
        'default': 'true',
    },
    'temperatureSensorName': {
        'description': 'Name of temperature sensor',
        'type': 'string',
        'default': 'temperature',
    },
    'luminanceSensor': {
        'description': 'Enable luminance sensor',
        'type': 'boolean',
        'default': 'false',
    },
    'luminanceSensorName': {
        'description': 'Name of luminance sensor',
        'type': 'string',
        'default': 'luminance',
    },
    'humiditySensor': {
        'description': 'Enable humidity sensor',
        'type': 'boolean',
        'default': 'false',
    },
    'humiditySensorName': {
        'description': 'Name of humidity sensor',
        'type': 'string',
        'default': 'humidity',
    },
    'pressureSensor': {
        'description': 'Enable pressure sensor',
        'type': 'boolean',
        'default': 'false',
    },
    'pressureSensorName': {
        'description': 'Name of pressure sensor',
        'type': 'string',
        'default': 'pressure',
    },
    'movementSensor': {
        'description': 'Enable movement sensor',
        'type': 'boolean',
        'default': 'false',
    },
    'gyroscopeSensorName': {
        'description': 'Name of gyroscope sensor',
        'type': 'string',
        'default': 'gyroscope',
    },
    'accelerometerSensorName': {
        'description': 'Name of accelerometer sensor',
        'type': 'string',
        'default': 'accelerometer',
    },
    'magnetometerSensorName': {
        'description': 'Name of magnetometer sensor',
        'type': 'string',
        'default': 'magnetometer',
    },
    'batteryData': {
        'description': 'Get battery data',
        'type': 'boolean',
        'default': 'false',
    },
    'batterySensorName': {
        'description': 'Name of battery sensor',
        'type': 'string',
        'default': 'battery',
    }
}


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_contract():
    # Evaluates if the plugin has all the required methods
    assert callable(getattr(cc2650, 'plugin_info'))
    assert callable(getattr(cc2650, 'plugin_init'))
    assert callable(getattr(cc2650, 'plugin_poll'))
    assert callable(getattr(cc2650, 'plugin_shutdown'))
    assert callable(getattr(cc2650, 'plugin_reconfigure'))


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_info():
    assert cc2650.plugin_info() == {
        'name': 'TI SensorTag CC2650 plugin',
        'version': '3.0.0',
        'mode': 'poll',
        'type': 'south',
        'interface': '1.0',
        'config': cc2650._DEFAULT_CONFIG
    }


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_init(mocker):
    # GIVEN
    config = copy.deepcopy(cc2650._DEFAULT_CONFIG)
    config['bluetoothAddress']['value'] = config['bluetoothAddress']['default']
    config['connectionTimeout']['value'] = config['connectionTimeout']['default']
    config['shutdownThreshold']['value'] = config['shutdownThreshold']['default']
    config['pollInterval']['value'] = config['pollInterval']['default']
    mocker.patch.object(SensorTagCC2650, "__init__", return_value=None)
    mocker.patch.object(SensorTagCC2650, "is_connected", True)
    mocker.patch.object(SensorTagCC2650, "get_char_handle", return_value=0x0000)
    log_info = mocker.patch.object(cc2650._LOGGER, "info")

    # WHEN
    returned_config = cc2650.plugin_init(config)

    # THEN
    assert "characteristics" in returned_config
    assert "tag" in returned_config
    log_info.assert_called_once_with('SensorTagCC2650 {} Polling initialized'.format(config['bluetoothAddress']['value']))


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_poll(mocker):
    # GIVEN
    config = copy.deepcopy(cc2650._DEFAULT_CONFIG)
    config['bluetoothAddress']['value'] = config['bluetoothAddress']['default']
    config['connectionTimeout']['value'] = config['connectionTimeout']['default']
    config['shutdownThreshold']['value'] = config['shutdownThreshold']['default']
    config['pollInterval']['value'] = config['pollInterval']['default']

    log_info = mocker.patch.object(cc2650._LOGGER, "info")
    log_debug = mocker.patch.object(cc2650._LOGGER, "debug")

    mocker.patch.object(SensorTagCC2650, "__init__", return_value=None)
    mocker.patch.object(SensorTagCC2650, "is_connected", True)
    mocker.patch.object(SensorTagCC2650, "get_char_handle", return_value=0x0000)
    mocker.patch.object(SensorTagCC2650, "reading_iterations", 1)

    returned_config = cc2650.plugin_init(config)

    mocker.patch.object(returned_config['tag'], "char_read_hnd", return_value=None)
    mocker.patch.object(returned_config['tag'], "char_write_cmd", return_value=None)
    mocker.patch.object(returned_config['tag'], "hex_temp_to_celsius", return_value=(None, None))
    mocker.patch.object(returned_config['tag'], "hex_lux_to_lux", return_value=None)
    mocker.patch.object(returned_config['tag'], "hex_humidity_to_rel_humidity", return_value=(None, None))
    mocker.patch.object(returned_config['tag'], "hex_pressure_to_pressure", return_value=None)
    mocker.patch.object(returned_config['tag'], "hex_movement_to_movement", return_value=(
        None, None, None, None, None, None, None, None, None, None))
    mocker.patch.object(returned_config['tag'], "get_battery_level", return_value=None)

    expected_readings_keys = [
        'temperature', 'luxometer', 'humidity', 'pressure', 'gyroscope', 'accelerometer',
        'magnetometer', 'battery'
    ]

    # WHEN
    data = cc2650.plugin_poll(returned_config)

    # THEN
    assert "characteristics" in returned_config
    assert "tag" in returned_config
    for item in data:
        assert 'asset' in item
        assert item['asset'][20:] in expected_readings_keys
        assert 'key' in item
        assert 'timestamp' in item
        assert 'readings' in item

    assert 1 == log_debug.call_count
    log_info.assert_called_once_with('SensorTagCC2650 B0:91:22:EA:79:04 Polling initialized')


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_poll_tag_not_in_handle():
    # GIVEN
    config = copy.deepcopy(cc2650._DEFAULT_CONFIG)
    config['bluetoothAddress']['value'] = config['bluetoothAddress']['default']
    config['connectionTimeout']['value'] = config['connectionTimeout']['default']
    config['shutdownThreshold']['value'] = config['shutdownThreshold']['default']
    config['pollInterval']['value'] = config['pollInterval']['default']

    # WHEN tag is not in handle
    # THEN
    with pytest.raises(RuntimeError):
        cc2650.plugin_poll(config)


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_poll_exception(mocker):
    # GIVEN
    config = copy.deepcopy(cc2650._DEFAULT_CONFIG)
    config['bluetoothAddress']['value'] = config['bluetoothAddress']['default']
    config['connectionTimeout']['value'] = config['connectionTimeout']['default']
    config['shutdownThreshold']['value'] = config['shutdownThreshold']['default']
    config['pollInterval']['value'] = config['pollInterval']['default']
    mocker.patch.object(SensorTagCC2650, "__init__", return_value=None)
    mocker.patch.object(SensorTagCC2650, "is_connected", False)
    mocker.patch.object(SensorTagCC2650, "get_char_handle", return_value=0x0000)
    mocker.patch.object(SensorTagCC2650, "reading_iterations", 1)

    returned_config = cc2650.plugin_init(config)

    # WHEN
    # THEN
    with pytest.raises(RuntimeError):
        cc2650.plugin_poll(returned_config)


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_poll_data_retrieval_error(mocker):
    # GIVEN
    config = copy.deepcopy(cc2650._DEFAULT_CONFIG)
    config['bluetoothAddress']['value'] = config['bluetoothAddress']['default']
    config['connectionTimeout']['value'] = config['connectionTimeout']['default']
    config['shutdownThreshold']['value'] = config['shutdownThreshold']['default']
    config['pollInterval']['value'] = config['pollInterval']['default']
    mocker.patch.object(SensorTagCC2650, "__init__", return_value=None)
    mocker.patch.object(SensorTagCC2650, "is_connected", True)
    mocker.patch.object(SensorTagCC2650, "get_char_handle", return_value=0x0000)
    mocker.patch.object(SensorTagCC2650, "reading_iterations", 1)
    log_exception = mocker.patch.object(cc2650._LOGGER, "exception")
    log_info = mocker.patch.object(cc2650._LOGGER, "info")

    returned_config = cc2650.plugin_init(config)

    # WHEN
    from fledge.services.south import exceptions
    with pytest.raises(exceptions.DataRetrievalError):
        data = cc2650.plugin_poll(returned_config)

    # THEN
    log_info.assert_called_once_with('SensorTagCC2650 B0:91:22:EA:79:04 Polling initialized')
    log_exception.assert_called_once_with("SensorTagCC2650 B0:91:22:EA:79:04 exception: 'NoneType' object has no attribute 'sendline'")


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_reconfigure(mocker):
    # GIVEN
    config = copy.deepcopy(cc2650._DEFAULT_CONFIG)
    config['bluetoothAddress']['value'] = config['bluetoothAddress']['default']
    config['connectionTimeout']['value'] = config['connectionTimeout']['default']
    config['shutdownThreshold']['value'] = config['shutdownThreshold']['default']
    config['pollInterval']['value'] = config['pollInterval']['default']
    log_info = mocker.patch.object(cc2650._LOGGER, "info")

    mocker.patch.object(SensorTagCC2650, "__init__", return_value=None)
    mocker.patch.object(SensorTagCC2650, "is_connected", True)
    mocker.patch.object(SensorTagCC2650, "get_char_handle", return_value=0x0000)
    mocker.patch.object(SensorTagCC2650, "disconnect", return_value=None)
    returned_old_config = cc2650.plugin_init(config)

    # Only bluetoothAddress is changed
    config2 = copy.deepcopy(_NEW_CONFIG)
    config2['bluetoothAddress']['value'] = config2['bluetoothAddress']['default']
    config2['connectionTimeout']['value'] = config2['connectionTimeout']['default']
    config2['shutdownThreshold']['value'] = config2['shutdownThreshold']['default']
    config2['pollInterval']['value'] = config2['pollInterval']['default']

    pstop = mocker.patch.object(cc2650, '_plugin_stop', return_value=True)

    # WHEN
    new_config = cc2650.plugin_reconfigure(returned_old_config, config2)

    # THEN
    for key, value in new_config.items():
        if key in ('characteristics', 'tag', 'restart', 'bluetoothAddress'):
            continue
        assert returned_old_config[key] == value

    # Confirm the new bluetoothAddress
    assert new_config['bluetoothAddress']['value'] == config2['bluetoothAddress']['value']
    assert new_config["restart"] == "yes"
    assert 1 == pstop.call_count

    log_info_call_args = log_info.call_args_list
    assert log_info_call_args[0] == call('SensorTagCC2650 B0:91:22:EA:79:04 Polling initialized')

    args,  kwargs = log_info_call_args[1]
    assert 'new config' in args[0]  # Assert to check if 'new config' text exists when reconfigured

    assert log_info_call_args[2] == call('SensorTagCC2650 C0:92:23:EB:80:05 Polling initialized')
    assert log_info_call_args[3] == call('Restarting CC2650POLL plugin due to change in configuration keys [bluetoothAddress]')


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_reconfigure_elif(mocker):
    # GIVEN
    config = copy.deepcopy(cc2650._DEFAULT_CONFIG)
    config['bluetoothAddress']['value'] = config['bluetoothAddress']['default']
    config['connectionTimeout']['value'] = config['connectionTimeout']['default']
    config['shutdownThreshold']['value'] = config['shutdownThreshold']['default']
    config['pollInterval']['value'] = config['pollInterval']['default']
    log_info = mocker.patch.object(cc2650._LOGGER, "info")

    mocker.patch.object(SensorTagCC2650, "__init__", return_value=None)
    mocker.patch.object(SensorTagCC2650, "is_connected", True)
    mocker.patch.object(SensorTagCC2650, "get_char_handle", return_value=0x0000)
    mocker.patch.object(SensorTagCC2650, "disconnect", return_value=None)
    returned_old_config = cc2650.plugin_init(config)

    # Only shutdownThreshold is changed
    config2 = copy.deepcopy(config)
    config2['shutdownThreshold']['value'] = '30'

    pstop = mocker.patch.object(cc2650, '_plugin_stop', return_value=True)

    # WHEN
    new_config = cc2650.plugin_reconfigure(returned_old_config, config2)

    # THEN
    for key, value in new_config.items():
        if key in ('characteristics', 'tag', 'restart', 'shutdownThreshold'):
            continue
        assert returned_old_config[key] == value
    # Confirm the new shutdownThreshold
    assert new_config['shutdownThreshold']['value'] == config2['shutdownThreshold']['value']

    log_info_call_args = log_info.call_args_list
    assert log_info_call_args[0] == call('SensorTagCC2650 B0:91:22:EA:79:04 Polling initialized')

    args,  kwargs = log_info_call_args[1]
    assert 'new config' in args[0]  # Assert to check if 'new config' text exists when reconfigured

    assert new_config["restart"] == "no"
    assert 0 == pstop.call_count


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_reconfigure_else(mocker):
    # GIVEN
    config = copy.deepcopy(cc2650._DEFAULT_CONFIG)
    config['bluetoothAddress']['value'] = config['bluetoothAddress']['default']
    config['connectionTimeout']['value'] = config['connectionTimeout']['default']
    config['shutdownThreshold']['value'] = config['shutdownThreshold']['default']
    config['pollInterval']['value'] = config['pollInterval']['default']
    log_info = mocker.patch.object(cc2650._LOGGER, "info")

    mocker.patch.object(SensorTagCC2650, "__init__", return_value=None)
    mocker.patch.object(SensorTagCC2650, "is_connected", True)
    mocker.patch.object(SensorTagCC2650, "get_char_handle", return_value=0x0000)
    mocker.patch.object(SensorTagCC2650, "disconnect", return_value=None)
    returned_old_config = cc2650.plugin_init(config)

    # Only shutdownThreshold is changed
    config2 = copy.deepcopy(config)

    pstop = mocker.patch.object(cc2650, '_plugin_stop', return_value=True)

    # WHEN
    new_config = cc2650.plugin_reconfigure(returned_old_config, config2)

    # THEN
    for key, value in new_config.items():
        if key in ('characteristics', 'tag', 'restart'):
            continue
        assert returned_old_config[key] == value

    log_info_call_args = log_info.call_args_list
    assert log_info_call_args[0] == call('SensorTagCC2650 B0:91:22:EA:79:04 Polling initialized')

    args,  kwargs = log_info_call_args[1]
    assert 'new config' in args[0]  # Assert to check if 'new config' text exists when reconfigured

    assert new_config["restart"] == "no"
    assert 0 == pstop.call_count


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin__stop(mocker):
    # GIVEN
    config = copy.deepcopy(cc2650._DEFAULT_CONFIG)
    config['bluetoothAddress']['value'] = config['bluetoothAddress']['default']
    config['connectionTimeout']['value'] = config['connectionTimeout']['default']
    config['shutdownThreshold']['value'] = config['shutdownThreshold']['default']
    config['pollInterval']['value'] = config['pollInterval']['default']
    log_info = mocker.patch.object(cc2650._LOGGER, "info")

    mocker.patch.object(SensorTagCC2650, "__init__", return_value=None)
    mocker.patch.object(SensorTagCC2650, "is_connected", True)
    mocker.patch.object(SensorTagCC2650, "get_char_handle", return_value=0x0000)
    mocker.patch.object(SensorTagCC2650, "disconnect", return_value=None)

    returned_config = cc2650.plugin_init(config)

    # WHEN
    cc2650._plugin_stop(returned_config)

    # THEN
    calls = [call('SensorTagCC2650 {} Disconnected.'.format(config['bluetoothAddress']['value'])),
             call('SensorTagCC2650 {} Polling initialized'.format(config['bluetoothAddress']['value']))]
    log_info.assert_has_calls(calls, any_order=True)


@pytest.allure.feature("unit")
@pytest.allure.story("plugin", "south", "cc2650")
def test_plugin_shutdown(mocker):
    # GIVEN
    config = copy.deepcopy(cc2650._DEFAULT_CONFIG)
    config['bluetoothAddress']['value'] = config['bluetoothAddress']['default']
    config['connectionTimeout']['value'] = config['connectionTimeout']['default']
    config['shutdownThreshold']['value'] = config['shutdownThreshold']['default']
    config['pollInterval']['value'] = config['pollInterval']['default']
    log_info = mocker.patch.object(cc2650._LOGGER, "info")

    mocker.patch.object(SensorTagCC2650, "__init__", return_value=None)
    mocker.patch.object(SensorTagCC2650, "is_connected", True)
    mocker.patch.object(SensorTagCC2650, "get_char_handle", return_value=0x0000)
    mocker.patch.object(SensorTagCC2650, "disconnect", return_value=None)

    returned_config = cc2650.plugin_init(config)

    # WHEN
    cc2650.plugin_shutdown(returned_config)

    # THEN
    calls = [call('SensorTagCC2650 {} Disconnected.'.format(config['bluetoothAddress']['value'])),
             call('CC2650 poll plugin shut down.'),
             call('SensorTagCC2650 {} Polling initialized'.format(config['bluetoothAddress']['value']))]
    log_info.assert_has_calls(calls, any_order=True)
