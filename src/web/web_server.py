"""
NeuraBot Web Control Panel
Flask + SocketIO server for browser-based control.
"""

import base64
import cv2
import threading
from flask import Flask, render_template_string, jsonify, request
from flask_socketio import SocketIO, emit
from loguru import logger

WEB_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>NeuraBot Control Panel</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.6.1/socket.io.min.js"></script>
<style>
  :root { --bg:#0d1117; --card:#161b22; --accent:#238636; --text:#e6edf3; --sub:#8b949e; --red:#da3633; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--text); font-family:'Segoe UI',sans-serif; padding:20px; }
  h1 { text-align:center; margin-bottom:20px; font-size:1.6rem; }
  .grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; max-width:900px; margin:0 auto; }
  .card { background:var(--card); border-radius:12px; padding:16px; border:1px solid #30363d; }
  .card h2 { font-size:.9rem; color:var(--sub); margin-bottom:12px; text-transform:uppercase; letter-spacing:.08em; }
  .dpad { display:grid; grid-template-columns:repeat(3,52px); grid-template-rows:repeat(3,52px); gap:6px; margin:0 auto; width:fit-content; }
  .btn { background:#21262d; border:1px solid #30363d; border-radius:8px; color:var(--text); font-size:1.2rem; cursor:pointer; transition:.15s; display:flex; align-items:center; justify-content:center; }
  .btn:hover { background:#30363d; }
  .btn:active { background:var(--accent); }
  .btn.action { background:var(--accent); padding:8px 16px; border-radius:8px; font-size:.85rem; width:100%; margin:4px 0; }
  .btn.action:hover { filter:brightness(1.2); }
  .btn.stop { background:var(--red); }
  #camera { width:100%; border-radius:8px; background:#000; aspect-ratio:4/3; object-fit:cover; }
  .stat { display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #21262d; font-size:.85rem; }
  .stat:last-child { border:none; }
  .stat span:last-child { color:var(--accent); font-weight:600; }
  #status-dot { width:10px; height:10px; border-radius:50%; background:#da3633; display:inline-block; margin-right:8px; }
  #status-dot.connected { background:var(--accent); }
  .log { font-size:.75rem; color:var(--sub); height:100px; overflow-y:auto; font-family:monospace; }
</style>
</head>
<body>
<h1>🐾 NeuraBot Control Panel</h1>
<div class="grid">

  <!-- Camera -->
  <div class="card" style="grid-column:1/-1">
    <h2>📷 Camera Feed</h2>
    <img id="camera" src="" alt="Camera Feed"/>
  </div>

  <!-- D-Pad -->
  <div class="card">
    <h2>🕹️ Movement</h2>
    <div class="dpad">
      <div></div>
      <button class="btn" onmousedown="move('forward')" onmouseup="move('stop')">▲</button>
      <div></div>
      <button class="btn" onmousedown="move('left')" onmouseup="move('stop')">◀</button>
      <button class="btn stop" onclick="move('stop')">■</button>
      <button class="btn" onmousedown="move('right')" onmouseup="move('stop')">▶</button>
      <div></div>
      <button class="btn" onmousedown="move('backward')" onmouseup="move('stop')">▼</button>
      <div></div>
    </div>
  </div>

  <!-- Actions -->
  <div class="card">
    <h2>⚡ Actions</h2>
    <button class="btn action" onclick="action('stand')">🧍 Stand</button>
    <button class="btn action" onclick="action('sit')">🐾 Sit</button>
    <button class="btn action" onclick="action('trot')">🏃 Trot</button>
    <button class="btn action" onclick="action('shake')">🤝 Shake</button>
  </div>

  <!-- Stats -->
  <div class="card">
    <h2>📊 System Status</h2>
    <div class="stat"><span>Connection</span><span><span id="status-dot"></span><span id="conn-label">Disconnected</span></span></div>
    <div class="stat"><span>Battery</span><span id="battery">--</span></div>
    <div class="stat"><span>Current</span><span id="current">--</span></div>
    <div class="stat"><span>Vision FPS</span><span id="fps">--</span></div>
    <div class="stat"><span>Gait</span><span id="gait">--</span></div>
    <div class="stat"><span>Detections</span><span id="detections">--</span></div>
  </div>

  <!-- Log -->
  <div class="card">
    <h2>📝 Event Log</h2>
    <div class="log" id="log"></div>
  </div>

</div>

<script>
  const socket = io();
  const dot = document.getElementById('status-dot');
  const connLabel = document.getElementById('conn-label');

  socket.on('connect', () => {
    dot.classList.add('connected');
    connLabel.textContent = 'Connected';
    log('Connected to NeuraBot');
  });
  socket.on('disconnect', () => {
    dot.classList.remove('connected');
    connLabel.textContent = 'Disconnected';
    log('Disconnected');
  });
  socket.on('telemetry', (d) => {
    document.getElementById('battery').textContent  = d.battery_v?.toFixed(2) + 'V (' + d.soc?.toFixed(0) + '%)';
    document.getElementById('current').textContent  = d.current_ma?.toFixed(0) + ' mA';
    document.getElementById('fps').textContent      = d.vision_fps?.toFixed(1);
    document.getElementById('gait').textContent     = d.gait;
    document.getElementById('detections').textContent = d.detections?.join(', ') || 'none';
  });
  socket.on('frame', (data) => {
    document.getElementById('camera').src = 'data:image/jpeg;base64,' + data;
  });

  function move(dir) {
    const vel = { forward:[0.3,0,0], backward:[-0.3,0,0], left:[0,0.2,0], right:[0,-0.2,0], stop:[0,0,0] };
    socket.emit('move', { vx: vel[dir][0], vy: vel[dir][1], wz: vel[dir][2] });
  }
  function action(cmd) {
    socket.emit('action', { cmd });
    log('Action: ' + cmd);
  }
  function log(msg) {
    const el = document.getElementById('log');
    el.innerHTML += new Date().toLocaleTimeString() + ' — ' + msg + '<br/>';
    el.scrollTop = el.scrollHeight;
  }
</script>
</body>
</html>
"""


class WebServer:
    def __init__(self, config: dict, gait, vision, speech, power):
        self.config  = config
        self.gait    = gait
        self.vision  = vision
        self.speech  = speech
        self.power   = power
        self._thread = None

        self.app = Flask(__name__)
        self.sio = SocketIO(self.app, cors_allowed_origins="*", async_mode="eventlet")
        self._register_routes()

    def _register_routes(self):
        @self.app.route("/")
        def index():
            return render_template_string(WEB_HTML)

        @self.sio.on("move")
        def on_move(data):
            self.gait.set_velocity(data.get("vx",0), data.get("vy",0), data.get("wz",0))

        @self.sio.on("action")
        def on_action(data):
            from src.control.gait_controller import Gait
            cmd = data.get("cmd", "")
            gait_map = {"stand": Gait.STAND, "sit": Gait.SIT,
                        "trot": Gait.TROT, "shake": Gait.SHAKE}
            if cmd in gait_map:
                self.gait.set_gait(gait_map[cmd])
            logger.info(f"Web action: {cmd}")

    def _emit_loop(self):
        import eventlet
        while True:
            # Telemetry
            pwr = self.power.get_main()
            vis = self.vision.get_state() if hasattr(self.vision, 'get_state') else None
            dets = [d.label for d in vis.detections] if vis else []
            self.sio.emit("telemetry", {
                "battery_v":  pwr.bus_voltage,
                "soc":        pwr.soc_percent,
                "current_ma": pwr.current,
                "vision_fps": vis.fps if vis else 0,
                "gait":       self.gait.current_gait.value,
                "detections": dets,
            })

            # Camera frame
            if vis and vis.frame is not None:
                frame = self.vision.annotated_frame()
                if frame is not None:
                    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
                    self.sio.emit("frame", base64.b64encode(buf).decode())

            eventlet.sleep(0.1)

    def start(self):
        host = self.config.get("host", "0.0.0.0")
        port = self.config.get("port", 5000)
        self._thread = threading.Thread(
            target=lambda: self.sio.run(self.app, host=host, port=port, log_output=False),
            daemon=True,
        )
        self._thread.start()
        self.sio.start_background_task(self._emit_loop)
        logger.success(f"Web control panel at http://{host}:{port}")

    def stop(self):
        pass
