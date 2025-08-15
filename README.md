# AI Map Scaffold (Fresh Start)


- **infra/**: Docker Compose for Zookeeper, Kafka, Redis, MongoDB, and OSRM
- **backend/**: Three FastAPI services (`traffic_processor`, `crowdsourcing`, `ai_ml_service`)
- **mobile/**: A guide and script to create a fresh Expo app (recommended path)

> Tip: Open **PowerShell** in the project root and follow the steps below.

---

## 1) Bring up infra (Kafka, Redis, Mongo, OSRM shell)
```powershell
cd infra
docker compose up -d
```

If `osrm` logs say it’s waiting for `graph.osrm`, run the OSRM prep script (see §3).

## 2) Run the backend services
In **three terminals** (or one-by-one), from the `infra` folder:
```powershell
docker compose build traffic_processor crowdsourcing ai_ml_service
docker compose up -d traffic_processor crowdsourcing ai_ml_service
```

Check health:
- Traffic Processor: http://localhost:8000/health
- Crowdsourcing: http://localhost:8001/health
- AI/ML Service: http://localhost:8002/health

## 3) Prepare OSRM data (Windows PowerShell)
Download your `.osm.pbf` file (ex: `us-northeast-latest.osm.pbf`) and place it in `infra/osrm/`.
Then run:
```powershell
.\scripts\windows\prepare_osrm.ps1 -PbfPath "..\..\infra\osrm\us-northeast-latest.osm.pbf"
```

This creates `infra/osrm/graph.osrm`. Restart OSRM or wait; it will start serving on port **5000**:
- OSRM route service: http://localhost:5000

## 4) Create the mobile app (Expo)
From the project ROOT (not inside `mobile`):
```powershell
.\mobile\setup_expo.ps1
```

When it finishes:
```powershell
cd mobile\AiMapApp
npx expo start   # press "a" to open Android
```

## Notes
- Don’t mix old React Native CLI projects with a new Expo app in the same folder.
- Use Node 18 or 20 LTS and JDK 17.
- If port 8081 is busy for Metro, use `scripts/windows/kill_port.ps1 8081`.

---

## Service Overview

**traffic_processor** (port 8000): accepts traffic/incident payloads (designed to publish to Kafka and cache via Redis).  
**crowdsourcing** (port 8001): stores user reports to MongoDB (fallback to in-memory store if Mongo is down).  
**ai_ml_service** (port 8002): returns simple route advice stubs (ready to swap in ONNX / TF later).

All three expose `/health` for quick checks.
