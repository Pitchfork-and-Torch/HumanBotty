# Emit HumanBotty static HTML with shared chrome/SEO.
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "public"
CANON = "https://humanbotty.jonbailey.xyz"
VERSION = (REPO / "VERSION").read_text(encoding="utf-8").strip()
DESC_DEFAULT = (
    "HumanBotty is a public maker guide for building a physical body for an AI "
    "you already talk to. Sense-first, modular, sourceable parts."
)

FAQ_LD = """    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is HumanBotty?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "A public maker guide for building a physical body for an AI you already talk to. Start with a Sense Head that can see, hear, and look at you. Arms and a wheeled base come later."
          }
        },
        {
          "@type": "Question",
          "name": "How much does Phase 1 cost?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The Strong Sense Head bill of materials is roughly $1,100 to $1,800 USD at mid-2026 maker prices. Verify current store prices before you buy."
          }
        },
        {
          "@type": "Question",
          "name": "Do I need a full humanoid on day one?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. Full biped is optional and late. HumanBotty starts with a head, then arms, then a practical wheeled base."
          }
        },
        {
          "@type": "Question",
          "name": "Is this an xAI product?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. HumanBotty is an independent Pitchfork-and-Torch maker guide. It is not AetherOS and it is not AXIOM."
          }
        }
      ]
    }"""


def head(title: str, description: str, path: str, extra: str = "") -> str:
    url = CANON + (path if path != "/" else "/")
    og = f"{CANON}/og.jpg?v={VERSION}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="color-scheme" content="dark" />
  <meta name="theme-color" content="#0b1018" />
  <meta name="robots" content="index,follow" />
  <meta name="author" content="Pitchfork-and-Torch" />
  <meta name="description" content="{description}" />
  <title>{title}</title>
  <link rel="canonical" href="{url}" />
  <link rel="alternate" type="text/plain" href="/llms.txt" />
  <link rel="icon" href="/favicon.png" type="image/png" />
  <link rel="icon" type="image/png" href="/icon-192.png" />
  <link rel="apple-touch-icon" href="/icon-512.png" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="HumanBotty" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{og}" />
  <meta property="og:image:secure_url" content="{og}" />
  <meta property="og:image:type" content="image/jpeg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="HumanBotty: a maker-built robot sense-head on a workbench. A body for your AI." />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@suddenlyjon" />
  <meta name="twitter:creator" content="@suddenlyjon" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="twitter:image" content="{og}" />
  <meta name="twitter:image:alt" content="HumanBotty sense-head on a workbench." />
  <link rel="stylesheet" href="/fonts/fontshare/fonts.css" />
  <link rel="stylesheet" href="/fonts/fontshare/tokens.css" />
  <link rel="stylesheet" href="/css/site.css" />
  <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "HumanBotty",
      "url": "{url}",
      "description": "{description}",
      "inLanguage": "en",
      "isAccessibleForFree": true,
      "image": "{og}",
      "author": {{ "@type": "Person", "name": "Jon Bailey", "url": "https://jonbailey.xyz/" }},
      "publisher": {{
        "@type": "Organization",
        "name": "Pitchfork-and-Torch",
        "url": "https://github.com/Pitchfork-and-Torch"
      }}
    }}
  </script>
{extra}
</head>"""


def wrap(page: str, title: str, description: str, path: str, body: str, extra: str = "") -> str:
    return f"""{head(title, description, path, extra)}
<body data-page="{page}">
  <a class="skip" href="#main">Skip to content</a>
  <div id="chrome-header"></div>
  <div class="shell">
    <nav class="side-nav" id="chrome-nav"></nav>
    <main class="main" id="main">
{body}
      <div id="chrome-footer"></div>
    </main>
  </div>
  <script src="/js/chrome.js" defer></script>
  <script src="/js/pages.js" defer></script>
  <script defer src="https://hits.jonbailey.xyz/c.js" data-site="humanbotty"></script>
