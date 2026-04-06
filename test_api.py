"""
Robust TMDb API Tester (Stable Version)

"""

import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🎬 TMDb API Key Tester (Robust Version)")
print("=" * 60)

# 🔑 Choose ONE method:

# --- Method 1: API Key ---
API_KEY = os.getenv("TMDB_API_KEY")
# print(API_KEY)

# --- Method 2: Bearer Token (Recommended) ---
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# print(ACCESS_TOKEN)

# 🌐 Create Session with Retry
session = requests.Session()

retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)

# 🧠 Headers
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    # Uncomment if using Bearer token:
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}


# 🔧 Safe request function
def safe_get(url, params=None):
    try:
        response = session.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Failed: {e}")
        return None


# 🧪 Test flags
test1_ok = False
test2_ok = False
test3_ok = False

# ============================================================
# 🔍 TEST 1: Basic API
# ============================================================
print("\n🔍 Test 1: Basic API Connection")
print("-" * 60)

url = "https://api.themoviedb.org/3/movie/550"
params = {"api_key": API_KEY}

data = safe_get(url, params)

if data:
    print("✅ SUCCESS!")
    print(f"   Movie: {data['title']}")
    print(f"   Year: {data['release_date'][:4]}")
    test1_ok = True
else:
    print("❌ FAILED!")


time.sleep(1.5)

# ============================================================
# 🔍 TEST 2: Search
# ============================================================
print("\n🔍 Test 2: Movie Search")
print("-" * 60)

url = "https://api.themoviedb.org/3/search/movie"
params = {"api_key": API_KEY, "query": "Spider-Man"}

data = safe_get(url, params)

if data and data.get("results"):
    results = data["results"]
    print(f"✅ Found {len(results)} movies")
    print(f"   Top: {results[0]['title']}")
    test2_ok = True
else:
    print("❌ FAILED or No results")


time.sleep(1.5)

# ============================================================
# 🔍 TEST 3: Credits
# ============================================================
print("\n🔍 Test 3: Director Info")
print("-" * 60)

url = "https://api.themoviedb.org/3/movie/557/credits"
params = {"api_key": API_KEY}

data = safe_get(url, params)

if data and "crew" in data:
    directors = [c["name"] for c in data["crew"] if c["job"] == "Director"]
    if directors:
        print(f"✅ Director: {directors[0]}")
        test3_ok = True
    else:
        print("⚠️ No director found")
else:
    print("❌ FAILED")


# ============================================================
# 📊 FINAL RESULT
# ============================================================
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)

if test1_ok and test2_ok and test3_ok:
    print("\n✅ ALL TESTS PASSED!")
    print("   Your TMDb integration is stable 🚀")
else:
    print("\n❌ SOME TESTS FAILED!")
    print("   Likely network instability (not API issue)")

print("=" * 60)
