"""
Configuration settings for the Sanic Notes API application.
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    database_path: str = "app.db"
    connection_timeout: float = 30.0

    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create database config from environment variables."""
        return cls(
            database_path=os.getenv("DATABASE_PATH", "app.db"),
            connection_timeout=float(os.getenv("DATABASE_TIMEOUT", "30.0"))
        )

@dataclass
class ServerConfig:
    """Server configuration settings."""
    host: str = "0.0.0.0"
    port: int = 8880
    debug: bool = True
    access_log: bool = True

    @classmethod
    def from_env(cls) -> 'ServerConfig':
        """Create server config from environment variables."""
        return cls(
            host=os.getenv("SERVER_HOST", "0.0.0.0"),
            port=int(os.getenv("SERVER_PORT", "8880")),
            debug=os.getenv("DEBUG", "true").lower() == "true",
            access_log=os.getenv("ACCESS_LOG", "true").lower() == "true"
        )

@dataclass
class HTTPClientConfig:
    """HTTP client configuration settings."""
    timeout: float = 10.0
    max_retries: int = 3

    @classmethod
    def from_env(cls) -> 'HTTPClientConfig':
        """Create HTTP client config from environment variables."""
        return cls(
            timeout=float(os.getenv("HTTP_TIMEOUT", "10.0")),
            max_retries=int(os.getenv("HTTP_MAX_RETRIES", "3"))
        )

@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @classmethod
    def from_env(cls) -> 'LoggingConfig':
        """Create logging config from environment variables."""
        return cls(
            level=os.getenv("LOG_LEVEL", "INFO"),
            format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

@dataclass
class AppConfig:
    """Main application configuration."""
    database: DatabaseConfig
    server: ServerConfig
    http_client: HTTPClientConfig
    logging: LoggingConfig

    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create application config from environment variables."""
        return cls(
            database=DatabaseConfig.from_env(),
            server=ServerConfig.from_env(),
            http_client=HTTPClientConfig.from_env(),
            logging=LoggingConfig.from_env()
        )

# Global configuration instance
config = AppConfig.from_env()
