import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/topology-validator.sh"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


class TopologyValidatorTests(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_help_exits_zero(self) -> None:
        result = self.run_validator("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout)

    def test_no_args_exits_two(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage:", result.stdout)

    def test_valid_campus_is_idempotent(self) -> None:
        first = self.run_validator(str(FIXTURES / "valid-campus.topo"))
        second = self.run_validator(str(FIXTURES / "valid-campus.topo"))
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertIn("0 error(s), 0 warning(s)", first.stdout)

    def test_path_with_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "dir with spaces" / "my topo.topo"
            target.parent.mkdir()
            target.write_text((FIXTURES / "valid-campus.topo").read_text(encoding="utf-8"))
            result = self.run_validator(str(target))
        self.assertEqual(result.returncode, 0)

    def test_empty_manifest_is_error(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".topo", delete=False) as handle:
            path = handle.name
        try:
            result = self.run_validator(path)
        finally:
            os.unlink(path)
        self.assertEqual(result.returncode, 1)
        self.assertIn("no node records", result.stderr)

    def test_missing_and_unreadable_manifest(self) -> None:
        missing = self.run_validator("/no/such/manifest.topo")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("not a regular file", missing.stderr)

        with tempfile.NamedTemporaryFile("w", suffix=".topo", delete=False) as handle:
            handle.write("node R1 router\n")
            path = handle.name
        os.chmod(path, 0)
        try:
            result = self.run_validator(path)
        finally:
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
            os.unlink(path)
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot read manifest file", result.stderr)

    def test_invalid_stp_value_is_reported(self) -> None:
        result = self.run_validator(str(FIXTURES / "invalid-stp.topo"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown link attribute", result.stderr)

    def test_vlan_out_of_range_is_rejected(self) -> None:
        result = self.run_validator(str(FIXTURES / "invalid-vlan.topo"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("vlan value '5000' is out of range", result.stderr)

    def test_strict_treats_warnings_as_failures(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".topo", delete=False) as handle:
            handle.write("node R1 router\nnode R2 router\nlink R1 R2 layer3\nnode ORPHAN host\n")
            path = handle.name
        try:
            loose = self.run_validator(path)
            strict = self.run_validator("--strict", path)
        finally:
            os.unlink(path)
        self.assertEqual(loose.returncode, 0)
        self.assertEqual(strict.returncode, 1)
        self.assertIn("strict mode", strict.stderr)


if __name__ == "__main__":
    unittest.main()