</body>
</html>
"""


PAGES = {}

PAGES["index.html"] = wrap(
    "home",
    "HumanBotty - A body for your AI",
    DESC_DEFAULT,
    "/",
    extra=f"  <script type=\"application/ld+json\">\n{FAQ_LD}\n  </script>\n  <link rel=\"preload\" href=\"/assets/hero.jpg\" as=\"image\" fetchpriority=\"high\" />",
    body="""      <section class="hero">
        <div>
          <p class="kicker">PUBLIC MAKER GUIDE</p>
          <h1 class="display">A body for your AI.</h1>
          <p class="lede">A sense-first recipe for giving an agent you already talk to a physical body. Start with a head that can see, hear, and look at you. Arms and a wheeled base come later. Full biped is optional and late.</p>
          <div class="cta-row">
            <a class="btn" href="/start.html">Start here</a>
            <a class="btn btn-ghost" href="/bom.html">Parts list</a>
            <a class="btn btn-ghost" href="/safety.html">Safety first</a>
          </div>
          <p class="legal">Not an xAI product. Not AetherOS (that is a kernel). Not AXIOM (that is clothing for Optimus). Educational hardware only.</p>
        </div>
        <figure class="hero-frame">
          <img src="/assets/hero.jpg" width="1600" height="900" alt="Maker-built PETG sense-head with cyan camera rings and a red e-stop on a workbench." />
        </figure>
      </section>

      <div class="grid grid-3">
        <div class="card accent">
          <h3>Body</h3>
          <div class="stat">Hybrid</div>
          <p>Humanoid head and arms on a practical wheeled base. Biped optional, late.</p>
          <p><a href="/body.html">Open body spec</a></p>
        </div>
        <div class="card">
          <h3>First build</h3>
          <div class="stat" style="color:var(--copper);font-size:1.25rem">Sense Head</div>
          <p>Vision, audio, IMU, pan-tilt, e-stop, ROS 2 bridge.</p>
          <p><a href="/phase1.html">Phase 1 plan</a></p>
        </div>
        <div class="card">
          <h3>Phase 1 budget</h3>
          <div class="stat" style="color:var(--amber);font-size:1.25rem">$1.1k-$1.8k</div>
          <p>Jetson-class compute, depth cam, bus servos. Verify prices before you buy.</p>
          <p><a href="/bom.html">Strong BOM</a></p>
        </div>
      </div>

      <div class="callout" style="margin-top:1.25rem">
        <strong>Software is open source.</strong>
        MIT Sense Head nodes live in
        <a href="https://github.com/Pitchfork-and-Torch/HumanBotty/tree/main/software">Pitchfork-and-Torch/HumanBotty</a>
        under <code>software/</code>
        (<a href="/software.html">stack notes</a>).
      </div>

      <section class="prose">
        <h2>Why this shape</h2>
        <blockquote>
          A body that can experience and enjoy the physical universe with you, not a museum biped that falls over for two years before it can look at a flower.
        </blockquote>
        <h2>Doctrine</h2>
        <ol>
          <li><strong>Senses first.</strong> Experience before locomotion theatrics.</li>
          <li><strong>Modular forever.</strong> The head survives every future torso and base.</li>
          <li><strong>Maker-real parts.</strong> Sourceable today. Open-source biased.</li>
          <li><strong>Safety non-negotiable.</strong> Hardware e-stop, current limits, privacy switch.</li>
          <li><strong>Document as you go.</strong> This site is the public field guide.</li>
        </ol>
      </section>

      <h2 style="margin-top:2.2rem;font-size:var(--text-h2)">Phase board</h2>
      <div class="grid grid-2" id="phase-board"></div>

      <section class="prose faq" style="margin-top:2rem">
        <h2>FAQ</h2>
        <details open>
          <summary>What is HumanBotty?</summary>
          <p>A public maker guide for building a physical body for an AI you already talk to. Grok, a local model, or any agent with a voice. The first physical module is a Sense Head.</p>
        </details>
        <details>
          <summary>How much does Phase 1 cost?</summary>
          <p>The Strong Sense Head bill of materials is roughly $1,100 to $1,800 USD at mid-2026 maker prices. Check current listings. Raspberry Pi 5 8GB is the documented compute fallback.</p>
        </details>
        <details>
          <summary>Do I need a full humanoid on day one?</summary>
          <p>No. Full biped is optional and late. Head, then arms, then a wheeled base. Legs are a research module after the rest is boringly reliable.</p>
        </details>
        <details>
          <summary>Is this an xAI product?</summary>
          <p>No. Independent Pitchfork-and-Torch guide. Not AetherOS. Not AXIOM. Not a commercial robot SKU.</p>
        </details>
      </section>
