import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID

from handlers.player.configurar_ubicacion import (
    handle_address_configuration,
    process_address_step,
    process_radius_step,
)

TEST_CHAT_ID = 12345
TEST_USER_PUBLIC_ID = UUID("11111111-2222-3333-4444-555555555555")
TEST_ADDRESS = "Av. Paseo Colón 850, Buenos Aires"
TEST_RADIUS = "<10"
TEST_PARSED_RADIUS = 10


@pytest.fixture
def message_mock():
    message = MagicMock()
    message.chat.id = TEST_CHAT_ID
    message.text = TEST_ADDRESS
    return message


@pytest.fixture
def bot_mock():
    bot = MagicMock()
    bot.send_message.return_value = MagicMock()
    return bot


@pytest.fixture
def users_service_mock():
    mock = MagicMock()
    mock.get_user_info.return_value = {
        "data": [{"public_id": TEST_USER_PUBLIC_ID}]
    }
    return mock


@pytest.fixture
def players_service_mock():
    mock = MagicMock()
    mock.update_partial_player.return_value = True
    return mock


@pytest.fixture
def patched_users_service(users_service_mock):
    with patch("handlers.player.configurar_ubicacion.users_service", users_service_mock):
        yield users_service_mock


@pytest.fixture
def patched_players_service(players_service_mock):
    with patch("handlers.player.configurar_ubicacion.players_service", players_service_mock):
        yield players_service_mock


def test_handle_address_configuration_success(patched_users_service, message_mock, bot_mock):
    handle_address_configuration(message_mock, bot_mock)

    patched_users_service.get_user_info.assert_called_once_with(TEST_CHAT_ID)
    bot_mock.send_message.assert_called_once_with(
        TEST_CHAT_ID, "Por favor, ingrese la ubicación donde desea jugar:"
    )
    bot_mock.register_next_step_handler.assert_called_once()


def test_handle_address_configuration_no_user_data(patched_users_service, message_mock, bot_mock):
    patched_users_service.get_user_info.return_value = {"data": []}

    with pytest.raises(IndexError):
        handle_address_configuration(message_mock, bot_mock)

    patched_users_service.get_user_info.assert_called_once_with(TEST_CHAT_ID)


def test_process_address_step_success(patched_players_service, message_mock, bot_mock):
    message_mock.text = TEST_ADDRESS

    process_address_step(message_mock, bot_mock, TEST_USER_PUBLIC_ID)

    patched_players_service.update_partial_player.assert_called_once_with(
        TEST_USER_PUBLIC_ID, {"address": TEST_ADDRESS}
    )
    assert bot_mock.send_message.call_count == 2
    bot_mock.register_next_step_handler.assert_called_once()


def test_process_address_step_failure(patched_players_service, message_mock, bot_mock):
    patched_players_service.update_partial_player.return_value = False
    message_mock.text = TEST_ADDRESS

    process_address_step(message_mock, bot_mock, TEST_USER_PUBLIC_ID)

    patched_players_service.update_partial_player.assert_called_once_with(
        TEST_USER_PUBLIC_ID, {"address": TEST_ADDRESS}
    )
    bot_mock.send_message.assert_called_once_with(
        TEST_CHAT_ID,
        "No se pudo guardar la ubicación. Por favor, inténtelo de nuevo.",
    )
    bot_mock.register_next_step_handler.assert_not_called()


def test_process_radius_step_success(patched_players_service, message_mock, bot_mock):
    patched_players_service.update_partial_player.return_value = True
    message_mock.text = TEST_RADIUS

    process_radius_step(message_mock, bot_mock, TEST_USER_PUBLIC_ID)

    patched_players_service.update_partial_player.assert_called_once_with(
        TEST_USER_PUBLIC_ID, {"search_range_km": TEST_PARSED_RADIUS}
    )
    bot_mock.send_message.assert_called_once_with(
        TEST_CHAT_ID, f"¡Radio de {TEST_RADIUS} km guardado con éxito!"
    )


def test_process_radius_step_failure(patched_players_service, message_mock, bot_mock):
    patched_players_service.update_partial_player.return_value = False
    message_mock.text = TEST_RADIUS

    process_radius_step(message_mock, bot_mock, TEST_USER_PUBLIC_ID)

    patched_players_service.update_partial_player.assert_called_once_with(
        TEST_USER_PUBLIC_ID, {"search_range_km": TEST_PARSED_RADIUS}
    )
    bot_mock.send_message.assert_called_once_with(
        TEST_CHAT_ID, "No se pudo guardar el radio. Por favor, inténtelo de nuevo."
    )


def test_process_radius_step_invalid_format(patched_players_service, message_mock, bot_mock):
    message_mock.text = "invalid_radius"

    with pytest.raises(ValueError):
        process_radius_step(message_mock, bot_mock, TEST_USER_PUBLIC_ID)

    patched_players_service.update_partial_player.assert_not_called()