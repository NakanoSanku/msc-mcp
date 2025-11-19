import unittest
from unittest.mock import patch


class TestMain(unittest.TestCase):
    @patch("msc_mcp.server.mcp")
    def test_main_calls_mcp_run(self, mock_mcp) -> None:
        # Import inside the test so patched mcp is used by serve().
        from msc_mcp.__main__ import main

        # No CLI arguments; should just invoke serve() -> mcp.run().
        main([])

        mock_mcp.run.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