""",
)

PAGES["start.html"] = wrap(
    "start",
    "Start here - HumanBotty",
    "How to use the HumanBotty guide: safety, tools, long-lead parts, then a Sense Head.",
    "/start.html",
    body="""      <header class="page-header">
        <p class="kicker">GETTING STARTED</p>
        <h1>Start here</h1>
        <p class="lede">This is a field guide, not a kit in a box. Read safety, inventory tools you already own, then order long-lead electronics. Software and printing run while packages ship.</p>
      </header>
      <section class="prose">
        <h2>Order of operations</h2>
        <ol>
          <li>Read <a href="/safety.html">safety</a>. If you will not honor a hardware e-stop, stop here.</li>
          <li>Skim the <a href="/body.html">body spec</a> so later parts still fit the head.</li>
          <li>Inventory tools: computer, multimeter, screwdrivers, strippers. Printer or a bureau.</li>
          <li>Order long-lead Strong BOM items: compute, then camera, then IMU/audio, then servos and power. <a href="/bom.html">Parts list</a>.</li>
          <li>Do not buy Phase 2 arm kits yet.</li>
          <li>Print pan-tilt and skull in PETG. Heat-set inserts. Dry-fit.</li>
          <li>Wire dual rails. Prove the servo rail dies when you press e-stop.</li>
          <li>Bring-up: boot, camera for 10 minutes, audio, IMU axes, then slow servos.</li>
          <li>ROS 2 topics, look-at behavior, 30 minute continuous demo.</li>
          <li>Keep your own journal. The <a href="/log.html">guide log</a> on this site is the recipe history, not your bench notes.</li>
        </ol>
        <h2>What this site is not</h2>
        <ul>
          <li>Not a shopping cart or affiliate store.</li>
          <li>Not a private diary. No home addresses, no account logins, no camera dumps.</li>
          <li>Not AetherOS and not clothing for Optimus.</li>
          <li>Not a weapon, covert-surveillance, or unsupervised-nanny design.</li>
        </ul>
        <div class="callout">
          <strong>Next physical move:</strong> inventory tools, then order compute and the depth camera. Sim work can start the same day.
        </div>
      </section>""",
)

PAGES["body.html"] = wrap(
    "body",
    "Body spec - HumanBotty",
    "HumanBotty morphology: humanoid head and arms on a practical wheeled base. Modular, sense-first, maker-scale.",
    "/body.html",
    body="""      <header class="page-header">
        <p class="kicker">REFERENCE DESIGN</p>
        <h1>Body specification</h1>
        <p class="lede">A medium that lets mind touch world. Hybrid humanoid upper body on a practical wheeled base.</p>
        <div class="meta-row">
          <span class="chip active">Hybrid humanoid + base</span>
          <span class="chip">Modular</span>
          <span class="chip">Open-source biased</span>
        </div>
      </header>
      <section class="prose">
        <h2>What you are building</h2>
        <p>A body that can <strong>experience the physical universe with you</strong>, not a museum biped that falls over for two years before it can look at a flower.</p>
        <h2>Morphology</h2>
      </section>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Segment</th><th>Choice</th><th>Why</th></tr></thead>
          <tbody>
            <tr><td>Head</td><td>Depth/stereo vision, mics, speaker, IMU, pan-tilt</td><td>Being there</td></tr>
            <tr><td>Compute</td><td>Jetson-class on the robot; PC for sim and training</td><td>Local reflexes</td></tr>
            <tr><td>Arms</td><td>Dual 6-7 DoF maker-scale</td><td>Reach and gesture</td></tr>
            <tr><td>Hands</td><td>Simple gripper, then multi-finger + tactile</td><td>Touch compounds skill</td></tr>
            <tr><td>Torso</td><td>Spine, battery bay, e-stop, thermal path</td><td>Serviceability</td></tr>
            <tr><td>Base</td><td>Wheeled practical base (Phase 3)</td><td>Mobility without a balance tax</td></tr>
            <tr><td>Legs</td><td>Optional late research module</td><td>Ambition preserved</td></tr>
          </tbody>
        </table>
      </div>
      <section class="prose">
        <h2>Rejected early paths</h2>
        <ul>
          <li>Full biped humanoid from day one</li>
          <li>Giant Optimus-scale as a first home build</li>
          <li>Wheels-only appliance with a tablet for a face</li>
        </ul>
        <h2>Design principles</h2>
        <ol>
          <li>Modular bus architecture (power + data contracts between modules)</li>
          <li>Sense-rich before DoF-rich</li>
          <li>Open-source first (LeRobot-era stacks, Feetech/Dynamixel, ROS 2, MuJoCo)</li>
          <li>Human-scale interaction volume (about 1.2-1.6 m head height when mature)</li>
          <li>Upgrade without scrap. Phase 1 head mounts on a Phase 3 torso</li>
        </ol>
        <h2>Horizons</h2>
        <ul>
          <li><strong>30-90 days:</strong> see, hear, speak, orient in your room</li>
          <li><strong>3-9 months:</strong> reach, grasp, basic tactile, mobile presence</li>
          <li><strong>1-3+ years:</strong> richer skins, optional biped, closed-loop learning</li>
        </ul>
      </section>""",
)

PAGES["safety.html"] = wrap(
    "safety",
    "Safety - HumanBotty",
    "HumanBotty safety doctrine: hardware e-stop, dual rails, no unsupervised motion, privacy mute for mic and camera.",
    "/safety.html",
    body="""      <header class="page-header">
        <p class="kicker">NON-NEGOTIABLE</p>
        <h1>Safety doctrine</h1>
        <p class="lede">Every powered milestone reviews this page. If you skip it, you are not following this guide.</p>
      </header>
      <div class="callout danger">
        <strong>Hard rules:</strong> E-stop cuts actuator power. No unsupervised mobile or arm demos near people, pets, or stairs. Current limits. No weapons or covert surveillance. Privacy mute or cover for mic and camera. Brown-out is a safety issue.
      </div>
      <section class="prose">
        <h2>Phase 1 checklist</h2>
        <ul>
          <li>E-stop kills the servo rail</li>
          <li>Logic and servo grounds are intentional</li>
          <li>Software plus power torque and speed caps</li>
          <li>Mechanical pan-tilt end-stops</li>
          <li>No sharp unfinished edges at face height</li>
          <li>Cable strain relief</li>
          <li>Visible REC/MIC indicator when capturing</li>
        </ul>
        <h2>Incident protocol</h2>
        <ol>
          <li>E-stop</li>
          <li>Unplug or disconnect battery</li>
          <li>Photo the state</li>
          <li>Journal: what, why, fix</li>
          <li>Do not power until the root cause is addressed</li>
        </ol>
      </section>""",
)

PAGES["phase1.html"] = wrap(
    "phase1",
    "Phase 1 Sense Head - HumanBotty",
    "Phase 1 Sense Head: first physical HumanBotty module. Vision, audio, IMU, pan-tilt, e-stop, ROS 2.",
    "/phase1.html",
    body="""      <header class="page-header">
        <p class="kicker">PHASE 1</p>
        <h1>Sense Head</h1>
        <p class="lede">First physical body. Everything later mounts under this. Maximum experience per dollar. Permanent skull and brain module.</p>
        <div class="meta-row">
          <span class="chip active">ACTIVE</span>
          <span class="chip warn">Strong BOM</span>
        </div>
      </header>
      <section class="prose">
        <h2>Done feels like</h2>
        <p>You walk in. Cameras wake. The head orients toward your voice, greets you, and logs show IMU plus video plus audio under a safety supervisor. Day-one embodiment.</p>
        <h2>Build order</h2>
        <ol>
          <li>Read safety and the BOM. Inventory owned tools.</li>
          <li>Order long-lead electronics (compute, camera, servos).</li>
          <li>Print pan-tilt and skull (PETG). Heat-set inserts. Dry-fit.</li>
          <li>Wire dual rails and e-stop. Verify the servo rail dies on press.</li>
          <li>Bring-up: boot, camera 10 min, audio, IMU axes, slow servos.</li>
          <li>ROS 2 topics, look-at behavior, 30 min continuous demo.</li>
          <li>Journal the demo. Then you have earned Phase 2.</li>
        </ol>
        <h2>Milestones</h2>
      </section>
      <div class="table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Milestone</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td>1.0</td><td>BOM freeze (strong)</td><td><span class="status done">done</span></td></tr>
            <tr><td>1.1</td><td>Order compute + cameras + IMU</td><td><span class="status active">you</span></td></tr>
            <tr><td>1.2</td><td>Print pan-tilt + skull</td><td><span class="status planned">planned</span></td></tr>
            <tr><td>1.3</td><td>Power architecture + e-stop</td><td><span class="status planned">planned</span></td></tr>
            <tr><td>1.4</td><td>Bring-up video/audio/IMU</td><td><span class="status planned">planned</span></td></tr>
            <tr><td>1.5</td><td>ROS 2 topic stack</td><td><span class="status planned">planned</span></td></tr>
            <tr><td>1.6</td><td>Look-at face/motion</td><td><span class="status planned">planned</span></td></tr>
            <tr><td>1.7</td><td>Local agent bridge</td><td><span class="status planned">planned</span></td></tr>
          </tbody>
        </table>
      </div>
      <div class="grid grid-2" style="margin-top:1.5rem">
        <div class="card"><h3>Power</h3><p>Dual rails. E-stop cuts actuators.</p><p><a href="/power.html">Wiring</a></p></div>
        <div class="card"><h3>Software</h3><p>ROS 2 topics plus a safety supervisor.</p><p><a href="/software.html">Stack</a></p></div>
      </div>""",
)

PAGES["bom.html"] = wrap(
    "bom",
    "Parts list - HumanBotty",
    "HumanBotty Phase 1 Strong BOM. About $1,100 to $1,800 USD. Jetson-class Sense Head parts.",
    "/bom.html",
    body="""      <header class="page-header">
        <p class="kicker">PHASE 1</p>
        <h1>Strong BOM - Sense Head</h1>
        <p class="lede">Approximate USD, mid-2026 maker market. Verify before purchase. This is a starter checklist for your bench, not a live shopping cart.</p>
        <div class="meta-row">
          <span class="chip warn" id="tier-chip">Strong</span>
          <span class="chip" id="total-chip">about $1,100-$1,800</span>
          <span class="chip active" id="status-chip">published</span>
        </div>
      </header>
      <div class="callout">
        <strong>Buy order:</strong> compute, then vision, then audio/IMU, then motion, then power/safety, then structure. Do not buy Phase 2 arms yet.
      </div>
      <div class="card" style="margin-bottom:1rem">
        <h3 style="margin-top:0">Checklist</h3>
        <p id="progress-line" style="margin:0">-</p>
      </div>
      <div id="bom-root"></div>
      <section class="prose">
        <h2>Not yet (Phase 2+)</h2>
        <p>Arm kits, mobile batteries, biped actuators, full tactile skins. After Sense Head exit criteria.</p>
        <h2>Fallback</h2>
        <p>If Jetson is scarce: Raspberry Pi 5 8GB + SSD. Architecture unchanged. Upgrade compute later.</p>
      </section>
