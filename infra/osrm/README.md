# OSRM Data

Place your `.osm.pbf` file here (e.g., `us-northeast-latest.osm.pbf`).  
Then run the PowerShell script:

```powershell
..\..\scripts\windows\prepare_osrm.ps1 -PbfPath ".\us-northeast-latest.osm.pbf"
```

This will create `graph.osrm` used by the `osrm` service.
