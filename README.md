1. LangGraph Workflow Design
START
  │
  ▼
Repository Loader
  │
  ▼
Supervisor
  │
  ├── Security Agent
  ├── Design Agent
  ├── Compliance Agent
  └── Test Agent
          │
          ▼
   Merge Results Node
          │
          ▼
   Final Report Node
          │
          ▼
         END





==========================================================

2. PHASE 1 — Project Setup & Basic Repo Analyzer

Upload Repository
      ↓
Read Files
      ↓
Process Code
      ↓
Store in Vector DB
      ↓
Ask AI Questions About Code