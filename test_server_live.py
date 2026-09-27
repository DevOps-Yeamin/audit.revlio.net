import time
import httpx
import sys
import io

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def test_all_live():
    print("==================================================")
    print("   TESTING LIVE LOCAL REVLIO AUDIT SERVER STACK   ")
    print("==================================================")

    # 1. Healthcheck
    print("\n[1] Testing Backend Healthcheck (GET /health)...")
    with httpx.Client(timeout=15.0) as client:
        res = client.get("http://127.0.0.1:8000/health")
        assert res.status_code == 200, f"Healthcheck failed: {res.status_code}"
        print(f"  [PASS] Backend Healthy: {res.json()}")

    # 2. Root API Info
    print("\n[2] Testing Backend Root (GET /)...")
    with httpx.Client(timeout=15.0) as client:
        res = client.get("http://127.0.0.1:8000/")
        assert res.status_code == 200
        print(f"  [PASS] Root Service: {res.json()['service']} v{res.json()['version']}")

    # 3. SSRF Defense Rejection
    print("\n[3] Testing SSRF Defense Rejection (POST /api/audit with localhost)...")
    with httpx.Client(timeout=15.0) as client:
        res = client.post("http://127.0.0.1:8000/api/audit", json={"url": "http://127.0.0.1:8080"})
        assert res.status_code == 400, f"Expected 400, got {res.status_code}"
        print(f"  [PASS] SSRF Attack Blocked with 400 Bad Request: {res.json()['detail']}")

    # 4. Initiate Audit on revlio.net
    print("\n[4] Testing Audit Creation (POST /api/audit for revlio.net)...")
    audit_id = None
    with httpx.Client(timeout=15.0) as client:
        res = client.post("http://127.0.0.1:8000/api/audit", json={"url": "revlio.net"})
        assert res.status_code == 200, f"Audit creation failed: {res.text}"
        data = res.json()
        audit_id = data["audit_id"]
        print(f"  [PASS] Audit Queued: ID={audit_id}, Domain={data['domain']}, Status={data['status']}")

    # 5. Poll Audit until Completion
    print("\n[5] Polling Audit Status (GET /api/audit/{audit_id})...")
    completed_data = None
    for attempt in range(25):
        time.sleep(1.5)
        with httpx.Client(timeout=15.0) as client:
            res = client.get(f"http://127.0.0.1:8000/api/audit/{audit_id}")
            assert res.status_code == 200
            completed_data = res.json()
            status = completed_data["status"]
            print(f"  ... attempt {attempt+1}: Status = {status}")
            if status == "completed":
                break
            elif status == "failed":
                raise Exception(f"Audit failed: {completed_data.get('error_message')}")

    assert completed_data["status"] == "completed", "Audit did not complete in time"
    scores = completed_data["scores"]
    print(f"  [PASS] Audit Completed Successfully!")
    print(f"     * Overall Score: {scores['overall']}/100 ({scores['classification']})")
    print(f"     * Security: {scores['security']}/100 | Performance: {scores['performance']}/100 | SEO: {scores['seo']}/100")
    print(f"     * Technical: {scores['technical']}/100 | Mobile: {scores['mobile']}/100 | a11y: {scores['accessibility']}/100")
    print(f"     * Issues: Critical={completed_data['critical_count']}, Warnings={completed_data['warning_count']}, Passed={completed_data['passed_count']}")
    print(f"     * Total Findings: {len(completed_data['results'])}")
    print(f"     * Technologies Detected: {len(completed_data['technologies'])}")

    # 6. Test Lead Capture and Zoho Campaigns Sync
    print("\n[6] Testing Lead Capture & Zoho Campaigns Sync (POST /api/lead)...")
    with httpx.Client(timeout=15.0) as client:
        lead_payload = {
            "audit_id": audit_id,
            "full_name": "Alexander Wright",
            "email": "alexander.wright@techinnovations.com",
            "company": "Tech Innovations Ltd",
            "phone": "+1 415-555-0188"
        }
        res = client.post("http://127.0.0.1:8000/api/lead", json=lead_payload)
        assert res.status_code == 200, f"Lead capture failed: {res.text}"
        lead_res = res.json()
        assert lead_res["success"] is True
        print(f"  [PASS] Lead Captured: Lead ID={lead_res['lead_id']}")
        print(f"     * Message: {lead_res['message']}")

    # 7. Test Recent Audits Social Proof
    print("\n[7] Testing Recent Audits Feed (GET /api/recent)...")
    with httpx.Client(timeout=15.0) as client:
        res = client.get("http://127.0.0.1:8000/api/recent")
        assert res.status_code == 200
        recent = res.json()
        print(f"  [PASS] Fetched {len(recent)} recent audits from DB.")

    # 8. Test Next.js Frontend Server
    print("\n[8] Testing Next.js Frontend (GET http://localhost:3000)...")
    with httpx.Client(timeout=25.0) as client:
        res = client.get("http://localhost:3000")
        assert res.status_code == 200, f"Frontend returned {res.status_code}"
        assert "REVLIO" in res.text, "Frontend HTML does not contain REVLIO branding"
        print(f"  [PASS] Next.js Frontend Live & Serving HTML (Status {res.status_code})")

    print("\n==================================================")
    print("   ALL LOCAL SERVER & FUNNEL TESTS PASSED 100%!  ")
    print("==================================================")

if __name__ == "__main__":
    test_all_live()
