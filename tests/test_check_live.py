import importlib.util
import io
import json
from pathlib import Path
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_live", ROOT / "scripts" / "check_live.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

RECORD = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))


def fake_discover(server_info):
    fake = types.SimpleNamespace(ENDPOINT=None)
    fake.discover = lambda: {"serverInfo": server_info}
    return fake


class CheckLiveTests(unittest.TestCase):
    def live_info(self, **changes):
        info = {"name": "Scraper API", **{field: RECORD[field] for field in module.FIELDS}}
        info.update(changes)
        return info

    def test_a_matching_server_passes_and_the_record_endpoint_is_checked(self):
        fake = fake_discover(self.live_info())
        with patch("sys.stdout", new=io.StringIO()):
            self.assertEqual(module.main(fake), 0)
        self.assertEqual(fake.ENDPOINT, RECORD["remotes"][0]["url"])

    def test_a_different_version_fails(self):
        with patch("sys.stderr", new=io.StringIO()) as stderr:
            self.assertEqual(module.main(fake_discover(self.live_info(version="0.1.0"))), 1)
        self.assertIn("version", stderr.getvalue())

    def test_a_different_icon_theme_fails(self):
        icons = [dict(icon, theme=None) for icon in RECORD["icons"]]
        with patch("sys.stderr", new=io.StringIO()):
            self.assertEqual(module.main(fake_discover(self.live_info(icons=icons))), 1)

    def test_the_record_and_the_example_share_one_endpoint(self):
        discover = module.load_discover()
        self.assertEqual(RECORD["remotes"][0]["url"], discover.ENDPOINT)


if __name__ == "__main__":
    unittest.main()
