#!/usr/bin/env python3
"""
Trigger module for SceneValidator.

This module handles the automatic triggering of scene validation
based on various events like file uploads, metadata changes, etc.
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

from validator import SceneValidator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("scene_validator_trigger")

class SceneValidatorTrigger:
    """Class that handles triggering scene validation based on events."""
    
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the trigger.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.validator = SceneValidator(config_path)
        self.last_check_time = datetime.now()
        logger.info("SceneValidatorTrigger initialized")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dict containing configuration
        """
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found at {config_path}, using defaults")
            return {
                "trigger": {
                    "watch_interval_seconds": 60,
                    "watch_directories": ["data/scenes"],
                    "watch_file_patterns": ["*.json", "*.xml"],
                    "ignore_patterns": ["*_temp.json", "*.bak"],
                    "trigger_on_metadata_change": True,
                    "notification_on_validation": True
                }
            }
    
    def watch_directories(self) -> List[Dict]:
        """Watch directories for new or modified scene files.
        
        Returns:
            List of scene files that have been added or modified
        """
        modified_files = []
        
        # Get watch directories from config
        watch_dirs = self.config.get("trigger", {}).get(
            "watch_directories", ["data/scenes"]
        )
        
        # Get file patterns to watch
        patterns = self.config.get("trigger", {}).get(
            "watch_file_patterns", ["*.json", "*.xml"]
        )
        
        # Get patterns to ignore
        ignore_patterns = self.config.get("trigger", {}).get(
            "ignore_patterns", []
        )
        
        # Check each directory
        for directory in watch_dirs:
            if not os.path.exists(directory):
                logger.warning(f"Watch directory does not exist: {directory}")
                continue
            
            # Get all files matching patterns
            for pattern in patterns:
                path = Path(directory)
                for file_path in path.glob(pattern):
                    # Check if file should be ignored
                    if any(file_path.match(ignore) for ignore in ignore_patterns):
                        continue
                    
                    # Check if file was modified since last check
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if mod_time > self.last_check_time:
                        logger.info(f"Found modified file: {file_path}")
                        modified_files.append({
                            "path": str(file_path),
                            "modified_time": mod_time.isoformat()
                        })
        
        self.last_check_time = datetime.now()
        return modified_files
    
    def process_scene_file(self, file_path: str) -> Dict:
        """Process a scene file and run validation.
        
        Args:
            file_path: Path to scene file
            
        Returns:
            Dict containing validation results
        """
        try:
            with open(file_path, "r") as f:
                scene_data = json.load(f)
            
            # Generate a report filename
            report_dir = "reports"
            os.makedirs(report_dir, exist_ok=True)
            
            scene_id = scene_data.get("scene_id", "unknown")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(
                report_dir, f"validation_{scene_id}_{timestamp}.html"
            )
            
            # Validate the scene
            results = self.validator.validate_scene(scene_data)
            
            # Generate and save the report
            report = self.validator.generate_report(results, report_path)
            
            # Send notification if configured
            if self.config.get("trigger", {}).get("notification_on_validation", True):
                self._send_notification(results, report_path)
            
            logger.info(f"Processed scene file: {file_path}")
            logger.info(f"Validation report saved to: {report_path}")
            
            return {
                "success": True,
                "scene_id": scene_id,
                "valid": results.get("valid", False),
                "report_path": report_path,
                "error_count": len(results.get("errors", [])),
                "warning_count": len(results.get("warnings", []))
            }
        
        except Exception as e:
            logger.error(f"Error processing scene file {file_path}: {e}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
    
    def _send_notification(self, results: Dict, report_path: str) -> None:
        """Send notification about validation results.
        
        Args:
            results: Validation results
            report_path: Path to the generated report
        """
        # This is a placeholder for notification integration
        # In a real implementation, this could send emails, Slack messages, etc.
        scene_id = results.get("scene_id", "unknown")
        is_valid = results.get("valid", False)
        error_count = len(results.get("errors", []))
        warning_count = len(results.get("warnings", []))
        
        logger.info(f"NOTIFICATION: Scene {scene_id} validation completed")
        logger.info(f"NOTIFICATION: Valid: {is_valid}, Errors: {error_count}, Warnings: {warning_count}")
        logger.info(f"NOTIFICATION: Report available at: {report_path}")
    
    def run_continuous_watch(self, interval: Optional[int] = None) -> None:
        """Run continuous watch for scene changes.
        
        Args:
            interval: Interval in seconds between checks, overrides config
        """
        if interval is None:
            interval = self.config.get("trigger", {}).get(
                "watch_interval_seconds", 60
            )
        
        logger.info(f"Starting continuous watch with interval: {interval} seconds")
        
        try:
            while True:
                modified_files = self.watch_directories()
                
                for file_info in modified_files:
                    file_path = file_info["path"]
                    self.process_scene_file(file_path)
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            logger.info("Continuous watch stopped by user")
        except Exception as e:
            logger.error(f"Error in continuous watch: {e}")
            raise


def main():
    """Main function for running the trigger as a script."""
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config/config.json"
    
    trigger = SceneValidatorTrigger(config_path)
    
    # If a specific file is provided, process it once
    if len(sys.argv) > 2 and os.path.isfile(sys.argv[2]):
        trigger.process_scene_file(sys.argv[2])
    else:
        # Otherwise, start continuous watch
        trigger.run_continuous_watch()


if __name__ == "__main__":
    main()