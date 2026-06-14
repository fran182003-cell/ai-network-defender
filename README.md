

# AI Network Defender 

Sistema completo de ciberseguridad impulsado por Inteligencia Artificial. Este repositorio implementa un pipeline MLOps y un microservicio seguro capaz de ingerir telemetría de red, analizarla mediante algoritmos no supervisados y aplicar políticas defensivas en tiempo real.

## Arquitectura del Sistema

```mermaid
graph TD
    A[Tráfico de Red] -->|Ingesta JSON| B(FastAPI Gateway + JWT Auth)
    B --> C{¿IP en Caché Blacklist?}
    C -->|Sí| D[Drop: 403 Forbidden]
    C -->|No| E[Inferencia IA]
    E -->|Isolation Forest Model| F{¿Es Anomalía?}
    F -->|Sí| G[Actualizar Blacklist State]
    G --> D
    F -->|No| H[Allow: 200 OK]
    
    style B fill:#2b3440,stroke:#333,stroke-width:2px,color:#fff
    style E fill:#005b96,stroke:#333,stroke-width:2px,color:#fff
    style D fill:#a11d33,stroke:#333,stroke-width:2px,color:#fff
    style H fill:#1e7b2f,stroke:#333,stroke-width:2px,color:#fff
