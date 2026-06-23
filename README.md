<div align="center">

<img src="https://github.com/Vexel-Innovations.png" alt="Vexel Innovations" width="120"/>

# 🛰️ Sentinel-X

**The autonomous multimodal intelligence platform for 3D situational awareness, drone swarm orchestration, and proactive urban defense.**

[Quickstart](https://github.com/Vexel-Innovations/Sentinel-X#-quickstart) · [Docs](https://github.com/Vexel-Innovations/Sentinel-X/wiki) · [Architecture](https://github.com/Vexel-Innovations/Sentinel-X#-architecture) · [Contributing](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/CONTRIBUTING.md) · [Discussions](https://github.com/Vexel-Innovations/Sentinel-X/discussions)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/Dockerfile)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/CONTRIBUTING.md)
[![All Contributors](https://img.shields.io/badge/all_contributors-welcome-orange.svg)](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/CONTRIBUTING.md)

</div>

---

Sentinel-X is a production-grade, open-source intelligence platform that fuses **computer vision**, **acoustic sensing**, **satellite imagery**, **drone telemetry**, and **NLP** into a single autonomous decision engine. It is designed for national security operations, urban safety monitoring, and proactive threat detection.

It runs on your own infrastructure with full **data sovereignty** — no cloud dependency, no third-party data sharing.

- [**Self-host on your server**](https://github.com/Vexel-Innovations/Sentinel-X#option-2-docker-recommended) — Full control, full privacy
- [**3D Digital Twin**](https://github.com/Vexel-Innovations/Sentinel-X#-3d-digital-twin) — Real-time CesiumJS situational awareness
- [**Autonomous drone response**](https://github.com/Vexel-Innovations/Sentinel-X#-autonomous-drone-swarms) — Detect → Triangulate → Dispatch
- [**Military-standard symbology**](https://github.com/Vexel-Innovations/Sentinel-X#-c4isr--interoperability) — MIL-STD-2525D compliant
- [**Field sync with ATAK**](https://github.com/Vexel-Innovations/Sentinel-X#-c4isr--interoperability) — Push intel to agents' handheld devices
- [**Every contribution welcome**](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/CONTRIBUTING.md) — From typo fixes to new AI modules

---

## 🚀 Quickstart

You can deploy Sentinel-X on your laptop, a dedicated server, or in the cloud.

### Option 1: From Source

> **Prerequisites:** Python 3.11+, pip, MongoDB

```bash
git clone https://github.com/Vexel-Innovations/Sentinel-X.git
cd Sentinel-X
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Access the API at [http://localhost:8000/docs](http://localhost:8000/docs).
Access the Dashboard at [http://localhost/frontend/dashboard.php](http://localhost/frontend/dashboard.php).

### Option 2: Docker (Recommended)

> **Prerequisites:** Docker, Docker Compose

```bash
git clone https://github.com/Vexel-Innovations/Sentinel-X.git
cd Sentinel-X
docker-compose up -d
```

This starts both the **AI Engine** (port 8000) and **MongoDB** automatically.

### Option 3: Pull from GitHub Packages

```bash
docker pull ghcr.io/vexel-innovations/sentinel-x:latest
docker run -p 8000:8000 ghcr.io/vexel-innovations/sentinel-x:latest
```

---

## 🧠 Core Capabilities

### 🎯 High-Precision Vision AI

| Feature | Description |
| :--- | :--- |
| **SAHI** | Sliced Aided Hyper Inference — detects tiny objects in 4K/8K aerial feeds |
| **Super-Resolution** | AI-driven 2x upscaling of target crops for pinpoint identification |
| **Person Re-ID** | Soft Attribute Signatures to track targets across drones ↔ CCTV |
| **Crowd Intelligence** | Real-time density mapping (PPSM) and panic flow detection |

### 🚁 Autonomous Drone Swarms

| Feature | Description |
| :--- | :--- |
| **Formation Control** | Circle (360° surveillance) and Grid (area search) patterns |
| **Target Locking** | Predictive trajectory estimation using Kalman-filtering patterns |
| **Auto-Dispatch** | Acoustic event → GPS triangulation → Swarm deployment (zero human input) |

### 🔊 Acoustic & Signal Intelligence

| Feature | Description |
| :--- | :--- |
| **Triangulation** | Weighted centroid calculation from multi-sensor RSSI data |
| **SIGINT** | RF frequency spike analysis to identify hidden electronic signatures |
| **Auto-Response** | Kinetic events (gunshots) trigger autonomous drone dispatch |

### 🛡️ C4ISR & Interoperability

| Feature | Description |
| :--- | :--- |
| **MIL-STD-2525D** | NATO/US standard tactical symbology for all mapped assets |
| **ATAK / CoT** | Push Cursor-on-Target XML to field agents' Android Tactical Kits |
| **3D Digital Twin** | CesiumJS-powered terrain rendering with real-time data overlays |

### 🛰️ Satellite & GeoAI

| Feature | Description |
| :--- | :--- |
| **Change Detection** | Identify structural changes in high-security zones via NDVI analysis |
| **Conflict Prediction** | Vegetation health monitoring for herder-farmer conflict early warning |

---

## 🏗️ Architecture

Sentinel-X is built as a modular, event-driven system where each intelligence domain operates as an independent service, fused by a central decision engine.

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                          │
│                  CesiumJS 3D Digital Twin                       │
│              MIL-STD-2525D Tactical Symbology                  │
└────────────────────────┬────────────────────────────────────────┘
                         │ REST API
┌────────────────────────┴────────────────────────────────────────┐
│                      FastAPI GATEWAY                            │
│               /api/v1/vision  /api/v1/drone  /api/v1/iot       │
└───┬────────┬────────┬────────┬────────┬────────┬───────────────┘
    │        │        │        │        │        │
┌───┴──┐ ┌──┴──┐ ┌──┴───┐ ┌──┴──┐ ┌──┴───┐ ┌──┴──┐
│Vision│ │Drone│ │ IoT  │ │ NLP │ │ SAT  │ │ CoT │
│  AI  │ │Swarm│ │Sensor│ │ LLM │ │GeoAI │ │ATAK │
└───┬──┘ └──┬──┘ └──┬───┘ └──┬──┘ └──┬───┘ └──┬──┘
    │        │        │        │        │        │
┌───┴────────┴────────┴────────┴────────┴────────┴───────────────┐
│                     🧠 FUSION ENGINE                            │
│           Anomaly Detection → Threat Assessment →               │
│           Autonomous Response → Ethical Guardrails              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                    ┌────┴────┐
                    │ MongoDB │
                    └─────────┘
```

Each module can be developed, tested, and deployed independently. The Fusion Engine orchestrates all modules into a unified intelligence pipeline.

---

## 📚 More Documentation

- [Architecture Overview](https://github.com/Vexel-Innovations/Sentinel-X/wiki)
- [API Reference](http://localhost:8000/docs) *(after starting the server)*
- [Deployment Guide](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/docker-compose.yml)
- [Contributing Guide](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/CONTRIBUTING.md)
- [Security Policy](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/SECURITY.md)
- [Code of Conduct](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/CODE_OF_CONDUCT.md)

---

## 🤝 Contributing

We welcome contributions of **all sizes** — from fixing a typo to building a new AI module. **No contribution is too small.**

See our [Contributing Guide](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/CONTRIBUTING.md) for:
- 🟢 Beginner-friendly tasks
- 🟡 Intermediate challenges
- 🔴 Advanced AI/Defense engineering

> *Every expert was once a beginner. Your journey with Sentinel-X starts now.* 🌍

---

## 📜 License

This project is licensed under the [Apache License 2.0](https://github.com/Vexel-Innovations/Sentinel-X/blob/main/LICENSE).

---

<div align="center">

**Built with 🧠 by [Vexel Innovations](https://github.com/Vexel-Innovations)**

*From Nigeria to the World — Building Intelligence, Together.*

</div>
