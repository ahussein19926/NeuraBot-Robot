<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>NeuraBot</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500&display=swap');

:root {
  --c1: #7F77DD;
  --c2: #1D9E75;
  --c3: #EF9F27;
  --c4: #D4537E;
  --dim1: rgba(127,119,221,0.08);
  --dim2: rgba(29,158,117,0.08);
  --line: rgba(127,119,221,0.18);
  --line2: rgba(29,158,117,0.15);
  --bg: #0d1117;
  --bg2: #161b22;
  --bg3: #21262d;
  --text: #e6edf3;
  --text2: #8b949e;
  --text3: #484f58;
  --border: rgba(127,119,221,0.18);
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; }

.nb { overflow: hidden; }

/* HERO */
.hero {
  position: relative;
  padding: 60px 32px 48px;
  text-align: center;
  border-bottom: 0.5px solid var(--border);
  overflow: hidden;
}
.hero-rings { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); pointer-events: none; }
.ring { position: absolute; border-radius: 50%; border: 0.5px solid; transform: translate(-50%,-50%); top: 0; left: 0; }
.r1 { width: 260px; height: 260px; border-color: rgba(127,119,221,0.14); }
.r2 { width: 420px; height: 420px; border-color: rgba(127,119,221,0.09); }
.r3 { width: 580px; height: 580px; border-color: rgba(127,119,221,0.05); }
.r4 { width: 740px; height: 740px; border-color: rgba(29,158,117,0.06); }
.scan-line { position: absolute; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, #7F77DD, #1D9E75, transparent); opacity: 0.25; top: 35%; }

.hero-eyebrow {
  font-family: 'Space Mono', monospace;
  font-size: 10px; letter-spacing: .22em; color: var(--c2);
  margin-bottom: 18px;
  display: flex; align-items: center; justify-content: center; gap: 12px;
}
.hero-eyebrow::before, .hero-eyebrow::after { content: ''; width: 50px; height: 0.5px; background: var(--c2); opacity: .4; }

.hero-name {
  font-family: 'Orbitron', monospace;
  font-size: 64px; font-weight: 900; letter-spacing: .06em; line-height: 1;
  margin: 0 0 8px; color: var(--text);
}
.hero-name-accent { color: var(--c1); }
.hero-tagline {
  font-family: 'Space Mono', monospace;
  font-size: 11px; letter-spacing: .18em; color: var(--text2);
  margin: 0 0 28px;
}

.badge-row { display: flex; flex-wrap: wrap; gap: 7px; justify-content: center; margin-bottom: 32px; }
.pill {
  font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: .08em;
  padding: 4px 14px; border-radius: 99px; border: 0.5px solid;
}
.pill-p { border-color: #534AB7; color: #AFA9EC; background: rgba(127,119,221,0.12); }
.pill-t { border-color: #0F6E56; color: #5DCAA5; background: rgba(29,158,117,0.12); }
.pill-a { border-color: #854F0B; color: #EF9F27; background: rgba(239,159,39,0.10); }
.pill-k { border-color: #993556; color: #ED93B1; background: rgba(212,83,126,0.10); }
.pill-b { border-color: #185FA5; color: #85B7EB; background: rgba(55,138,221,0.10); }

.stat-row {
  display: flex; justify-content: center;
  border: 0.5px solid var(--border); border-radius: 8px; overflow: hidden;
  max-width: 520px; margin: 0 auto;
}
.stat-box { flex: 1; padding: 12px 8px; text-align: center; border-right: 0.5px solid var(--border); }
.stat-box:last-child { border-right: none; }
.stat-val { font-family: 'Orbitron', monospace; font-size: 20px; font-weight: 700; line-height: 1; margin-bottom: 5px; }
.sv-p { color: var(--c1); }
.sv-t { color: var(--c2); }
.sv-a { color: var(--c3); }
.sv-k { color: var(--c4); }
.stat-lbl { font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: .1em; color: var(--text3); }

/* SECTIONS */
.section { padding: 32px; border-bottom: 0.5px solid var(--border); }
.sec-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.sec-num { font-family: 'Orbitron', monospace; font-size: 11px; color: var(--c1); opacity: .4; }
.sec-title { font-family: 'Orbitron', monospace; font-size: 13px; font-weight: 700; letter-spacing: .1em; color: var(--text); }
.sec-line { flex: 1; height: 0.5px; background: var(--border); }

/* ROBOT HERO IMAGE */
.robot-hero-img {
  border: 0.5px solid var(--border); border-radius: 10px; overflow: hidden;
  position: relative; aspect-ratio: 16/7; background: rgba(127,119,221,0.05);
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px;
}
.robot-hero-img::before {
  content: ''; position: absolute; inset: 0;
  background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px);
  background-size: 32px 32px; opacity: .5;
}
.img-corner { position: absolute; width: 16px; height: 16px; border-color: var(--c1); border-style: solid; }
.img-corner.tl { top: 12px; left: 12px; border-width: 2px 0 0 2px; }
.img-corner.tr { top: 12px; right: 12px; border-width: 2px 2px 0 0; }
.img-corner.bl { bottom: 12px; left: 12px; border-width: 0 0 2px 2px; }
.img-corner.br { bottom: 12px; right: 12px; border-width: 0 2px 2px 0; }
.img-scan { position: absolute; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, var(--c1), transparent); opacity: 0.18; top: 50%; }
.img-ph-icon { font-size: 56px; color: var(--c1); opacity: .2; position: relative; z-index: 1; }
.img-ph-label { font-family: 'Space Mono', monospace; font-size: 11px; letter-spacing: .18em; color: var(--c1); opacity: .4; position: relative; z-index: 1; }
.img-ph-path { font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: .1em; color: var(--text3); position: relative; z-index: 1; }

/* BUILD GALLERY */
.parts-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.part-img {
  border: 0.5px solid var(--border); border-radius: 8px; overflow: hidden;
  position: relative; aspect-ratio: 4/3; background: rgba(127,119,221,0.05);
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px;
}
.part-img::before {
  content: ''; position: absolute; inset: 0;
  background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px);
  background-size: 22px 22px; opacity: .4;
}
.p-t { background: rgba(29,158,117,0.05); }
.p-a { background: rgba(239,159,39,0.05); }
.p-k { background: rgba(212,83,126,0.05); }
.p-b { background: rgba(55,138,221,0.05); }

.part-icon { font-size: 30px; position: relative; z-index: 1; opacity: .3; }
.p-p .part-icon { color: var(--c1); }
.p-t .part-icon { color: var(--c2); }
.p-a .part-icon { color: var(--c3); }
.p-k .part-icon { color: var(--c4); }
.p-b .part-icon { color: #85B7EB; }

.part-tag { font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: .12em; position: relative; z-index: 1; opacity: .6; }
.p-p .part-tag { color: var(--c1); }
.p-t .part-tag { color: var(--c2); }
.p-a .part-tag { color: var(--c3); }
.p-k .part-tag { color: var(--c4); }
.p-b .part-tag { color: #85B7EB; }

.part-name { font-size: 11px; font-weight: 500; position: relative; z-index: 1; text-align: center; padding: 0 10px; color: var(--text2); }
.part-bottom {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 6px 10px; background: rgba(13,17,23,0.7);
  border-top: 0.5px solid var(--border);
  font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: .07em;
  color: var(--text3); z-index: 1;
  display: flex; align-items: center; justify-content: space-between;
}
.part-dot { width: 5px; height: 5px; border-radius: 50%; opacity: .35; }
.p-p .part-dot { background: var(--c1); }
.p-t .part-dot { background: var(--c2); }
.p-a .part-dot { background: var(--c3); }
.p-k .part-dot { background: var(--c4); }
.p-b .part-dot { background: #85B7EB; }

/* CAPABILITY */
.mod-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.mod-card { border: 0.5px solid var(--border); border-radius: 8px; padding: 16px; position: relative; overflow: hidden; background: var(--bg2); }
.mod-card::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px; }
.mc-p::after { background: var(--c1); }
.mc-t::after { background: var(--c2); }
.mc-a::after { background: var(--c3); }
.mc-k::after { background: var(--c4); }
.mc-b::after { background: #378ADD; }
.mod-id { font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: .12em; margin-bottom: 10px; }
.mc-p .mod-id { color: var(--c1); }
.mc-t .mod-id { color: var(--c2); }
.mc-a .mod-id { color: var(--c3); }
.mc-k .mod-id { color: var(--c4); }
.mc-b .mod-id { color: #85B7EB; }
.mod-icon-wrap { font-size: 24px; margin-bottom: 10px; }
.mc-p .mod-icon-wrap { color: var(--c1); }
.mc-t .mod-icon-wrap { color: var(--c2); }
.mc-a .mod-icon-wrap { color: var(--c3); }
.mc-k .mod-icon-wrap { color: var(--c4); }
.mc-b .mod-icon-wrap { color: #85B7EB; }
.mod-name { font-size: 13px; font-weight: 500; margin-bottom: 5px; color: var(--text); }
.mod-desc { font-size: 11px; color: var(--text2); line-height: 1.6; }

/* ARCH */
.arch-wrap { border: 0.5px solid var(--border); border-radius: 8px; overflow: hidden; }
.arch-layer { font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: .15em; padding: 7px 14px; background: rgba(127,119,221,0.07); border-bottom: 0.5px solid var(--border); color: var(--c1); }
.arch-layer.g { color: var(--c2); background: rgba(29,158,117,0.07); }
.arch-layer.a { color: var(--c3); background: rgba(239,159,39,0.07); }
.arch-row { display: flex; border-bottom: 0.5px solid var(--border); }
.arch-row:last-child { border-bottom: none; }
.arch-cell { flex: 1; padding: 11px 14px; border-right: 0.5px solid var(--border); }
.arch-cell:last-child { border-right: none; }
.ac-tag { font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: .1em; color: var(--c1); margin-bottom: 4px; }
.ac-tag.g { color: var(--c2); }
.ac-tag.a { color: var(--c3); }
.ac-name { font-size: 12px; font-weight: 500; margin-bottom: 3px; color: var(--text); }
.ac-sub { font-size: 11px; color: var(--text2); }
.conn-row { display: flex; justify-content: center; align-items: center; padding: 9px 0; gap: 10px; border-bottom: 0.5px solid var(--border); }
.conn-tag { font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: .1em; color: var(--text3); padding: 3px 10px; border: 0.5px dashed var(--border); border-radius: 99px; }
.conn-line { flex: 1; height: 0.5px; background: var(--border); max-width: 70px; }

/* ROADMAP */
.road-wrap { display: flex; flex-direction: column; }
.road-item { display: flex; align-items: center; gap: 14px; padding: 10px 0; border-bottom: 0.5px solid var(--border); font-size: 13px; }
.road-item:last-child { border-bottom: none; }
.road-node { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; position: relative; }
.road-node.done { background: var(--c2); }
.road-node.next { background: transparent; border: 1.5px solid var(--c1); }
.road-node.next::after { content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); width: 4px; height: 4px; background: var(--c1); border-radius: 50%; }
.road-label { flex: 1; color: var(--text); }
.road-label.done-t { color: var(--text2); }
.road-ver { font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: .06em; color: var(--text3); }
.road-ver.active { color: var(--c1); }
.road-tag-done { font-family: 'Space Mono', monospace; font-size: 9px; background: rgba(29,158,117,0.1); color: #5DCAA5; border: 0.5px solid rgba(29,158,117,0.25); padding: 2px 8px; border-radius: 99px; }
.road-tag-next { font-family: 'Space Mono', monospace; font-size: 9px; background: rgba(127,119,221,0.1); color: #AFA9EC; border: 0.5px solid rgba(127,119,221,0.25); padding: 2px 8px; border-radius: 99px; }

/* FOOTER */
.footer {
  padding: 16px 32px;
  display: flex; align-items: center; justify-content: space-between;
  font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: .1em; color: var(--text3);
  border-top: 0.5px solid var(--border);
}
.footer-brand { color: var(--c1); font-weight: 700; letter-spacing: .16em; }
.footer-pulse { display: inline-flex; align-items: center; gap: 7px; }
.pulse-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--c2); display: inline-block; }
</style>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css"/>

<div class="nb">

  <div class="hero">
    <div class="hero-rings">
      <div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="ring r4"></div>
    </div>
    <div class="scan-line"></div>
    <div class="hero-eyebrow">UNIT-NB01 &nbsp;·&nbsp; QUADRUPED PLATFORM &nbsp;·&nbsp; OPEN BUILD</div>
    <div class="hero-name">NEURA<span class="hero-name-accent">BOT</span></div>
    <div class="hero-tagline">AI-POWERED ROBOT DOG &nbsp;//&nbsp; VISION · SPEECH · GAIT · AUTONOMY</div>
    <div class="badge-row">
      <span class="pill pill-p">RPi / Jetson</span>
      <span class="pill pill-b">Dual ESP32</span>
      <span class="pill pill-t">YOLOv8 Vision</span>
      <span class="pill pill-a">Whisper STT</span>
      <span class="pill pill-k">Coqui TTS</span>
      <span class="pill pill-p">12-DOF IK</span>
      <span class="pill pill-t">3S LiPo Power</span>
      <span class="pill pill-a">Web Control</span>
    </div>
    <div class="stat-row">
      <div class="stat-box"><div class="stat-val sv-p">12</div><div class="stat-lbl">SERVOS</div></div>
      <div class="stat-box"><div class="stat-val sv-t">50Hz</div><div class="stat-lbl">IK RATE</div></div>
      <div class="stat-box"><div class="stat-val sv-a">15fps</div><div class="stat-lbl">VISION AI</div></div>
      <div class="stat-box"><div class="stat-val sv-k">4</div><div class="stat-lbl">LEGS</div></div>
      <div class="stat-box"><div class="stat-val sv-p">3S</div><div class="stat-lbl">LIPO</div></div>
    </div>
  </div>

  <!-- 01 UNIT OVERVIEW -->
  <div class="section">
    <div class="sec-header">
      <span class="sec-num">01</span>
      <span class="sec-title">UNIT OVERVIEW</span>
      <div class="sec-line"></div>
    </div>
    <div class="robot-hero-img">
      <div class="img-corner tl"></div><div class="img-corner tr"></div>
      <div class="img-corner bl"></div><div class="img-corner br"></div>
      <div class="img-scan"></div>
      <div class="img-ph-icon"><i class="ti ti-robot"></i></div>
      <div class="img-ph-label">NEURABOT // FULL UNIT PHOTO</div>
      <div class="img-ph-path">docs/images/neurabot_hero.jpg</div>
    </div>
  </div>

  <!-- 02 BUILD GALLERY -->
  <div class="section">
    <div class="sec-header">
      <span class="sec-num">02</span>
      <span class="sec-title">BUILD GALLERY</span>
      <div class="sec-line"></div>
    </div>
    <div class="parts-grid">
      <div class="part-img p-p">
        <div class="part-icon"><i class="ti ti-layout-grid"></i></div>
        <div class="part-tag">STRUC // CHASSIS</div>
        <div class="part-name">Body frame &amp; leg assembly</div>
        <div class="part-bottom"><span>build_chassis.jpg</span><span class="part-dot"></span></div>
      </div>
      <div class="part-img p-t">
        <div class="part-icon"><i class="ti ti-rotate-clockwise"></i></div>
        <div class="part-tag">ACT // SERVOS</div>
        <div class="part-name">12× servo installation</div>
        <div class="part-bottom"><span>build_servos.jpg</span><span class="part-dot"></span></div>
      </div>
      <div class="part-img p-a">
        <div class="part-icon"><i class="ti ti-bolt"></i></div>
        <div class="part-tag">PWR // POWER SYS</div>
        <div class="part-name">Power distribution &amp; LiPo bay</div>
        <div class="part-bottom"><span>build_power.jpg</span><span class="part-dot"></span></div>
      </div>
      <div class="part-img p-b">
        <div class="part-icon"><i class="ti ti-cpu"></i></div>
        <div class="part-tag">COMP // SBC + ESP32</div>
        <div class="part-name">Raspberry Pi &amp; dual ESP32 mount</div>
        <div class="part-bottom"><span>build_electronics.jpg</span><span class="part-dot"></span></div>
      </div>
      <div class="part-img p-k">
        <div class="part-icon"><i class="ti ti-device-desktop"></i></div>
        <div class="part-tag">PERIPH // HEAD</div>
        <div class="part-name">Display, camera &amp; mic array</div>
        <div class="part-bottom"><span>build_head.jpg</span><span class="part-dot"></span></div>
      </div>
      <div class="part-img p-p">
        <div class="part-icon"><i class="ti ti-wave-sine"></i></div>
        <div class="part-tag">WIRE // HARNESS</div>
        <div class="part-name">Cable routing &amp; wiring harness</div>
        <div class="part-bottom"><span>build_wiring.jpg</span><span class="part-dot"></span></div>
      </div>
      <div class="part-img p-t">
        <div class="part-icon"><i class="ti ti-printer"></i></div>
        <div class="part-tag">3DP // PARTS</div>
        <div class="part-name">3D printed components laid out</div>
        <div class="part-bottom"><span>build_3dparts.jpg</span><span class="part-dot"></span></div>
      </div>
      <div class="part-img p-a">
        <div class="part-icon"><i class="ti ti-vector-triangle"></i></div>
        <div class="part-tag">IK // GAIT TEST</div>
        <div class="part-name">First walk — IK gait in action</div>
        <div class="part-bottom"><span>build_gait_test.jpg</span><span class="part-dot"></span></div>
      </div>
      <div class="part-img p-b">
        <div class="part-icon"><i class="ti ti-sparkles"></i></div>
        <div class="part-tag">FINAL // COMPLETE</div>
        <div class="part-name">Fully assembled NeuraBot</div>
        <div class="part-bottom"><span>build_final.jpg</span><span class="part-dot"></span></div>
      </div>
    </div>
  </div>

  <!-- 03 CAPABILITY MATRIX -->
  <div class="section">
    <div class="sec-header">
      <span class="sec-num">03</span>
      <span class="sec-title">CAPABILITY MATRIX</span>
      <div class="sec-line"></div>
    </div>
    <div class="mod-grid">
      <div class="mod-card mc-p">
        <div class="mod-id">MOD // IK-ENGINE</div>
        <div class="mod-icon-wrap"><i class="ti ti-vector-triangle"></i></div>
        <div class="mod-name">Inverse Kinematics</div>
        <div class="mod-desc">Geometric 3-DOF solver per leg. Trot, walk, sit, shake gaits at 50 Hz</div>
      </div>
      <div class="mod-card mc-t">
        <div class="mod-id">MOD // VISION-AI</div>
        <div class="mod-icon-wrap"><i class="ti ti-eye"></i></div>
        <div class="mod-name">Vision AI</div>
        <div class="mod-desc">YOLOv8n real-time detection. Annotated frame stream to web panel</div>
      </div>
      <div class="mod-card mc-a">
        <div class="mod-id">MOD // SPEECH-AI</div>
        <div class="mod-icon-wrap"><i class="ti ti-microphone"></i></div>
        <div class="mod-name">Speech AI</div>
        <div class="mod-desc">Whisper STT + Coqui TTS. Wake word "Neura". Full command routing</div>
      </div>
      <div class="mod-card mc-k">
        <div class="mod-id">MOD // POWER-SYS</div>
        <div class="mod-icon-wrap"><i class="ti ti-bolt"></i></div>
        <div class="mod-name">Power System</div>
        <div class="mod-desc">Dual INA219 rail monitoring. SOC estimation. Low-voltage cutoff</div>
      </div>
      <div class="mod-card mc-b">
        <div class="mod-id">MOD // WEB-CTRL</div>
        <div class="mod-icon-wrap"><i class="ti ti-device-gamepad-2"></i></div>
        <div class="mod-name">Web Control</div>
        <div class="mod-desc">SocketIO panel. D-pad, gait actions, live camera, live telemetry</div>
      </div>
      <div class="mod-card mc-p">
        <div class="mod-id">MOD // PERIPH-BUS</div>
        <div class="mod-icon-wrap"><i class="ti ti-circuit-diode"></i></div>
        <div class="mod-name">Peripheral Bus</div>
        <div class="mod-desc">TFT display · I2S mic · MAX98357 amp · WS2812B NeoPixels</div>
      </div>
    </div>
  </div>

  <!-- 04 SYSTEM ARCHITECTURE -->
  <div class="section">
    <div class="sec-header">
      <span class="sec-num">04</span>
      <span class="sec-title">SYSTEM ARCHITECTURE</span>
      <div class="sec-line"></div>
    </div>
    <div class="arch-wrap">
      <div class="arch-layer">LAYER 2 &nbsp;·&nbsp; HIGH-LEVEL BRAIN &nbsp;·&nbsp; RASPBERRY PI / JETSON</div>
      <div class="arch-row">
        <div class="arch-cell"><div class="ac-tag">PROC-A</div><div class="ac-name">Vision AI</div><div class="ac-sub">YOLOv8 · Python · background thread</div></div>
        <div class="arch-cell"><div class="ac-tag">PROC-B</div><div class="ac-name">Speech AI</div><div class="ac-sub">Whisper STT · Coqui TTS · wake word</div></div>
        <div class="arch-cell"><div class="ac-tag">PROC-C</div><div class="ac-name">IK + Gait</div><div class="ac-sub">50 Hz · trot / walk / sit / shake</div></div>
        <div class="arch-cell"><div class="ac-tag">PROC-D</div><div class="ac-name">Web + Power</div><div class="ac-sub">Flask · SocketIO · INA219</div></div>
      </div>
      <div class="conn-row">
        <div class="conn-line"></div>
        <div class="conn-tag">UART 115200 baud</div>
        <div class="conn-line"></div>
        <div class="conn-tag">UART / I2C / SPI</div>
        <div class="conn-line"></div>
      </div>
      <div class="arch-layer g">LAYER 1 &nbsp;·&nbsp; MICROCONTROLLERS &nbsp;·&nbsp; DUAL ESP32</div>
      <div class="arch-row">
        <div class="arch-cell" style="flex:1.5"><div class="ac-tag g">ESP32-MOTION</div><div class="ac-name">Motion Controller</div><div class="ac-sub">12× servos · JSON UART · PlatformIO C++</div></div>
        <div class="arch-cell" style="flex:1.5"><div class="ac-tag g">ESP32-PERIPH</div><div class="ac-name">Peripheral Controller</div><div class="ac-sub">TFT · I2S mic · speaker · NeoPixel LEDs</div></div>
      </div>
      <div class="arch-layer a">LAYER 0 &nbsp;·&nbsp; HARDWARE</div>
      <div class="arch-row">
        <div class="arch-cell"><div class="ac-tag a">PWR</div><div class="ac-name">3S LiPo</div><div class="ac-sub">11.1V · 5000mAh · XT60</div></div>
        <div class="arch-cell"><div class="ac-tag a">ACT</div><div class="ac-name">12× Servos</div><div class="ac-sub">MG996R / DS3218 · 6V rail</div></div>
        <div class="arch-cell"><div class="ac-tag a">SENSE</div><div class="ac-name">Camera + Mic</div><div class="ac-sub">IMX477 · INMP441 I2S</div></div>
        <div class="arch-cell"><div class="ac-tag a">STRUC</div><div class="ac-name">3D Chassis</div><div class="ac-sub">PETG · PLA+ · TPU feet</div></div>
      </div>
    </div>
  </div>

  <!-- 05 MISSION ROADMAP -->
  <div class="section">
    <div class="sec-header">
      <span class="sec-num">05</span>
      <span class="sec-title">MISSION ROADMAP</span>
      <div class="sec-line"></div>
    </div>
    <div class="road-wrap">
      <div class="road-item"><div class="road-node done"></div><span class="road-label done-t">Mechanical design &amp; 3D printing</span><span class="road-tag-done">COMPLETE</span><span class="road-ver">v0.1</span></div>
      <div class="road-item"><div class="road-node done"></div><span class="road-label done-t">Basic servo control via ESP32</span><span class="road-tag-done">COMPLETE</span><span class="road-ver">v0.2</span></div>
      <div class="road-item"><div class="road-node done"></div><span class="road-label done-t">Inverse Kinematics engine</span><span class="road-tag-done">COMPLETE</span><span class="road-ver">v0.3</span></div>
      <div class="road-item"><div class="road-node done"></div><span class="road-label done-t">Web control interface</span><span class="road-tag-done">COMPLETE</span><span class="road-ver">v0.4</span></div>
      <div class="road-item"><div class="road-node done"></div><span class="road-label done-t">Vision AI — YOLOv8 integration</span><span class="road-tag-done">COMPLETE</span><span class="road-ver">v0.5</span></div>
      <div class="road-item"><div class="road-node done"></div><span class="road-label done-t">Speech AI — Whisper + Coqui</span><span class="road-tag-done">COMPLETE</span><span class="road-ver">v0.6</span></div>
      <div class="road-item"><div class="road-node done"></div><span class="road-label done-t">Power management system</span><span class="road-tag-done">COMPLETE</span><span class="road-ver">v0.7</span></div>
      <div class="road-item"><div class="road-node next"></div><span class="road-label">Autonomous navigation</span><span class="road-tag-next">NEXT</span><span class="road-ver active">v0.8</span></div>
      <div class="road-item"><div class="road-node next"></div><span class="road-label">SLAM mapping</span><span class="road-tag-next">PLANNED</span><span class="road-ver active">v0.9</span></div>
      <div class="road-item"><div class="road-node next"></div><span class="road-label">Emotion expression system</span><span class="road-tag-next">PLANNED</span><span class="road-ver active">v1.0</span></div>
      <div class="road-item"><div class="road-node next"></div><span class="road-label">ROS2 integration</span><span class="road-tag-next">PLANNED</span><span class="road-ver active">v1.1</span></div>
    </div>
  </div>

  <div class="footer">
    <span class="footer-brand">NEURABOT</span>
    <span class="footer-pulse"><span class="pulse-dot"></span>PRIVATE REPO &nbsp;·&nbsp; OPEN BUILD</span>
    <span>REV 2025.06</span>
  </div>

</div>

<script>
const dot = document.querySelector('.pulse-dot');
let v = true;
setInterval(() => { dot.style.opacity = v ? '0.3' : '1'; v = !v; }, 900);
</script>
