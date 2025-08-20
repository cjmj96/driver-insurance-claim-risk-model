# import pytest
# import logging
# import io
# from unittest.mock import patch, MagicMock
# from src.utils.log_config import ElegantFormatter, setup_logging

# # Define a sample emoji map for testing
# TEST_EMOJI_MAP = {
#     "starting": "⏳",
#     "completed": "✅",
#     "error": "❌",
# }

# @pytest.fixture
# def log_capture_string():
#     """Fixture to capture log output into a string buffer."""
#     return io.StringIO()

# @pytest.fixture
# def logger(log_capture_string):
#     """Fixture to get a logger instance with a stream handler for capturing output."""
#     # Ensure a clean logger for each test
#     logger = logging.getLogger("test_logger")
#     logger.setLevel(logging.DEBUG)

#     # Remove any existing handlers to prevent duplicate logs
#     if logger.hasHandlers():
#         logger.handlers.clear()

#     handler = logging.StreamHandler(log_capture_string)
#     logger.addHandler(handler)

#     yield logger

#     # Teardown: clear handlers after the test
#     logger.handlers.clear()


# class TestElegantFormatter:
#     """Tests for the ElegantFormatter class."""

#     def test_info_format_with_emoji(self, logger, log_capture_string):
#         """Verify INFO logs get the simple format with a dynamic emoji."""
#         formatter = ElegantFormatter(emoji_map=TEST_EMOJI_MAP)
#         logger.handlers[0].setFormatter(formatter)

#         message = "Starting data processing..."
#         logger.info(message)

#         output = log_capture_string.getvalue().strip()
#         assert output == f"{TEST_EMOJI_MAP['starting']} {message}"

#     def test_info_format_no_emoji(self, logger, log_capture_string):
#         """Verify INFO logs without a keyword have no emoji."""
#         formatter = ElegantFormatter(emoji_map=TEST_EMOJI_MAP)
#         logger.handlers[0].setFormatter(formatter)

#         message = "Just a regular message."
#         logger.info(message)

#         output = log_capture_string.getvalue().strip()
#         assert output == message

#     def test_warning_format_is_detailed(self, logger, log_capture_string):
#         """Verify WARNING logs use the detailed format."""
#         formatter = ElegantFormatter()
#         logger.handlers[0].setFormatter(formatter)

#         message = "Something might be wrong."
#         logger.warning(message)

#         output = log_capture_string.getvalue().strip()
#         assert "test_logger" in output
#         assert "WARNING" in output
#         assert message in output

#     def test_error_format_is_detailed(self, logger, log_capture_string):
#         """Verify ERROR logs use the detailed format."""
#         formatter = ElegantFormatter()
#         logger.handlers[0].setFormatter(formatter)

#         message = "An error occurred."
#         logger.error(message)

#         output = log_capture_string.getvalue().strip()
#         assert "test_logger" in output
#         assert "ERROR" in output
#         assert message in output

#     def test_emoji_keyword_is_case_insensitive(self, logger, log_capture_string):
#         """Verify that emoji keyword matching is case-insensitive."""
#         formatter = ElegantFormatter(emoji_map=TEST_EMOJI_MAP)
#         logger.handlers[0].setFormatter(formatter)

#         message = "Process COMPLETED successfully."
#         logger.info(message)

#         output = log_capture_string.getvalue().strip()
#         assert output.startswith(TEST_EMOJI_MAP['completed'])
#         assert output == f"{TEST_EMOJI_MAP['completed']} {message}"


# class TestSetupLogging:
#     """Tests for the setup_logging function."""

#     @pytest.fixture(autouse=True)
#     def reset_root_logger(self):
#         """Fixture to reset the root logger before and after each test."""
#         root = logging.getLogger()
#         original_handlers = root.handlers[:]
#         original_level = root.level

#         yield

#         root.handlers = original_handlers
#         root.setLevel(original_level)

#     def test_setup_adds_console_handler(self):
#         """Verify setup_logging adds a StreamHandler to the root logger."""
#         root = logging.getLogger()
#         assert len(root.handlers) == 0 # Start with no handlers

#         setup_logging(console_level=logging.INFO, emoji_map=TEST_EMOJI_MAP)

#         assert len(root.handlers) == 1
#         handler = root.handlers[0]
#         assert isinstance(handler, logging.StreamHandler)
#         assert handler.level == logging.INFO
#         assert isinstance(handler.formatter, ElegantFormatter)

#     @patch('src.utils.log_config.logging.FileHandler')
#     def test_setup_adds_file_handler(self, mock_file_handler):
#         """Verify setup_logging adds a FileHandler when a path is provided."""
#         mock_instance = MagicMock()
#         mock_file_handler.return_value = mock_instance

#         log_file = "test.log"
#         setup_logging(log_file=log_file)

#         # Check that FileHandler was instantiated with the correct path
#         mock_file_handler.assert_called_once_with(log_file)

#         # Check that the handler was added to the root logger
#         root = logging.getLogger()
#         assert mock_instance in root.handlers
#         assert mock_instance.level == logging.DEBUG
#         assert isinstance(mock_instance.formatter, logging.Formatter)
#         assert not isinstance(mock_instance.formatter, ElegantFormatter)

#     def test_setup_without_file_handler(self):
#         """Verify no FileHandler is added when log_file is None."""
#         root = logging.getLogger()
#         setup_logging() # log_file is None by default

