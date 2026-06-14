# ai-network-defender

## Arquitectura del Sistema

```mermaid
graph TD
    A[Usuario / Atacante] -->|Telemetría de Red| B(FastAPI Gateway)
    B --> C{¿IP en Blacklist?}
    C -->|Sí| D[Bloqueo Automático 403]
    C -->|No| E[Inferencia IA]
    E -->|Scikit-Learn Model| F{¿Anomalía?}
    F -->|Sí| G[Añadir IP a Blacklist]
    G --> D
    F -->|No| H[Tráfico Permitido 200 OK]
    
    style B fill:#2b3440,stroke:#333,stroke-width:2px,color:#fff
    style E fill:#005b96,stroke:#333,stroke-width:2px,color:#fff
    style D fill:#a11d33,stroke:#333,stroke-width:2px,color:#fff
    style H fill:#1e7b2f,stroke:#333,stroke-width:2px,color:#fff