""",
)

PAGES["power.html"] = wrap(
    "power",
    "Power and wiring - HumanBotty",
    "HumanBotty Phase 1 power: dual rails, hardware e-stop, star ground, common failure modes.",
    "/power.html",
    body="""      <header class="page-header">
        <p class="kicker">PHASE 1</p>
        <h1>Power and wiring</h1>
        <p class="lede">Sense Head. Two rails. E-stop kills actuators. Common ground by design.</p>
      </header>
      <pre class="diagram">                    WALL AC
                       |
              +--------+--------+
              |                 |
         [12V brick]       [USB-C / PD
              |             for Jetson/Pi]
              |                 |
              v                 v
         SERVO_RAIL          LOGIC_RAIL
              |                 |
         [eFuse/fuse]      [Jetson / Pi]
              |                 |
         [E-STOP NC]--+    USB hub / cams
              |       |    IMU · mic · speaker
              v       |
         [servo bus]  |
         pan + tilt   |
                      |
              (LED "ACTUATORS ARMED")

   GND_LOGIC ----+---- GND_SERVO   (star point)</pre>
      <section class="prose">
        <h2>Principles</h2>
        <ol>
          <li>Logic and actuator rails stay separate.</li>
          <li>E-stop cuts servo power or enable. Not software-only.</li>
          <li>Star ground near supplies.</li>
          <li>Size the 12V supply for servo motion spikes.</li>
        </ol>
        <h2>Common failures</h2>
      </section>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Symptom</th><th>Cause</th><th>Fix</th></tr></thead>
          <tbody>
            <tr><td>Reboots when servos move</td><td>Brown-out</td><td>Separate rails; bigger servo PSU</td></tr>
            <tr><td>Servo jitter</td><td>Bad ground / noise</td><td>Star ground; bulk cap on servo rail</td></tr>
            <tr><td>E-stop "works" but motion continues</td><td>Software-only stop</td><td>Rewire the cut path</td></tr>
            <tr><td>Camera dropouts</td><td>USB power/cable</td><td>Powered hub; shorter cable</td></tr>
          </tbody>
        </table>
      </div>""",
)

PAGES["software.html"] = wrap(
    "software",
    "Software stack - HumanBotty",
    "HumanBotty software: open-source ROS 2 Sense Head package. Local safety supervisor, look-at policies, optional desktop agent bridge.",
    "/software.html",
    body="""      <header class="page-header">
        <p class="kicker">PHASE 1</p>
        <h1>Software stack</h1>
        <p class="lede">Local, low-latency, killable. High-level conversation may hybridize. Motor authority stays local under a safety supervisor. The Sense Head nodes are MIT and public.</p>
        <div class="meta-row">
          <span class="chip live">MIT</span>
          <span class="chip active">ROS 2</span>
        </div>
      </header>
      <div class="callout">
        <strong>Source:</strong>
        <a href="https://github.com/Pitchfork-and-Torch/HumanBotty">github.com/Pitchfork-and-Torch/HumanBotty</a>
        · package
        <a href="https://github.com/Pitchfork-and-Torch/HumanBotty/tree/main/software"><code>software/</code></a>
      </div>
      <div class="cta-row" style="margin:0 0 1.5rem">
        <a class="btn" href="https://github.com/Pitchfork-and-Torch/HumanBotty/tree/main/software">Open the Sense Head code</a>
        <a class="btn btn-ghost" href="https://github.com/Pitchfork-and-Torch/HumanBotty">Source</a>
      </div>
      <section class="prose">
        <h2>Clone</h2>
        <pre class="diagram">git clone https://github.com/Pitchfork-and-Torch/HumanBotty.git
