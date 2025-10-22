import os
import logging
from typing import Dict, Any
from ..utils.core_utils import ConfigValidator


class ConfigManager:
    """Centralized configuration management"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load_config()
    
    def _load_config(self):
        """Load and validate all configuration"""
        # Required environment variables
        required_env_vars = [
            'GOOGLE_SHEETS_ID',  # ← แก้ตรงนี้
            'LINE_CHANNEL_ACCESS_TOKEN',
            'LINE_CHANNEL_SECRET',
            'LINE_USER_ID'
        ]
        
        try:
            self._config = ConfigValidator.validate_required_env_vars(required_env_vars)
            
            # Add optional configs with defaults
            self._config.update({
                'DEBUG': os.getenv('DEBUG', 'false').lower() == 'true',
                'PORT': int(os.getenv('PORT', '8080')),
                'BINANCE_BASE_URL': 'https://api.binance.com/api/v3',
                'VERSION': os.getenv('VERSION', '2.0-refactored'),
                'GOOGLE_APPLICATION_CREDENTIALS': os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/app/credentials.json')
            })
            
            # Validate configuration
            self._validate_config()
            
            logging.info("✅ Configuration loaded successfully")
            
        except Exception as e:
            logging.error(f"❌ Configuration error: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self._config.copy()
    
    def _validate_config(self):
        """Validate configuration values"""
        # Validate port range
        port = self._config.get('PORT')
        if not (1024 <= port <= 65535):
            raise ValueError(f"Invalid port: {port}. Must be between 1024-65535")
        
        # Validate Google Sheets ID format
        sheets_id = self._config.get('GOOGLE_SHEETS_ID')
        if not sheets_id or len(sheets_id) < 20:
            raise ValueError("Invalid Google Sheets ID")
        
        # Validate LINE tokens
        line_token = self._config.get('LINE_CHANNEL_ACCESS_TOKEN')
        if not line_token or len(line_token) < 50:
            raise ValueError("Invalid LINE Channel Access Token")
        
        logging.info("✅ Configuration validation passed")
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled"""
        return self._config.get('DEBUG', False)
    
    def get_binance_config(self) -> Dict[str, str]:
        """Get Binance API configuration"""
        return {
            'base_url': self._config['BINANCE_BASE_URL'],
            'timeout': 30,
            'rate_limit': 1200
        }
    
    def get_google_config(self) -> Dict[str, str]:
        """Get Google API configuration"""
        return {
            'sheets_id': self._config['GOOGLE_SHEETS_ID'],
            'credentials_path': self._config['GOOGLE_APPLICATION_CREDENTIALS']
        }
    
    def get_line_config(self) -> Dict[str, str]:
        """Get LINE Bot configuration"""
        return {
            'access_token': self._config['LINE_CHANNEL_ACCESS_TOKEN'],
            'secret': self._config['LINE_CHANNEL_SECRET'],
            'user_id': self._config.get('LINE_USER_ID')
        }