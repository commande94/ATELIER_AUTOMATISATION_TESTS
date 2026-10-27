from flask import Flask, jsonify, render_template
from storage import get_all_runs, save_run
from tester.runner import execute_run

app = Flask(__name__)


@app.route("/")
def home():
  return render_template("dashboard.html", runs=get_all_runs())


@app.route("/dashboard")
def dashboard():
  return render_template("dashboard.html", runs=get_all_runs())


@app.route("/run", methods=["GET", "POST"])
def run_tests():
  run_data = execute_run()
  save_run(run_data)
  return jsonify(
      {"status": "success", "message": "Run executed successfully", "data": run_data}
  )


@app.route("/health")
def health():
  runs = get_all_runs()
  status = "OK" if runs and runs[0]["summary"]["failed"] == 0 else "DEGRADED"
  return jsonify({"status": status, "last_run": runs[0] if runs else None})


if __name__ == "__main__":
  app.run(debug=True)
