# 🗂️ Tree Structure Generator

A simple Python script to create a full project directory and file structure from a manifest file.  
This is especially useful for initializing new projects or quickly scaffolding a known architecture.

## 📘 Example

**structure.txt**
```
R: shipit-backend
  R: app
    F: main.py
    R: api
      F: routes.py
    R: services
      F: fedex.py
    R: models
      F: shipment.py
    F: database.py
    F: config.py
  F: requirements.txt
  F: Dockerfile
  F: .env
```

This manifest corresponds to the following directory tree:

```
shipit-backend/
├── app/
│   ├── main.py             # Entry point (runs FastAPI)
│   ├── api/
│   │   └── routes.py       # All API endpoints
│   ├── services/
│   │   └── fedex.py        # Logic for calling FedEx API
│   ├── models/
│   │   └── shipment.py     # Database models
│   ├── database.py         # DB connection
│   └── config.py           # App settings (like API keys, mode, etc.)
├── requirements.txt
├── Dockerfile
└── .env
```

Run this with:
```bash
python Tree_generator.py structure.txt
```

This will create the full folder tree and all empty files listed in `structure.txt`.

## 🆕 Latest Changes
- **Full sync mode** – aligns the directory structure exactly with `structure.txt`:  
  - Creates missing files/folders.  
  - Permanently removes items not listed.  
- **Idempotent** – no changes occur on repeated runs unless the manifest is modified.  
  - Adding lines → creates new items.  
  - Removing lines → deletes corresponding items.  
- **2-space indentation** – defines hierarchy levels in the manifest.  
- **Verbose logging** – clear output for every created or deleted item.  

## 🛠️ How it works

- `R:` stands for a directory (folder)
- `F:` stands for a file
- Indentation with **2 spaces** defines depth
