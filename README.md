# Revlio Free Website Audit (audit.revlio.net)

> **Enterprise-Grade Passive Website Health, OWASP Security & Core Web Vitals Audit Funnel for Revlio.**

---

## Overview

**Revlio Free Website Audit** (`audit.revlio.net`) is a high-converting, passive website scanner and lead-generation product. It performs non-destructive, OWASP-aligned security header analysis, SSL certificate inspections, Core Web Vitals speed tests, on-page SEO evaluations, and technology fingerprinting without aggressive vulnerability payloads.

Captured leads are automatically synchronized with **Zoho Campaigns**, auto-tagged with custom audit metrics (`Website_URL`, `Audit_Score`, `Critical_Issues`, `Potential_Services`), and auto-replied via `hello@revlio.net`.

```
audit.revlio.net (Visitor)
   │
   ▼
[ Enter Target URL ]
   │
   ▼
⚡ Passive Multi-Layer Scanner
   ├── SSL/TLS Inspector & Certificate Expiry Check
   ├── OWASP Security Headers (CSP evaluation, HSTS, X-Frame-Options)
   ├── SEO & Indexability Analyzer (<title>, meta, H1, sitemaps, Open Graph)
   ├── Technology Stack Fingerprinter (CMS, Frameworks, Analytics, CDN)
   ├── Performance & Google PageSpeed Core Web Vitals (LCP, FCP, CLS, TTFB)
   └── Technical Health & Redirect Chain Inspector
   │
   ▼
📊 100-Point Weighted Scoring Engine (Security 25%, Speed 25%, SEO 20%, Tech 15%, Mobile 10%, a11y 5%)
   │
   ▼
🎯 Teaser Score & High-Priority Preview (2–3 Issues)
   │
   ▼
🔒 Lead Capture Gate (Name, Business Email, Company, Phone)
   ├── 1. Direct Sync to Zoho Campaigns Contact List
   ├── 2. Auto-Trigger Email Report Delivery from hello@revlio.net
   └── 3. Instant Lead Record in Database
   │
   ▼
🔓 Unlocked Interactive Full Report & Print/PDF Export + Revlio Strategy Session CTA
```

---

## 100-Point Weighted Scoring System

$$\text{Revlio Score} = 0.25 \times \text{Security} + 0.25 \times \text{Performance} + 0.20 \times \text{SEO} + 0.15 \times \text{Technical} + 0.10 \times \text{Mobile} + 0.05 \times \text{Accessibility}$$

| Score Range | Grade | Indicator |
|---|---|---|
| **90 – 100** | Excellent | 🟢 Green |
| **80 – 89** | Good | 🟢 Cyan |
| **70 – 79** | Needs Improvement | 🟠 Amber |
| **50 – 69** | Poor | 🔴 Orange |
| **0 – 49** | Critical | 🔴 Red |

---

## Quick Start (Local Development)

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### 2. Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
cp .env.example .env

# Run FastAPI backend on port 8000
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive API docs available at: `http://localhost:8000/docs`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to interact with the audit interface.

---

## Zoho Campaigns Integration Setup

1. Go to the [Zoho API Console](https://api-console.zoho.com) and create a **Server-based Application**.
2. Set the redirect URI and note down your `Client ID` and `Client Secret`.
3. Generate a refresh token with scope `ZohoCampaigns.contact.CREATE,ZohoCampaigns.contact.UPDATE,ZohoCampaigns.contact.READ`.
4. In Zoho Campaigns, find your target contact list's **List Key**.
5. Add the keys to `backend/.env`:
   ```env
   ZOHO_CLIENT_ID=your_client_id
   ZOHO_CLIENT_SECRET=your_client_secret
   ZOHO_REFRESH_TOKEN=your_refresh_token
   ZOHO_LIST_KEY=your_list_key
   ZOHO_REPLY_TO_EMAIL=hello@revlio.net
   ```

*Note: If Zoho credentials are not yet configured during local testing, the application safely persists all leads to the local database and returns a fallback status so zero leads are ever dropped.*

---

## Security & SSRF Safeguards

The scanner strictly adheres to passive web intelligence guidelines:
- **SSRF Protection**: Validates target DNS and resolves IP addresses against RFC 1918 private IP subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), localhost (`127.0.0.1`, `::1`), and cloud metadata (`169.254.169.254`).
- **OWASP WSTG Compliance**: Conforms with OWASP Web Security Testing Guide rules for passive reconnaissance and HTTP security headers testing.

---

## Production Deployment

- **Frontend (`audit.revlio.net`)**: Deploy to Vercel with environment variable `NEXT_PUBLIC_BACKEND_URL=https://api.audit.revlio.net`.
- **Backend**: Deploy FastAPI with Uvicorn / Gunicorn + PostgreSQL database on your VPS.

---

## License & Branding

© Revlio. Built for modern high-growth businesses. Contact: `hello@revlio.net` | [revlio.net](https://revlio.net)
