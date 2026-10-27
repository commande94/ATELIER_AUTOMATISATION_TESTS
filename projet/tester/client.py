import time
import requests


class APIClient:

  def __init__(self, base_url):
    self.base_url = base_url

  def get(self, endpoint, timeout=3):
    url = self.base_url + endpoint
    start_time = time.time()
    try:
      # Tentative avec timeout strict
      response = requests.get(url, timeout=timeout)
      latency = int((time.time() - start_time) * 1000)
      return response, latency
    except requests.exceptions.Timeout:
      # Un seul retry simple en cas de timeout
      try:
        start_time = time.time()
        response = requests.get(url, timeout=timeout)
        latency = int((time.time() - start_time) * 1000)
        return response, latency
      except Exception as e:
        return None, 0
    except Exception as e:
        return None, 0
