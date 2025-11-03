"""
Secure API Key Management
Handles sensitive configuration and API keys securely
"""

import os
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class SecretsManager:
    """Secure management of API keys and sensitive configuration"""
    
    def __init__(self, secrets_dir: str = "secure_config"):
        self.secrets_dir = Path(secrets_dir)
        self.secrets_dir.mkdir(exist_ok=True)
        self.api_keys_file = self.secrets_dir / "api_keys.env"
        
        # Ensure proper permissions (Unix only)
        if os.name != 'nt':  # Not Windows
            try:
                os.chmod(self.secrets_dir, 0o700)  # rwx------
                if self.api_keys_file.exists():
                    os.chmod(self.api_keys_file, 0o600)  # rw-------
            except OSError:
                logger.warning("Could not set restrictive permissions on secrets directory")
    
    def load_api_keys(self) -> Dict[str, str]:
        """Load API keys from the secrets file"""
        api_keys = {}
        
        if not self.api_keys_file.exists():
            logger.warning(f"API keys file not found: {self.api_keys_file}")
            return api_keys
        
        try:
            with open(self.api_keys_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Skip placeholder values
                        if not value.startswith('your_') and value != 'your_key_here':
                            api_keys[key] = value
                            # Set as environment variable
                            os.environ[key] = value
            
            logger.info(f"Loaded {len(api_keys)} API keys from secrets")
            return api_keys
            
        except Exception as e:
            logger.error(f"Error loading API keys: {e}")
            return api_keys
    
    def get_api_key(self, key_name: str, default: Optional[str] = None) -> Optional[str]:
        """Get a specific API key"""
        # First check environment variables
        value = os.getenv(key_name)
        if value and not value.startswith('your_'):
            return value
        
        # Then check loaded keys
        api_keys = self.load_api_keys()
        return api_keys.get(key_name, default)
    
    def set_api_key(self, key_name: str, value: str) -> bool:
        """Set an API key (updates file and environment)"""
        try:
            # Update environment variable
            os.environ[key_name] = value
            
            # Update file
            lines = []
            found = False
            
            if self.api_keys_file.exists():
                with open(self.api_keys_file, 'r') as f:
                    lines = f.readlines()
            
            # Update existing key or add new one
            for i, line in enumerate(lines):
                if line.strip().startswith(f"{key_name}="):
                    lines[i] = f"{key_name}={value}\n"
                    found = True
                    break
            
            if not found:
                lines.append(f"{key_name}={value}\n")
            
            with open(self.api_keys_file, 'w') as f:
                f.writelines(lines)
            
            # Set restrictive permissions
            if os.name != 'nt':
                os.chmod(self.api_keys_file, 0o600)
            
            logger.info(f"Updated API key: {key_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting API key {key_name}: {e}")
            return False


# Global instance
secrets = SecretsManager()


def load_secrets():
    """Convenience function to load all secrets"""
    return secrets.load_api_keys()


def get_secret(key: str, default: str = None) -> str:
    """Convenience function to get a secret"""
    return secrets.get_api_key(key, default)