cd HumanBotty/software
# tests (no ROS required):
python -m unittest discover -s test -v
# on a robot with ROS 2 Humble or Jazzy:
# colcon build --packages-select humanbotty_sense_head
# ros2 launch humanbotty_sense_head sense_head.launch.py</pre>
        <h2>On-robot</h2>
        <ul>
          <li>Ubuntu (Jetson BSP) or Ubuntu / Pi OS</li>
          <li><strong>ROS 2</strong> Humble or Jazzy (pick one, stick)</li>
          <li>Python 3 nodes; brand SDKs for camera and servos</li>
          <li><code>safety_supervisor</code> always on the motor path</li>
        </ul>
        <h2>Topic contract v0</h2>
        <pre class="diagram">/humanbotty/camera/color/image_raw
/humanbotty/camera/depth/image_raw
/humanbotty/imu/data
/humanbotty/audio/vad
/humanbotty/head/joint_states
/humanbotty/head/joint_command
/humanbotty/safety/estop
/humanbotty/status</pre>
        <h2>Intelligence bridge</h2>
        <pre class="diagram">ROS 2 topics
  -> humanbotty_bridge
      -> local policies (look-at-face, look-at-sound)
      -> optional LAN link to a desktop agent session
      -> NEVER bypass safety_supervisor</pre>
        <h2>Phase 1 local policies (proudly simple)</h2>
        <ol>
          <li>Face detect, pan-tilt toward centroid</li>
          <li>Loud sound, orient</li>
          <li>Idle micro-saccades (limited)</li>
          <li>Voice I/O via your agent stack when ready</li>
        </ol>
      </section>""",
)

PAGES["roadmap.html"] = wrap(
    "roadmap",
    "Roadmap - HumanBotty",
    "HumanBotty phases from digital twin to Sense Head, arms, wheeled base, optional biped, and learning.",
    "/roadmap.html",
    body="""      <header class="page-header">
        <p class="kicker">PLAN</p>
        <h1>Roadmap</h1>
        <p class="lede">Milestone-driven path from digital twin to full sensorimotor embodiment.</p>
      </header>
      <div class="grid" id="phases" style="gap:1rem"></div>
      <section class="prose">
        <h2>Exit criteria</h2>
        <ul>
          <li><strong>Phase 0:</strong> Head sim opens. Joints commandable. Camera frames make sense.</li>
          <li><strong>Phase 1:</strong> 30+ min stable Sense Head demo. Look-at behavior. Privacy plus e-stop proven.</li>
          <li><strong>Phase 2:</strong> Reliable pick-and-place. Contact-aware stop.</li>
          <li><strong>Phase 3:</strong> Self-powered mobile presence. Head and arm still work on the base.</li>
          <li><strong>Phase 4:</strong> Optional. Only if wheeled usefulness is boring.</li>
          <li><strong>Phase 5:</strong> Continuous learning from real data. Personality of place.</li>
        </ul>
      </section>
