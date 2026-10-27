from tester.client import APIClient


def run_all_tests():
  client = APIClient("https://catfact.ninja")
  tests_results = []

  # --- TEST 1 : Statut HTTP 200 sur /fact ---
  resp, lat = client.get("/fact")
  if resp and resp.status_code == 200:
    tests_results.append({
        "name": "GET /fact - Status 200",
        "status": "PASS",
        "latency_ms": lat,
    })
  else:
    tests_results.append({
        "name": "GET /fact - Status 200",
        "status": "FAIL",
        "latency_ms": lat,
        "details": f"Status code: {resp.status_code if resp else 'No response'}",
    })

  # --- TEST 2 : Content-Type JSON ---
  if resp and "application/json" in resp.headers.get("Content-Type", ""):
    tests_results.append({
        "name": "GET /fact - Content-Type JSON",
        "status": "PASS",
        "latency_ms": lat,
    })
  else:
    tests_results.append({
        "name": "GET /fact - Content-Type JSON",
        "status": "FAIL",
        "latency_ms": lat,
        "details": "Invalid Content-Type",
    })

  # --- TEST 3 : Présence des champs obligatoires (fact & length) ---
  try:
    data = resp.json()
    if "fact" in data and "length" in data:
      tests_results.append({
          "name": "Schema Check - Required fields",
          "status": "PASS",
          "latency_ms": lat,
      })
    else:
      tests_results.append({
          "name": "Schema Check - Required fields",
          "status": "FAIL",
          "latency_ms": lat,
          "details": "Missing 'fact' or 'length'",
      })
  except Exception:
    tests_results.append({
        "name": "Schema Check - Required fields",
        "status": "FAIL",
        "latency_ms": lat,
        "details": "JSON parse error",
    })

  # --- TEST 4 : Vérification des types de données (string et int) ---
  try:
    if isinstance(data.get("fact"), str) and isinstance(
        data.get("length"), int
    ):
      tests_results.append({
          "name": "Types Check - fact(str) & length(int)",
          "status": "PASS",
          "latency_ms": lat,
      })
    else:
      tests_results.append({
          "name": "Types Check - fact(str) & length(int)",
          "status": "FAIL",
          "latency_ms": lat,
          "details": "Incorrect types",
      })
  except Exception:
    tests_results.append({
        "name": "Types Check - fact(str) & length(int)",
        "status": "FAIL",
        "latency_ms": lat,
        "details": "Error checking types",
    })

  # --- TEST 5 : Endpoint de liste /facts ---
  resp_list, lat_list = client.get("/facts")
  if resp_list and resp_list.status_code == 200:
    try:
      list_data = resp_list.json()
      if "data" in list_data and isinstance(list_data["data"], list):
        tests_results.append({
            "name": "GET /facts - List endpoint contract",
            "status": "PASS",
            "latency_ms": lat_list,
        })
      else:
        tests_results.append({
            "name": "GET /facts - List endpoint contract",
            "status": "FAIL",
            "latency_ms": lat_list,
            "details": "Missing 'data' array",
        })
    except Exception:
      tests_results.append({
          "name": "GET /facts - List endpoint contract",
          "status": "FAIL",
          "latency_ms": lat_list,
          "details": "JSON parse error",
      })
  else:
    tests_results.append({
        "name": "GET /facts - List endpoint contract",
        "status": "FAIL",
        "latency_ms": lat_list,
        "details": "Status not 200",
    })

  # --- TEST 6 : Robustesse sur une route invalide (404 attendu) ---
  resp_404, lat_404 = client.get("/route-inexistante-12345")
  if resp_404 and resp_404.status_code in [404, 400]:
    tests_results.append({
        "name": "Robustness - Invalid Route handling",
        "status": "PASS",
        "latency_ms": lat_404,
    })
  else:
    tests_results.append({
        "name": "Robustness - Invalid Route handling",
        "status": "FAIL",
        "latency_ms": lat_404,
        "details": (
            f"Expected 404/400, got {resp_404.status_code if resp_404 else 0}"
        ),
    })

  return tests_results
