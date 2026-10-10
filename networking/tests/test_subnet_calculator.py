import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/subnet-calculator.py"


class SubnetCalculatorCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_help_exits_zero(self) -> None:
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("CIDR/VLSM calculator", result.stdout)

    def test_no_args_exits_two(self) -> None:
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("required", result.stderr)

    def test_summary_happy_path_json(self) -> None:
        result = self.run_cli("summary", "--json", "10.0.0.0/24", "2001:db8::/64")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["usable_hosts"], 254)
        self.assertEqual(payload[1]["version"], 6)

    def test_vlsm_happy_path_and_idempotence(self) -> None:
        args = ("vlsm", "--parent", "10.20.0.0/24", "--hosts", "users=100,servers=50,mgmt=20", "--json")
        first = self.run_cli(*args)
        second = self.run_cli(*args)
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        labels = [row["label"] for row in payload["allocations"]]
        self.assertEqual(labels, ["users", "servers", "mgmt"])
        self.assertEqual(payload["allocations"][0]["subnet"], "10.20.0.0/25")

    def test_split_happy_path(self) -> None:
        result = self.run_cli("split", "--network", "192.168.10.0/24", "--new-prefix", "26", "--json")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload), 4)
        self.assertEqual(payload[0]["network"], "192.168.10.0/26")

    def test_split_rejects_excessive_expansion(self) -> None:
        result = self.run_cli(
            "split",
            "--network",
            "2001:db8::/64",
            "--new-prefix",
            "80",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("would produce 65536 child subnets", result.stderr)

    def test_invalid_network_and_empty_hosts(self) -> None:
        invalid = self.run_cli("summary", "not-a-cidr")
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("invalid network", invalid.stderr)

        empty = self.run_cli("vlsm", "--parent", "10.0.0.0/24", "--hosts", "")
        self.assertEqual(empty.returncode, 2)
        self.assertIn("cannot be empty", empty.stderr)

        too_small = self.run_cli("vlsm", "--parent", "10.0.0.0/30", "--hosts", "users=100")
        self.assertEqual(too_small.returncode, 2)
        self.assertIn("too small", too_small.stderr)

        ipv6_parent = self.run_cli("vlsm", "--parent", "2001:db8::/32", "--hosts", "10")
        self.assertEqual(ipv6_parent.returncode, 2)
        self.assertIn("IPv4", ipv6_parent.stderr)


if __name__ == "__main__":
    unittest.main()
