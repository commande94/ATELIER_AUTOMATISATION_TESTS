from datetime import datetime, timezone
from tester.tests import run_all_tests


def execute_run():
  tests = run_all_tests()

  passed = sum(1 for t in tests if t["status"] == "PASS")
  failed = sum(1 for t in tests if t["status"] == "FAIL")
  total_tests = len(tests)
  error_rate = round(failed / total_tests, 3) if total_tests > 0 else 0

  latencies = [t["latency_ms"] for t in tests]
  avg_latency = (
      int(sum(latencies) / len(latencies)) if latencies else 0
  )

  # Calcul simple du p95
  latencies.sort()
  p95_index = int(len(latencies) * 0.95)
  p95_latency = latencies[min(p95_index, len(latencies) - 1)] if latencies else 0

  summary = {
      "api": "Cat Facts",
      "passed": passed,
      "failed": failed,
      "error_rate": error_rate,
      "latency_ms_avg": avg_latency,
      "latency_ms_p95": p95_latency,
  }

  run_data = {
      "timestamp": datetime.now(timezone.utc).isoformat(),
      "summary": summary,
      "tests": tests,
  }

  return run_data
