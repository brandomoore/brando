import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]


class LockupAssetTests(unittest.TestCase):
    def test_current_names_and_legacy_urls_share_generated_artwork(self):
        config = json.loads((ROOT / "apps.json").read_text())
        for app in config["apps"]:
            stem = Path(app["logo"]).stem
            self.assertTrue((ROOT / app["logo"]).is_file())
            for mode in ("light", "dark"):
                with self.subTest(app=app["name"], mode=mode):
                    current = (ROOT / "logos/lockups" / f"{stem}-{mode}.svg").read_bytes()
                    svg = ET.fromstring(current)
                    self.assertEqual(svg.attrib["aria-label"], app["name"])
                    self.assertEqual(svg.attrib["height"], "32")
                    for legacy in app.get("legacyLogoStems", []):
                        alias = ROOT / "logos/lockups" / f"{legacy}-{mode}.svg"
                        self.assertEqual(alias.read_bytes(), current)

    def test_strozz_uses_current_repository_and_asset_names(self):
        config = json.loads((ROOT / "apps.json").read_text())
        app = next(app for app in config["apps"] if app["name"] == "Strozz")
        self.assertEqual(app["repo"], "https://github.com/brandomoore/strozz")
        self.assertEqual(app["logo"], "logos/strozz.svg")
        self.assertIn("twozz", app["legacyLogoStems"])


if __name__ == "__main__":
    unittest.main()