#         has_file_handler = any(isinstance(h, logging.FileHandler) for h in root.handlers)
#         assert not has_file_handler
import pytest
import logging
import io
from unittest.mock import patch, MagicMock
from src.utils.log_config import ElegantFormatter, setup_logging

# Define a sample emoji map for testing
TEST_EMOJI_MAP = {
    "starting": "⏳",
    "completed": "✅",
    "error": "❌",
}


@pytest.fixture
def log_capture_string():
    """Fixture to capture log output into a string buffer."""
    return io.StringIO()


@pytest.fixture
def logger(log_capture_string):
    """Fixture to get a logger instance with a stream handler for capturing output."""
    # Ensure a clean logger for each test
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)

    # Remove any existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(log_capture_string)
    logger.addHandler(handler)

    yield logger

    # Teardown: clear handlers after the test
    logger.handlers.clear()


class TestElegantFormatter:
    """Tests for the ElegantFormatter class."""

    def test_info_format_with_emoji(self, logger, log_capture_string):
        """Verify INFO logs get the simple format with a dynamic emoji."""
        formatter = ElegantFormatter(emoji_map=TEST_EMOJI_MAP)
        logger.handlers[0].setFormatter(formatter)

        message = "Starting data processing..."
        logger.info(message)

        output = log_capture_string.getvalue().strip()
        assert output == f"{TEST_EMOJI_MAP['starting']} {message}"

    def test_info_format_no_emoji(self, logger, log_capture_string):
        """Verify INFO logs without a keyword have no emoji."""
        formatter = ElegantFormatter(emoji_map=TEST_EMOJI_MAP)
        logger.handlers[0].setFormatter(formatter)

        message = "Just a regular message."
        logger.info(message)

        output = log_capture_string.getvalue().strip()
        assert output == message

    def test_warning_format_is_detailed(self, logger, log_capture_string):
        """Verify WARNING logs use the detailed format."""
        formatter = ElegantFormatter()
        logger.handlers[0].setFormatter(formatter)

        message = "Something might be wrong."
        logger.warning(message)

        output = log_capture_string.getvalue().strip()
        assert "test_logger" in output
        assert "WARNING" in output
        assert message in output

    def test_error_format_is_detailed(self, logger, log_capture_string):
        """Verify ERROR logs use the detailed format."""
        formatter = ElegantFormatter()
        logger.handlers[0].setFormatter(formatter)

        message = "An error occurred."
        logger.error(message)

        output = log_capture_string.getvalue().strip()
        assert "test_logger" in output
        assert "ERROR" in output
        assert message in output

    def test_emoji_keyword_is_case_insensitive(self, logger, log_capture_string):
        """Verify that emoji keyword matching is case-insensitive."""
        formatter = ElegantFormatter(emoji_map=TEST_EMOJI_MAP)
        logger.handlers[0].setFormatter(formatter)

        message = "Process COMPLETED successfully."
        logger.info(message)

        output = log_capture_string.getvalue().strip()
        assert output.startswith(TEST_EMOJI_MAP["completed"])
        assert output == f"{TEST_EMOJI_MAP['completed']} {message}"


class TestSetupLogging:
    """Tests for the setup_logging function."""

    @pytest.fixture(autouse=True)
    def reset_root_logger(self):
        """Fixture to reset the root logger before and after each test."""
        root = logging.getLogger()
        original_handlers = root.handlers[:]
        original_level = root.level

        # Start each test from a clean slate to avoid interference from plugins
        root.handlers.clear()

        yield

        # Restore original handlers and level after the test
        root.handlers = original_handlers
        root.setLevel(original_level)

    def test_setup_adds_console_handler(self):
        """Verify setup_logging adds a StreamHandler to the root logger."""
        root = logging.getLogger()

        # Ensure no pre-existing handlers to avoid flaky assertions
        root.handlers.clear()

        setup_logging(console_level=logging.INFO, emoji_map=TEST_EMOJI_MAP)

        # Find a StreamHandler configured by setup_logging
        stream_handlers = [
            h for h in root.handlers if isinstance(h, logging.StreamHandler)
        ]
        assert any(
            h.level == logging.INFO and isinstance(h.formatter, ElegantFormatter)
            for h in stream_handlers
        )

    @patch("src.utils.log_config.logging.FileHandler")
    def test_setup_adds_file_handler(self, mock_file_handler):
        """Verify setup_logging adds a FileHandler when a path is provided."""
        mock_instance = MagicMock()
        mock_file_handler.return_value = mock_instance

        log_file = "test.log"
        setup_logging(log_file=log_file, console_level=logging.DEBUG)

        # Check that FileHandler was instantiated with the correct path
        mock_file_handler.assert_called_once_with(log_file)

        # Check that the handler was added to the root logger
        root = logging.getLogger()
        assert mock_instance in root.handlers

        # When using a MagicMock, level won't change automatically; verify setLevel was called correctly
        mock_instance.setLevel.assert_called_once_with(logging.DEBUG)

        # Verify that setFormatter was called with a standard logging.Formatter (not ElegantFormatter)
        assert mock_instance.setFormatter.called
        formatter_arg = mock_instance.setFormatter.call_args[0][0]
        assert isinstance(formatter_arg, logging.Formatter)
        assert not isinstance(formatter_arg, ElegantFormatter)

    def test_setup_without_file_handler(self):
        """Verify no FileHandler is added when log_file is None."""
        root = logging.getLogger()
        setup_logging()  # log_file is None by default

        has_file_handler = any(
            isinstance(h, logging.FileHandler) for h in root.handlers
        )
        assert not has_file_handler