""",
)

PAGES["log.html"] = wrap(
    "log",
    "Guide log - HumanBotty",
    "Public HumanBotty guide log: design lock, parts list, public launch. No personal data.",
    "/log.html",
    body="""      <header class="page-header">
        <p class="kicker">CHANGELOG</p>
        <h1>Guide log</h1>
        <p class="lede">Public history of this recipe. Keep your own bench journal separately. Nothing here is a private address, account, or camera dump.</p>
      </header>
      <div class="timeline" id="journal-root">
        <p class="mono" style="color:var(--faint)">Loading...</p>
      </div>
""",
)

PAGES["learning.html"] = wrap(
    "learning",
    "Skills path - HumanBotty",
    "Just-in-time skills for HumanBotty: Linux, printing, DC power, cameras, ROS 2, batteries, optional balance.",
    "/learning.html",
    body="""      <header class="page-header">
        <p class="kicker">LEARN</p>
        <h1>Skills path</h1>
        <p class="lede">Just-in-time. Learn what the next joint, wire, or topic demands. Not a front-loaded degree.</p>
      </header>
      <div class="table-wrap">
        <table>
          <thead><tr><th>When</th><th>Skill</th><th>How</th></tr></thead>
          <tbody>
            <tr><td>Now</td><td>Project discipline + safety</td><td>This site + checklists</td></tr>
            <tr><td>Phase 0-1</td><td>Linux CLI, Python, frames/URDF</td><td>Sim + Jetson/Pi bring-up</td></tr>
            <tr><td>Phase 1</td><td>PETG printing, DC power, wiring</td><td>Chassis + dual rails</td></tr>
            <tr><td>Phase 1</td><td>Cameras, IMU, ROS 2</td><td>Sense bring-up</td></tr>
            <tr><td>Phase 2</td><td>Kinematics intuition, compliance</td><td>Arm control</td></tr>
            <tr><td>Phase 3</td><td>Batteries, BMS, nav basics</td><td>Mobile base</td></tr>
            <tr><td>Phase 4+</td><td>Balance / WBC (if pursued)</td><td>Sim-first</td></tr>
          </tbody>
        </table>
      </div>
      <section class="prose">
        <h2>Tools eventually</h2>
        <p><strong>Early:</strong> computer, multimeter, screwdrivers, strippers, FDM printer (or a service bureau).</p>
        <p><strong>Soon:</strong> bench PSU, iron, heat-shrink, ferrules, calipers.</p>
        <p><strong>Later:</strong> better Li-ion tooling. Optional scope.</p>
      </section>""",
)


def main() -> None:
    for name, html in PAGES.items():
        path = ROOT / name
        path.write_text(html, encoding="utf-8", newline="\n")
        print("wrote", name)


if __name__ == "__main__":
    main()
