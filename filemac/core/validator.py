from typing import Tuple
from pathlib import Path


class SystemValidator:
    """Validates system requirements and dependencies."""

    @staticmethod
    def validate_file_permissions(temp_dir: Path) -> Tuple[bool, str]:
        """Validate write permissions in temporary directory."""
        try:
            if temp_dir.is_file():
                temp_dir = temp_dir.parent
            test_file = temp_dir / "permission_test.txt"
            test_file.write_text("test")
            test_file.unlink()
            return True, "Write permissions verified"
        except (OSError, IOError) as e:
            return False, f"Insufficient permissions: {str(e)}"
