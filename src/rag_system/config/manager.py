import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
from .models import SystemConfig


class ConfigManager:
    """Configuration manager for loading and saving configurations"""
    
    def __init__(self):
        self.config: Optional[SystemConfig] = None
    
    def load_from_file(self, config_path: Path) -> SystemConfig:
        """Load configuration from YAML or JSON file"""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        if config_path.suffix.lower() in ['.yaml', '.yml']:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_dict = yaml.safe_load(f)
        elif config_path.suffix.lower() == '.json':
            with open(config_path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
        else:
            raise ValueError(f"Unsupported configuration file format: {config_path.suffix}")
        
        self.config = SystemConfig(**config_dict)
        return self.config
    
    def load_from_dict(self, config_dict: Dict[str, Any]) -> SystemConfig:
        """Load configuration from dictionary"""
        self.config = SystemConfig(**config_dict)
        return self.config
    
    def load_default(self) -> SystemConfig:
        """Load default configuration"""
        self.config = SystemConfig()
        return self.config
    
    def save_to_file(self, config_path: Path, config: Optional[SystemConfig] = None) -> None:
        """Save configuration to YAML or JSON file"""
        if config is None:
            config = self.config
        
        if config is None:
            raise ValueError("No configuration to save")
        
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        config_dict = config.model_dump()
        
        if config_path.suffix.lower() in ['.yaml', '.yml']:
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
        elif config_path.suffix.lower() == '.json':
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported configuration file format: {config_path.suffix}")
    
    def get_config(self) -> SystemConfig:
        """Get current configuration"""
        if self.config is None:
            self.config = SystemConfig()
        return self.config
    
    def update_config(self, updates: Dict[str, Any]) -> SystemConfig:
        """Update configuration with new values"""
        if self.config is None:
            self.config = SystemConfig()
        
        # Deep update the configuration
        config_dict = self.config.model_dump()
        self._deep_update(config_dict, updates)
        
        self.config = SystemConfig(**config_dict)
        return self.config
    
    def _deep_update(self, base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> None:
        """Recursively update nested dictionaries"""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value


# Global configuration manager instance
config_manager = ConfigManager()