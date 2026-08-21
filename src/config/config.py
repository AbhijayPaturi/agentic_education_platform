"""Application configuration management with environment variable loading."""

import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

from src.utils.text_utils import sanitize_filename

# Load .env from project root
# Path: src/config/config.py -> src/config/ -> src/ -> project_root/
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


def _as_bool(value: Optional[str]) -> bool:
    """Interpret common truthy string values from environment variables."""
    return str(value).strip().lower() in {'1', 'true', 'yes', 'on'}


def _configure_ssl_bypass() -> None:
    """Disable TLS verification process-wide.

    This is a security trade-off intended ONLY for corporate networks that
    perform TLS interception with self-signed certificates. It is opt-in via
    the ``DISABLE_SSL_VERIFY`` environment variable and disabled by default so
    the application is secure out of the box.
    """
    import ssl
    import warnings
    import urllib3
    import httpx

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    ssl._create_default_https_context = ssl._create_unverified_context

    os.environ['CURL_CA_BUNDLE'] = ''
    os.environ['REQUESTS_CA_BUNDLE'] = ''
    os.environ['SSL_CERT_FILE'] = ''
    os.environ['PYTHONHTTPSVERIFY'] = '0'

    # Force httpx clients (used by openai/crewai) to skip verification.
    if not getattr(httpx.Client, '_ssl_bypass_patched', False):
        _orig_sync_init = httpx.Client.__init__
        _orig_async_init = httpx.AsyncClient.__init__

        def _sync_init(self, *args, **kwargs):
            kwargs['verify'] = False
            _orig_sync_init(self, *args, **kwargs)

        def _async_init(self, *args, **kwargs):
            kwargs['verify'] = False
            _orig_async_init(self, *args, **kwargs)

        httpx.Client.__init__ = _sync_init
        httpx.AsyncClient.__init__ = _async_init
        httpx.Client._ssl_bypass_patched = True


# Disable telemetry (avoids background network calls / SSL noise).
os.environ.setdefault('CREWAI_TELEMETRY_ENABLED', 'false')
os.environ.setdefault('OTEL_SDK_DISABLED', 'true')

# Opt-in TLS bypass for corporate proxy environments (secure by default).
DISABLE_SSL_VERIFY = _as_bool(os.getenv('DISABLE_SSL_VERIFY'))
if DISABLE_SSL_VERIFY:
    _configure_ssl_bypass()


class Config:
    """Application configuration with centralized settings and validation."""

    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    # Model is configurable via OPENAI_MODEL; defaults to a fast, low-cost model.
    DEFAULT_MODEL: str = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    OUTPUT_DIR: Path = Path(__file__).parent.parent.parent / 'output'
    VERBOSE: bool = _as_bool(os.getenv('VERBOSE', 'true'))
    DISABLE_SSL_VERIFY: bool = DISABLE_SSL_VERIFY

    @classmethod
    def validate(cls) -> None:
        """Validate required configuration is present.
        
        Raises:
            ValueError: If critical configuration is missing
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please create a .env file in the project root with your OpenAI API key."
            )
        
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_output_path(cls, topic_name: str, lesson_number: Optional[int] = None) -> Path:
        """Generate structured output path for educational content.
        
        Args:
            topic_name: Topic being taught
            lesson_number: Optional lesson number for further organization
            
        Returns:
            Path object for output directory
        """
        # Sanitize for filesystem
        safe_topic_name = sanitize_filename(topic_name)

        if lesson_number is not None:
            path = cls.OUTPUT_DIR / safe_topic_name / f'lesson_{lesson_number}'
        else:
            path = cls.OUTPUT_DIR / safe_topic_name
        
        path.mkdir(parents=True, exist_ok=True)
        return path


Config.validate()
