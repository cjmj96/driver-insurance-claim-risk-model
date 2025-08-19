import logging


class ElegantFormatter(logging.Formatter):
    """Custom formatter: elegant INFO with dynamic emojis, detailed other levels."""

    def __init__(
        self, info_fmt="%(message)s", other_fmt=None, datefmt=None, emoji_map=None
    ):
        super().__init__(datefmt=datefmt)
        self.info_fmt = info_fmt
        self.other_fmt = (
            other_fmt or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.emoji_map = emoji_map or {}  # Maps keywords to emojis

    def _get_emoji(self, message):
        """Find first matching emoji based on message keywords."""
        for keyword, emoji in self.emoji_map.items():
            if keyword.lower() in message.lower():
                return f"{emoji} "
        return ""

    def format(self, record):
        if record.levelno == logging.INFO:
            # Add dynamic emoji to INFO messages
            emoji = self._get_emoji(record.getMessage())
            record.msg = emoji + record.msg
            formatter = logging.Formatter(self.info_fmt, datefmt=self.datefmt)
        else:
            formatter = logging.Formatter(self.other_fmt, datefmt=self.datefmt)
        return formatter.format(record)


# Configure logging with custom emojis
def setup_logging(console_level=logging.INFO, log_file=None, emoji_map=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Console handler with dynamic emojis
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(
        ElegantFormatter(
            info_fmt="%(message)s",
            other_fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            emoji_map=emoji_map,
        )
    )

    # File handler (detailed logs)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)

    logger.addHandler(console_handler)
