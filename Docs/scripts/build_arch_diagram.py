"""Generate the system architecture diagram for Bab 3 using mingrammer/diagrams."""
from __future__ import annotations

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Internet
from diagrams.onprem.queue import Kafka
from diagrams.onprem.storage import Ceph
from diagrams.programming.framework import Fastapi, Flutter
from diagrams.programming.language import Python

OUT = Path(__file__).resolve().parents[1] / "images" / "bab_3" / "arsitektur_sistem"
OUT.parent.mkdir(parents=True, exist_ok=True)

graph_attr = {
    "fontname": "Helvetica",
    "fontsize": "16",
    "bgcolor": "white",
    "splines": "ortho",
    "pad": "0.5",
    "nodesep": "0.6",
    "ranksep": "1.0",
}
node_attr = {
    "fontname": "Helvetica",
    "fontsize": "12",
}
edge_attr = {
    "fontname": "Helvetica",
    "fontsize": "10",
    "color": "#2c3e50",
}

with Diagram(
    "Arsitektur Sistem SmartCityApps",
    show=False,
    filename=str(OUT),
    direction="LR",
    outformat="png",
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr,
):
    citizen = Client("Warga Pelapor\n(Android)")

    with Cluster("Aplikasi Flutter"):
        flutter = Flutter("SmartCityApps\n(Riverpod + GoRouter)")

    internet = Internet("Internet\n(HTTPS)")

    with Cluster("FastAPI Server (RunPod / VPS)"):
        api = Fastapi("FastAPI\n/predict, /health")
        with Cluster("ONNX Runtime"):
            img = Python("DINOv3 large\nONNX\n(image encoder)")
            txt = Python("mE5 large\nONNX\n(text encoder)")
            cb = Python("CatBoost+PGS\nONNX\n(classifier head)")
        router = Server("Nearest Agency\nRouting\nkelas + lat/lon")

    with Cluster("Supabase (Managed)"):
        auth = Server("Auth\n(PKCE)")
        db = PostgreSQL("PostgreSQL\nprofiles\nreports\nreport_history")
        storage = Ceph("Storage\nreport-images\nbucket")
        rt = Kafka("Realtime\nWebSocket")

    citizen >> Edge(label="Pakai aplikasi") >> flutter
    flutter >> Edge(label="POST /predict\nimage + text + lat/lon") >> internet >> api
    api >> img >> Edge(label="1024d") >> cb
    api >> txt >> Edge(label="1024d") >> cb
    cb >> Edge(label="probabilitas\n9 instansi") >> router
    router >> Edge(label="instansi terdekat\n+ jarak") >> api
    api >> Edge(label="JSON response") >> internet >> flutter

    flutter >> Edge(label="Auth (sign-in,\nsession)") >> auth
    flutter >> Edge(label="CRUD reports,\nprediction, assignment,\nevidence metadata") >> db
    flutter >> Edge(label="Upload report/evidence foto") >> storage
    flutter >> Edge(label="Subscribe\nperubahan status") >> rt

print(f"wrote {OUT}.png")
