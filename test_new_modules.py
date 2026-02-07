"""
Simple test to verify that the new modules can be imported correctly.
"""

def test_imports():
    try:
        from scripts.tools import web_search
        print("+ Successfully imported web_search module")

        from scripts import agent_logic
        print("+ Successfully imported agent_logic module")

        from scripts.config import TAVILY_API_KEY
        print("+ Successfully imported TAVILY_API_KEY from config")

        print("\nAll imports successful!")
        return True
    except ImportError as e:
        print(f"- Import error: {e}")
        return False
    except Exception as e:
        print(f"- Unexpected error: {e}")
        return False


if __name__ == "__main__":
    test_imports()