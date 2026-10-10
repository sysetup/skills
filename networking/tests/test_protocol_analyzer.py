import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/protocol-analyzer.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
ARP_HEX = (
    "ffffffffffff00112233445508060001080006040001001122334455c0a80101"
    "000000000000c0a80102"
)


def load_module():
    spec = importlib.util.spec_from_file_location("protocol_analyzer", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProtocolAnalyzerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(MODULE_PATH), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_help_exits_zero(self) -> None:
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Analyze a classic Ethernet PCAP", result.stdout)

    def test_no_args_exits_two(self) -> None:
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("provide exactly one", result.stderr)

    def test_hex_arp_json_and_idempotence(self) -> None:
        first = self.run_cli("--hex-stream", ARP_HEX, "--json")
        second = self.run_cli("--hex-stream", ARP_HEX, "--json")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        self.assertEqual(payload["summary"]["total_packets"], 1)
        self.assertEqual(payload["packets"][0]["layer3"], "ARP")

    def test_empty_hex_stream_is_useful_error(self) -> None:
        result = self.run_cli("--hex-stream", "")
        self.assertEqual(result.returncode, 1)
        self.assertIn("No hexadecimal frames were provided", result.stderr)

    def test_invalid_hex_and_missing_pcap(self) -> None:
        bad = self.run_cli("--hex-stream", "zz")
        self.assertEqual(bad.returncode, 1)
        self.assertIn("invalid hexadecimal", bad.stderr)

        missing = self.run_cli("/no/such/file.pcap")
        self.assertEqual(missing.returncode, 1)
        self.assertIn("Capture file not found", missing.stderr)

    def test_pcap_fixture_and_path_with_spaces(self) -> None:
        result = self.run_cli(str(FIXTURES / "sample-arp.pcap"), "--json")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["total_packets"], 1)
        self.assertEqual(payload["packets"][0]["layer3"], "ARP")

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "dir with spaces" / "cap file.pcap"
            target.parent.mkdir()
            target.write_bytes((FIXTURES / "sample-arp.pcap").read_bytes())
            spaced = self.run_cli(str(target), "--summary-only")
        self.assertEqual(spaced.returncode, 0)
        self.assertIn("Packets: 1", spaced.stdout)

    def test_unreadable_pcap_is_capture_error(self) -> None:
        with tempfile.NamedTemporaryFile("wb", suffix=".pcap", delete=False) as handle:
            handle.write((FIXTURES / "sample-arp.pcap").read_bytes())
            path = handle.name
        os.chmod(path, 0)
        try:
            result = self.run_cli(path)
        finally:
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
            os.unlink(path)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Cannot read capture file", result.stderr)

    def test_pcapng_is_rejected(self) -> None:
        with tempfile.NamedTemporaryFile("wb", suffix=".pcap", delete=False) as handle:
            handle.write(b"\x0a\x0d\x0d\x0a" + b"\x00" * 20)
            path = handle.name
        try:
            result = self.run_cli(path)
        finally:
            os.unlink(path)
        self.assertEqual(result.returncode, 1)
        self.assertIn("PCAPNG is not supported", result.stderr)

    def test_analysis_can_limit_retained_packets_while_preserving_summary(self) -> None:
        hex_stream = "\n".join([ARP_HEX, ARP_HEX, ARP_HEX])
        summary, packets = self.module.analyze_hex_stream(
            hex_stream,
            detail_limit=1,
            filter_name="all",
        )
        self.assertEqual(summary.total_packets, 3)
        self.assertEqual(len(packets), 1)


if __name__ == "__main__":
    unittest.main()
