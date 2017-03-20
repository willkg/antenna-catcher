from pathlib import Path
import sys


# Add repository root so we can import catcher
REPO_ROOT = Path(__file__).parent.parent
print(str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT))
