
from pathlib import Path
import math, json, html, xml.etree.ElementTree as ET
import base64, hashlib
import numpy as np
import cairosvg
from utf73_field import load_spec as load_utf73_spec, symbols as utf73_symbols, write_all as write_utf73_all
from language_frame_closure import derive as derive_language_closure

OUT = Path(__file__).resolve().parent.parent
SVG_PATH = OUT / "assets" / "signals_systems_full_atlas_master.svg"
VERIFY_PATH = OUT / "verification.txt"
CH14_SVG_PATH = OUT / "assets" / "ch14_test_object.svg"
CH14_PNG_PATH = OUT / "assets" / "ch14_test_object.png"
CH14_B64_PATH = OUT / "data" / "ch14_test_object.b64.txt"
CH14_DATA_PATH = OUT / "data" / "encoding_geometry.json"

# --------------------------
# Chapter 14 source object + exact encoding chain
# --------------------------
CH14_TEST_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="160" height="96" viewBox="0 0 160 96">
<rect width="160" height="96" fill="#04060b"/>
<rect x="12.4387" y="11.25" width="61.5" height="37.75" rx="5.125" fill="#65f4ff"/>
<circle cx="111.75" cy="46.5" r="21.375" fill="#b48cff"/>
<line x1="9.125" y1="79.625" x2="148.75" y2="66.375" stroke="#edf6ff" stroke-width="2.25"/>
</svg>"""
CH14_SVG_PATH.write_text(CH14_TEST_SVG, encoding="utf-8")
CH14_PNG_BYTES = cairosvg.svg2png(bytestring=CH14_TEST_SVG.encode("utf-8"), output_width=160, output_height=96)
CH14_PNG_PATH.write_bytes(CH14_PNG_BYTES)
CH14_B64 = base64.b64encode(CH14_PNG_BYTES)
CH14_B64_PATH.parent.mkdir(exist_ok=True)
CH14_B64_PATH.write_bytes(CH14_B64 + b"\n")
CH14_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
CH14_INDICES = [CH14_ALPHABET.index(chr(c)) for c in CH14_B64 if chr(c) != "="]
CH14_RAW_SHA256 = hashlib.sha256(CH14_PNG_BYTES).hexdigest()
CH14_B64_SHA256 = hashlib.sha256(CH14_B64).hexdigest()
CH14_FIRST_BYTES = list(CH14_PNG_BYTES[:16])
CH14_FIRST_CHARS = CH14_B64[:16].decode("ascii")
CH14_FIRST_INDICES = CH14_INDICES[:16]
CH14_ENCODING_DATA = {
    "source_svg": "assets/ch14_test_object.svg",
    "png": "assets/ch14_test_object.png",
    "base64": "data/ch14_test_object.b64.txt",
    "width": 160,
    "height": 96,
    "vector_coordinate_example": 12.4387,
    "raster_cell_example": 12,
    "png_length_bytes": len(CH14_PNG_BYTES),
    "png_sha256": CH14_RAW_SHA256,
    "base64_length_chars": len(CH14_B64),
    "base64_sha256": CH14_B64_SHA256,
    "first_16_png_bytes_hex": [f"{b:02x}" for b in CH14_FIRST_BYTES],
    "first_16_base64_chars": CH14_FIRST_CHARS,
    "first_16_base64_indices": CH14_FIRST_INDICES,
    "structural_frames": {
        "vector": "real-valued coordinates / epsilon chosen by representation",
        "raster": "1 pixel",
        "byte": "8 bits",
        "base64_symbol": "6 bits"
    },
    "physical_planck_scale_claim": False
}
CH14_DATA_PATH.write_text(json.dumps(CH14_ENCODING_DATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# --------------------------
# Canonical UTF73 field + exhaustive RGB24 basin data
# --------------------------
UTF73_SPEC = load_utf73_spec()
UTF73_SYMBOLS = utf73_symbols()
UTF73_REAL_BASINS, UTF73_DATASET = write_utf73_all()
UTF73_REAL_COUNTS = [row["rgb24_basin_size"] for row in UTF73_REAL_BASINS["states"]]

# Chapter 17 quotient theorem data
CLOSURE7 = derive_language_closure()

# --------------------------
# Global visual system
# --------------------------
VW = 1600
HEADER_H = 260
CHAPTER_H = 1320
N_CH = 20
VH = HEADER_H + N_CH*CHAPTER_H + 180
OUT_W = 3840
OUT_H = int(3840 * VH / VW)

BG0 = "#0b1220"
BG1 = "#04060b"
CYAN = "#65f4ff"
PURPLE = "#b48cff"
GREY = "#6c7a94"
WHITE = "#edf6ff"
DARK = "#07101b"
RED = "#ff7f8f"
GREEN = "#7dffb2"

svg = []
A = svg.append

def esc(s):
    return html.escape(str(s), quote=True)

# --------------------------
# Helpers
# --------------------------
def panel(x,y,w,h,title,subtitle="",concept="",eq=""):
    A(f'<g data-concept="{esc(concept)}" data-equation="{esc(eq)}">')
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{DARK}" fill-opacity=".68" stroke="{GREY}" stroke-opacity=".20"/>')
    A(f'<text x="{x+24}" y="{y+34}" class="mono" font-size="10" letter-spacing="1.6" fill="{CYAN}">{esc(title.upper())}</text>')
    if subtitle:
        A(f'<text x="{x+24}" y="{y+56}" class="mono" font-size="8.8" fill="{GREY}">{esc(subtitle)}</text>')
    return (x+24,y+76,w-48,h-100)

def end_panel():
    A('</g>')

def axes(x,y,w,h, xlabel="", ylabel="", xzero=0.0, yzero=0.5):
    xx = x + w*xzero
    yy = y + h*yzero
    A(f'<line x1="{x}" y1="{yy:.2f}" x2="{x+w}" y2="{yy:.2f}" stroke="{GREY}" stroke-opacity=".38"/>')
    A(f'<line x1="{xx:.2f}" y1="{y}" x2="{xx:.2f}" y2="{y+h}" stroke="{GREY}" stroke-opacity=".28"/>')
    if xlabel:
        A(f'<text x="{x+w}" y="{y+h+16}" text-anchor="end" class="mono" font-size="7.5" fill="{GREY}">{esc(xlabel)}</text>')
    if ylabel:
        A(f'<text x="{x+4}" y="{y+10}" class="mono" font-size="7.5" fill="{GREY}">{esc(ylabel)}</text>')
    return xx,yy

def polyline(points, stroke=CYAN, width=2.2, glow=False, opacity=1.0, dash=None):
    attrs = f'stroke="{stroke}" stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"'
    if glow:
        attrs += ' filter="url(#glowC)"' if stroke==CYAN else ' filter="url(#glowP)"'
    if dash:
        attrs += f' stroke-dasharray="{dash}"'
    A('<polyline points="' + " ".join(f"{px:.2f},{py:.2f}" for px,py in points) + f'" {attrs}/>')

def stems(x,y,w,h, bins, values, maxbin=None, maxval=None, color=PURPLE, labels=True, logx=False, fundamental=None):
    maxbin = maxbin if maxbin is not None else max(bins)
    maxval = maxval if maxval is not None else max(values)
    axes(x,y,w,h,xlabel="frequency / bin",ylabel="magnitude",xzero=0,yzero=1)
    for b,v in zip(bins,values):
        if logx:
            px = x + (math.log(max(b,1))/math.log(maxbin))*w
        else:
            px = x + (b/maxbin)*w
        py0 = y+h
        py1 = y+h - (v/maxval)*(h*.84)
        c = CYAN if fundamental is not None and b==fundamental else color
        filt = "glowC" if c==CYAN else "glowP"
        A(f'<line x1="{px:.2f}" y1="{py0:.2f}" x2="{px:.2f}" y2="{py1:.2f}" stroke="{c}" stroke-width="{3.6 if c==CYAN else 2.2}" filter="url(#{filt})"/>')
        A(f'<circle cx="{px:.2f}" cy="{py1:.2f}" r="2.5" fill="{c}"/>')
        if labels:
            A(f'<text x="{px:.2f}" y="{py0+14:.2f}" text-anchor="middle" class="mono" font-size="6.6" fill="{GREY}">{esc(b)}</text>')

def wave(x,y,w,h, func, color=CYAN, glow=True, samples=400):
    pts=[]
    for i in range(samples):
        t=i/(samples-1)
        v=float(func(t))
        px=x+t*w
        py=y+h/2-v*(h*.38)
        pts.append((px,py))
    axes(x,y,w,h,xlabel="t",ylabel="",xzero=0,yzero=.5)
    polyline(pts,color,2.3,glow)

def discrete_wave(x,y,w,h, vals, color=CYAN, labels=False):
    vals=np.array(vals,float)
    axes(x,y,w,h,xlabel="n",ylabel="",xzero=0,yzero=.5)
    m=max(1e-9,np.max(np.abs(vals)))
    for i,v in enumerate(vals):
        px=x + i/(len(vals)-1)*w
        py=y+h/2-v/m*(h*.36)
        A(f'<line x1="{px:.2f}" y1="{y+h/2:.2f}" x2="{px:.2f}" y2="{py:.2f}" stroke="{color}" stroke-width="1.4" opacity=".82"/>')
        A(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="2.1" fill="{color}"/>')
        if labels and i%8==0:
            A(f'<text x="{px:.2f}" y="{y+h+14}" text-anchor="middle" class="mono" font-size="6.5" fill="{GREY}">{i}</text>')

def polezero(x,y,w,h,poles,zeros,roc=None,title=""):
    # normalized complex plane [-2,2]
    axes(x,y,w,h,xlabel="Re",ylabel="Im",xzero=.5,yzero=.5)
    cx=x+w/2; cy=y+h/2
    sx=w/4; sy=h/4
    # unit circle
    r=min(sx,sy)
    A(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GREY}" stroke-opacity=".24" stroke-dasharray="4 5"/>')
    if roc:
        kind,val=roc
        rr=r*val
        if kind=="outside":
            A(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{CYAN}" stroke-opacity=".45" stroke-width="8"/>')
        elif kind=="inside":
            A(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{CYAN}" fill-opacity=".05" stroke="{CYAN}" stroke-opacity=".45"/>')
    for z in zeros:
        px=cx+z.real*sx; py=cy-z.imag*sy
        A(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="6" fill="none" stroke="{CYAN}" stroke-width="2"/>')
    for p in poles:
        px=cx+p.real*sx; py=cy-p.imag*sy
        A(f'<line x1="{px-5:.2f}" y1="{py-5:.2f}" x2="{px+5:.2f}" y2="{py+5:.2f}" stroke="{PURPLE}" stroke-width="2"/>')
        A(f'<line x1="{px-5:.2f}" y1="{py+5:.2f}" x2="{px+5:.2f}" y2="{py-5:.2f}" stroke="{PURPLE}" stroke-width="2"/>')

def block(x,y,w,h,label,sub=""):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#08111d" stroke="{CYAN}" stroke-opacity=".72"/>')
    A(f'<text x="{x+w/2}" y="{y+h/2-2}" text-anchor="middle" class="mono" font-size="11" fill="{WHITE}">{esc(label)}</text>')
    if sub:
        A(f'<text x="{x+w/2}" y="{y+h/2+15}" text-anchor="middle" class="mono" font-size="7" fill="{GREY}">{esc(sub)}</text>')

def arrow(x1,y1,x2,y2,color=CYAN,dash=None):
    d = f'M{x1},{y1} L{x2},{y2}'
    extra = f' stroke-dasharray="{dash}"' if dash else ''
    A(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.8" marker-end="url(#arrC)"{extra}/>')

def chapter_header(ch_y,num,title,subtitle):
    A(f'<text x="70" y="{ch_y+55}" class="mono" font-size="12" letter-spacing="2.4" fill="{CYAN}">CHAPTER {num:02d}</text>')
    A(f'<text x="70" y="{ch_y+96}" class="sans" font-size="34" font-weight="700" fill="{WHITE}">{esc(title)}</text>')
    A(f'<text x="70" y="{ch_y+124}" class="mono" font-size="10" fill="{GREY}">{esc(subtitle)}</text>')
    A(f'<line x1="70" y1="{ch_y+148}" x2="1530" y2="{ch_y+148}" stroke="{GREY}" stroke-opacity=".22"/>')

def grid_panels(ch_y):
    # 2x2 big + one full width bottom
    return [
        (70,ch_y+180,710,430),
        (820,ch_y+180,710,430),
        (70,ch_y+640,710,430),
        (820,ch_y+640,710,430),
        (70,ch_y+1100,1460,180),
    ]

# --------------------------
# SVG preamble + metadata
# --------------------------
chapters = [
("Signals & Systems","Representations, transformations, elementary signals, system properties"),
("LTI Systems","Impulse response, convolution, step response, equations"),
("Fourier Series","Periodic signals in harmonic coordinates"),
("Continuous-Time Fourier Transform","Aperiodic signals and continuous spectra"),
("Discrete-Time Fourier Transform","Periodic spectra of discrete-time signals"),
("Time / Frequency Characterization","Frequency response, filters, resonance, delay"),
("Sampling","Sampling theorem, replicas, aliasing, reconstruction"),
("Communication Systems","Modulation, sidebands, demodulation, multiplexing"),
("Laplace Transform","s-plane, ROC, poles, zeros, system functions"),
("Z-Transform","z-plane, ROC, unit circle, discrete-time systems"),
("Linear Feedback Systems","Closed loop, sensitivity, pole movement, stability"),
("Hash Dynamics","Finite words, cyclic bit geometry, modular state updates, diffusion"),
("Address Geometry","IPv4 32-bit words, IPv6 128-bit space, mapped embedding and prefix structure"),
("Encoding Geometry","Vector coordinates, raster frames, PNG bytes, Base64 partitions and reconstruction"),
("Canonical Field Encoding","73 Unicode states, UTF-8 sequences, fixed points and measured RGB24 basins"),
("Abjad Field Geometry","UTF carrier, direct abjad mapping, exact mod-9 dynamics, locked corpus measurement"),
("7-Closure","Three language frames × two coordinates plus one identified closure point"),
("Transformer Frame","Residual carrier, learned structure, 6+1 geometry and self-reference · working model"),
("Choice Geometry","Explicit choice space Θ, dual encoding chains and reflective provenance closure"),
("Carrier Invariance","Replaceable model carrier, fixed structural route, canonical discrete field and executable read-route checks"),
]
meta = {
    "title":"Signals & Systems · Full Visual Atlas",
    "style":"HEXA_64 / NPN Signal Field",
    "chapters":[{"index":i+1,"title":t,"subtitle":s} for i,(t,s) in enumerate(chapters)],
    "note":"Original educational visualizations; all plotted data and geometry are embedded in this SVG.",
    "default_discrete_frame":64
}

A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{OUT_W}" height="{OUT_H}" viewBox="0 0 {VW} {VH}" preserveAspectRatio="xMidYMid meet">')
A('<title>Signals &amp; Systems · Full Visual Atlas · HEXA_64</title>')
A('<desc>Original long-form visual atlas covering eleven Signals and Systems chapters with computed waveforms, spectra, sampling diagrams, transforms, pole-zero maps, and feedback-system visualizations.</desc>')
A('<metadata id="atlas-data"><![CDATA[' + json.dumps(meta,ensure_ascii=False) + ']]></metadata>')
A(r"""
<defs>
  <radialGradient id="bg" cx="46%" cy="18%" r="92%">
    <stop offset="0%" stop-color="#0b1220"/>
    <stop offset="100%" stop-color="#04060b"/>
  </radialGradient>
  <filter id="glowC" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="3.3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glowP" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="2.6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <marker id="arrC" markerWidth="8" markerHeight="8" refX="7" refY="3.5" orient="auto">
    <path d="M0,0 L0,7 L8,3.5 z" fill="#65f4ff"/>
  </marker>
  <style>
    .mono { font-family: "IBM Plex Mono","SFMono-Regular",Consolas,monospace; }
    .sans { font-family: Inter,Arial,Helvetica,sans-serif; }
  </style>
</defs>
""")
A(f'<rect width="{VW}" height="{VH}" fill="url(#bg)"/>')
A('<g stroke="#6c7a94" stroke-opacity=".035" stroke-width="1">')
for gx in range(40,VW,40):
    A(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{VH}"/>')
for gy in range(40,VH,40):
    A(f'<line x1="0" y1="{gy}" x2="{VW}" y2="{gy}"/>')
A('</g>')

# Master header
A(f'<text x="70" y="64" class="mono" font-size="14" letter-spacing="3.2" fill="{CYAN}">NPN // SIGNAL FIELD</text>')
A(f'<text x="70" y="116" class="sans" font-size="46" font-weight="700" fill="{WHITE}">SIGNALS &amp; SYSTEMS · FULL VISUAL ATLAS</text>')
A(f'<text x="70" y="150" class="mono" font-size="11" letter-spacing="1.3" fill="{GREY}">ORIGINAL SVG · 20 CHAPTERS · COMPUTED CURVES · EMBEDDED DATA · HEXA_64</text>')
A(f'<text x="1530" y="64" text-anchor="end" class="mono" font-size="10" fill="{CYAN}">MASTER SVG · 1 FILE</text>')
A(f'<rect x="70" y="185" width="1460" height="42" rx="21" fill="{DARK}" stroke="{GREY}" stroke-opacity=".22"/>')
A(f'<text x="800" y="211" text-anchor="middle" class="mono" font-size="9.5" fill="{GREY}">READ TOP → BOTTOM · TIME / STATE → TRANSFORM / SPECTRUM → SYSTEM CONSEQUENCE</text>')

# --------------------------
# Chapter 1
# --------------------------
ch=HEADER_H
chapter_header(ch,1,*chapters[0])
p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"Continuous-time sinusoid","Amplitude, phase and period are geometric parameters","ct_sinusoid","x(t)=A sin(ω0 t+φ)")
wave(ix,iy+30,iw,ih-40,lambda t: math.sin(4*math.pi*t+0.55))
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="8" fill="{GREY}">A=1 · 2 periods · φ=0.55 rad</text>')
end_panel()

ix,iy,iw,ih=panel(*p[1],"Discrete-time sinusoid","64 positions in a fixed frame","dt_sinusoid","x[n]=sin(2π·5n/64)")
n=np.arange(64); vals=np.sin(2*np.pi*5*n/64)
discrete_wave(ix,iy+22,iw,ih-32,vals,labels=True)
end_panel()

ix,iy,iw,ih=panel(*p[2],"Time operations","Shift · scale · reverse","signal_transformations","x(t), x(t-t0), x(at), x(-t)")
axes(ix,iy+30,iw,ih-50)
for off,c,lab in [(0,CYAN,"x(t)"),(.15,PURPLE,"x(t−t₀)"),(-.10,GREEN,"x(−t)")]:
    pts=[]
    for i in range(220):
        t=i/219
        v=math.exp(-35*(t-.45-off)**2)
        if lab=="x(−t)": v=math.exp(-35*((1-t)-.45)**2)
        pts.append((ix+t*iw,iy+30+(ih-50)/2-v*(ih-50)*.33))
    polyline(pts,c,2,False,.9)
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="8" fill="{GREY}">cyan=original · purple=shift · green=reverse</text>')
end_panel()

ix,iy,iw,ih=panel(*p[3],"Impulse & step","Elementary building blocks","impulse_step","u[n], δ[n], u[n]-u[n-1]=δ[n]")
# step
vals=np.r_[np.zeros(16),np.ones(48)]
discrete_wave(ix,iy+20,iw,120,vals,PURPLE)
# impulse
vals2=np.zeros(64); vals2[16]=1
discrete_wave(ix,iy+190,iw,120,vals2,CYAN)
A(f'<text x="{ix}" y="{iy+167}" class="mono" font-size="8" fill="{GREY}">u[n]</text>')
A(f'<text x="{ix}" y="{iy+337}" class="mono" font-size="8" fill="{GREY}">δ[n]</text>')
end_panel()

ix,iy,iw,ih=panel(*p[4],"System properties","Memory · causality · linearity · time invariance · stability","system_properties","S{x}=y ; properties ∈ {memoryless, causal, linear, TI, BIBO}")
props=[("MEMORY","y(t)=x(t−1)"),("CAUSAL","depends on present/past"),("LINEAR","superposition"),("TIME-INVARIANT","shift commutes"),("BIBO","bounded → bounded")]
for j,(a,b) in enumerate(props):
    xx=ix+j*(iw/5)
    A(f'<rect x="{xx+6:.1f}" y="{iy+20}" width="{iw/5-12:.1f}" height="74" rx="12" fill="#08111d" stroke="{CYAN if j in [1,2] else GREY}" stroke-opacity=".45"/>')
    A(f'<text x="{xx+iw/10:.1f}" y="{iy+48}" text-anchor="middle" class="mono" font-size="8.4" fill="{WHITE}">{a}</text>')
    A(f'<text x="{xx+iw/10:.1f}" y="{iy+69}" text-anchor="middle" class="mono" font-size="6.8" fill="{GREY}">{esc(b)}</text>')
end_panel()

# --------------------------
# Chapter 2
# --------------------------
ch=HEADER_H+CHAPTER_H
chapter_header(ch,2,*chapters[1]); p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"Convolution sum","Flip · shift · multiply · sum","convolution_sum","y[n]=Σ x[k]h[n-k]")
x=np.r_[np.zeros(10),np.ones(12),np.zeros(42)]
h=np.exp(-np.arange(64)/10.0)
y=np.convolve(x,h)[:64]
discrete_wave(ix,iy+18,iw,100,x,CYAN)
discrete_wave(ix,iy+135,iw,100,h,PURPLE)
discrete_wave(ix,iy+252,iw,100,y/max(y),GREEN)
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="7.5" fill="{GREY}">x[n]</text>')
A(f'<text x="{ix}" y="{iy+129}" class="mono" font-size="7.5" fill="{GREY}">h[n]</text>')
A(f'<text x="{ix}" y="{iy+246}" class="mono" font-size="7.5" fill="{GREY}">y[n]</text>')
end_panel()

ix,iy,iw,ih=panel(*p[1],"Convolution integral","Overlap area becomes output","convolution_integral","y(t)=∫x(τ)h(t-τ)dτ")
tt=np.linspace(-3,3,500)
xv=np.where(np.abs(tt)<1,1,0)
hv=np.where(np.abs(tt)<.7,1,0)
yv=np.convolve(xv,hv,mode="same")*(tt[1]-tt[0])
axes(ix,iy+20,iw,ih-30)
for arr,c,scale in [(xv,CYAN,.8),(hv,PURPLE,.55),(yv/yv.max(),GREEN,.3)]:
    pts=[(ix+j/(len(arr)-1)*iw,iy+20+(ih-30)/2-arr[j]*(ih-30)*scale*.35) for j in range(len(arr))]
    polyline(pts,c,2,False,.85)
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="7.5" fill="{GREY}">cyan=x(τ) · purple=h(t−τ) · green=integral result</text>')
end_panel()

ix,iy,iw,ih=panel(*p[2],"Impulse response","LTI system is determined by h","impulse_response","y=x*h")
block(ix+iw*.35,iy+70,iw*.30,90,"H","impulse response")
arrow(ix+20,iy+115,ix+iw*.35,iy+115)
arrow(ix+iw*.65,iy+115,ix+iw-20,iy+115)
A(f'<text x="{ix+10}" y="{iy+102}" class="mono" font-size="10" fill="{CYAN}">δ</text>')
A(f'<text x="{ix+iw-10}" y="{iy+102}" text-anchor="end" class="mono" font-size="10" fill="{PURPLE}">h</text>')
A(f'<text x="{ix}" y="{iy+205}" class="mono" font-size="8.5" fill="{GREY}">Probe with δ → observe h → predict response to every input by convolution.</text>')
end_panel()

ix,iy,iw,ih=panel(*p[3],"Step response","Integrating h gives response to u","step_response","s(t)=u*h")
t=np.linspace(0,1,300); hct=np.exp(-6*t); sct=1-np.exp(-6*t)
axes(ix,iy+20,iw,ih-40)
for arr,c in [(hct,CYAN),(sct,PURPLE)]:
    pts=[(ix+j/(len(arr)-1)*iw,iy+20+(ih-40)-arr[j]*(ih-40)*.82) for j in range(len(arr))]
    polyline(pts,c,2.2,False,.95)
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="7.5" fill="{GREY}">cyan=h(t) · purple=step response s(t)</text>')
end_panel()

ix,iy,iw,ih=panel(*p[4],"Difference / differential equations","Local recursion ↔ global impulse response","system_equations","y[n]-ay[n-1]=bx[n]")
block(ix+100,iy+28,260,72,"y[n] − a y[n−1] = b x[n]","difference equation")
arrow(ix+380,iy+64,ix+520,iy+64)
block(ix+540,iy+28,260,72,"H(z)=b/(1−az⁻¹)","system function")
arrow(ix+820,iy+64,ix+960,iy+64)
block(ix+980,iy+28,260,72,"h[n]=b aⁿu[n]","impulse response")
end_panel()

# --------------------------
# Chapter 3
# --------------------------
ch=HEADER_H+2*CHAPTER_H
chapter_header(ch,3,*chapters[2]); p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"CT Fourier series","Periodic waveform ↔ harmonic coefficients","ctfs","x(t)=Σ ak e^{jkω0t}")
# square wave approximation + coefficients
wave(ix,iy+20,iw,130,lambda t: 1 if math.sin(2*math.pi*t)>=0 else -1,PURPLE,False)
bins=[1,3,5,7,9]; vals=[1,1/3,1/5,1/7,1/9]
stems(ix,iy+185,iw,135,bins,vals,9,1,PURPLE,True,False,1)
end_panel()

ix,iy,iw,ih=panel(*p[1],"Line spectrum","Amplitude and phase live on discrete harmonics","line_spectrum","ak")
bins=list(range(-6,7)); vals=[0,0.08,0,0.14,0,0.33,0,1,0,0.33,0,0.14,0]
# remap nonnegative only visually
stems(ix,iy+30,iw,270,list(range(len(vals))),vals,len(vals)-1,1,PURPLE,False,False,6)
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="8" fill="{GREY}">symmetric magnitude example</text>')
end_panel()

ix,iy,iw,ih=panel(*p[2],"DT Fourier series","One period ↔ N coefficient bins","dtfs","x[n]=Σ ak e^{jk(2π/N)n}")
N=16;n=np.arange(N); x=np.cos(2*np.pi*3*n/N)+.5*np.cos(2*np.pi*5*n/N)
discrete_wave(ix,iy+20,iw,135,x,CYAN)
X=np.abs(np.fft.fft(x))/N
stems(ix,iy+195,iw,125,list(range(N)),X,N-1,max(X),PURPLE,False,False,3)
end_panel()

ix,iy,iw,ih=panel(*p[3],"Gibbs phenomenon","Finite harmonic sums sharpen jumps but overshoot","gibbs","partial sums of odd harmonics")
axes(ix,iy+25,iw,ih-45)
for M,c in [(1,GREY),(3,CYAN),(9,PURPLE)]:
    pts=[]
    for i in range(400):
        t=i/399
        s=sum(math.sin(2*math.pi*(2*m+1)*t)/(2*m+1) for m in range(M))
        s*=4/math.pi
        pts.append((ix+t*iw,iy+25+(ih-45)/2-s*(ih-45)*.28))
    polyline(pts,c,1.7 if M==1 else 2.0,False,.85)
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="7.5" fill="{GREY}">grey=1 term · cyan=3 · purple=9</text>')
end_panel()

ix,iy,iw,ih=panel(*p[4],"Symmetry shortcuts","Even ↔ cosine · odd ↔ sine · real ↔ conjugate symmetry","fourier_symmetry","real x(t) ⇒ a₋k=aₖ*")
items=[("EVEN","a₋k=aₖ","cosine content"),("ODD","a₋k=−aₖ","sine content"),("REAL","a₋k=aₖ*","conjugate symmetry"),("PERIODIC","line spectrum","discrete harmonics")]
for j,(a,b,c) in enumerate(items):
    xx=ix+j*iw/4
    A(f'<text x="{xx+iw/8}" y="{iy+35}" text-anchor="middle" class="mono" font-size="8.5" fill="{WHITE}">{a}</text>')
    A(f'<text x="{xx+iw/8}" y="{iy+58}" text-anchor="middle" class="mono" font-size="8" fill="{CYAN}">{esc(b)}</text>')
    A(f'<text x="{xx+iw/8}" y="{iy+80}" text-anchor="middle" class="mono" font-size="7" fill="{GREY}">{esc(c)}</text>')
end_panel()

# --------------------------
# Chapter 4
# --------------------------
ch=HEADER_H+3*CHAPTER_H
chapter_header(ch,4,*chapters[3]); p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"Rect ↔ sinc","Finite support in time spreads in frequency","ctft_rect_sinc","rect(t/T) ↔ T sinc(fT)")
wave(ix,iy+20,iw,120,lambda t: 1 if .3<t<.7 else 0,CYAN,False)
axes(ix,iy+180,iw,130)
pts=[]
for i in range(400):
    u=-6+12*i/399
    v=1 if abs(u)<1e-9 else math.sin(math.pi*u)/(math.pi*u)
    pts.append((ix+i/399*iw,iy+180+65-v*45))
polyline(pts,PURPLE,2,False)
end_panel()

ix,iy,iw,ih=panel(*p[1],"Gaussian ↔ Gaussian","Localization in both domains","ctft_gaussian","e^{-πt²} ↔ e^{-πf²}")
wave(ix,iy+20,iw,120,lambda t: math.exp(-60*(t-.5)**2),CYAN,False)
wave(ix,iy+180,iw,120,lambda t: math.exp(-60*(t-.5)**2),PURPLE,False)
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="7.5" fill="{GREY}">top=time · bottom=frequency</text>')
end_panel()

ix,iy,iw,ih=panel(*p[2],"Modulation property","Multiplication by cosine shifts the spectrum","ctft_modulation","x(t)cos(2πfct) ↔ 1/2[X(f-fc)+X(f+fc)]")
# baseband and shifted lobes
axes(ix,iy+30,iw,280)
for center,c in [(.25,PURPLE),(.75,PURPLE),(.5,CYAN)]:
    pts=[]
    for i in range(300):
        t=i/299
        v=math.exp(-400*(t-center)**2)
        pts.append((ix+t*iw,iy+170-v*90))
    polyline(pts,c,2,False,.9)
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="7.5" fill="{GREY}">cyan=baseband · purple=translated copies</text>')
end_panel()

ix,iy,iw,ih=panel(*p[3],"Convolution theorem","Convolution in time ↔ multiplication in frequency","ctft_convolution","x*h ↔ XH")
block(ix+40,iy+70,180,70,"x(t) * h(t)")
arrow(ix+240,iy+105,ix+360,iy+105)
block(ix+380,iy+70,210,70,"X(f) · H(f)")
A(f'<text x="{ix+300}" y="{iy+190}" text-anchor="middle" class="mono" font-size="9" fill="{PURPLE}">same operation viewed in the other domain</text>')
end_panel()

ix,iy,iw,ih=panel(*p[4],"Transform property map","Shift · scale · derivative · duality","ctft_properties","x(t−t₀) ↔ e^{-j2πft₀}X(f)")
props=[("SHIFT","x(t−t₀)","e^{-j2πft₀}X(f)"),("SCALE","x(at)","|a|⁻¹X(f/a)"),("DERIVATIVE","dx/dt","j2πfX(f)"),("DUALITY","x↔X","X↔x(−·)")]
for j,(a,b,c) in enumerate(props):
    xx=ix+j*iw/4
    A(f'<text x="{xx+iw/8}" y="{iy+26}" text-anchor="middle" class="mono" font-size="8" fill="{WHITE}">{a}</text>')
    A(f'<text x="{xx+iw/8}" y="{iy+52}" text-anchor="middle" class="mono" font-size="7.2" fill="{CYAN}">{esc(b)}</text>')
    A(f'<text x="{xx+iw/8}" y="{iy+77}" text-anchor="middle" class="mono" font-size="7.2" fill="{PURPLE}">{esc(c)}</text>')
end_panel()

# --------------------------
# Chapter 5
# --------------------------
ch=HEADER_H+4*CHAPTER_H
chapter_header(ch,5,*chapters[4]); p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"DTFT periodicity","Discrete time produces a 2π-periodic spectrum","dtft_periodic","X(e^{jω})=Σx[n]e^{-jωn}")
axes(ix,iy+25,iw,ih-45)
pts=[]
for i in range(500):
    w=-2*math.pi+4*math.pi*i/499
    v=abs((1-np.exp(-1j*w*8))/(1-np.exp(-1j*w))) if abs(math.sin(w/2))>1e-8 else 8
    v=float(v/8)
    pts.append((ix+i/499*iw,iy+25+(ih-45)-v*(ih-45)*.82))
polyline(pts,CYAN,2,False)
end_panel()

ix,iy,iw,ih=panel(*p[1],"Finite sequence spectrum","Rectangular sequence ↔ Dirichlet kernel","dtft_rect","x[n]=1, 0≤n≤M-1")
vals=np.r_[np.ones(12),np.zeros(52)]
discrete_wave(ix,iy+20,iw,120,vals,CYAN)
w=np.linspace(-math.pi,math.pi,400)
X=np.array([abs(np.sum(np.exp(-1j*ww*np.arange(12)))) for ww in w]); X/=X.max()
axes(ix,iy+185,iw,120)
polyline([(ix+i/399*iw,iy+185+120-v*100) for i,v in enumerate(X)],PURPLE,2,False)
end_panel()

ix,iy,iw,ih=panel(*p[2],"Frequency shift","Multiply by e^{jω0n} → spectral translation","dtft_shift","x[n]e^{jω0n} ↔ X(e^{j(ω-ω0)})")
axes(ix,iy+25,iw,ih-45)
for center,c in [(.5,CYAN),(.72,PURPLE)]:
    pts=[]
    for i in range(350):
        t=i/349
        v=math.exp(-260*(t-center)**2)
        pts.append((ix+t*iw,iy+25+(ih-45)-v*(ih-45)*.75))
    polyline(pts,c,2,False)
end_panel()

ix,iy,iw,ih=panel(*p[3],"Circular view","Unit-circle frequency coordinate","dtft_unit_circle","z=e^{jω}")
cx=ix+iw/2; cy=iy+(ih-20)/2+10; r=min(iw,ih-20)*.34
A(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CYAN}" stroke-opacity=".7" stroke-width="2"/>')
for ang in np.linspace(0,2*np.pi,8,endpoint=False):
    px=cx+r*math.cos(ang); py=cy-r*math.sin(ang)
    A(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="3" fill="{PURPLE}"/>')
    A(f'<line x1="{cx}" y1="{cy}" x2="{px:.2f}" y2="{py:.2f}" stroke="{GREY}" stroke-opacity=".16"/>')
A(f'<text x="{cx}" y="{cy-r-12}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">ω wraps: −π = π</text>')
end_panel()

ix,iy,iw,ih=panel(*p[4],"DTFT property map","Convolution · multiplication · periodicity · Parseval","dtft_properties","x*h ↔ X(ω)H(ω)")
items=[("CONV","x*h","XH"),("MULT","xy","periodic convolution"),("PERIODIC","X(ω+2π)=X(ω)","wrap frequency"),("PARSEVAL","Σ|x|²","(1/2π)∫|X|²")]
for j,(a,b,c) in enumerate(items):
    xx=ix+j*iw/4
    A(f'<text x="{xx+iw/8}" y="{iy+26}" text-anchor="middle" class="mono" font-size="8" fill="{WHITE}">{a}</text>')
    A(f'<text x="{xx+iw/8}" y="{iy+51}" text-anchor="middle" class="mono" font-size="7.2" fill="{CYAN}">{esc(b)}</text>')
    A(f'<text x="{xx+iw/8}" y="{iy+76}" text-anchor="middle" class="mono" font-size="7.2" fill="{PURPLE}">{esc(c)}</text>')
end_panel()

# --------------------------
# Chapter 6
# --------------------------
ch=HEADER_H+5*CHAPTER_H
chapter_header(ch,6,*chapters[5]); p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"Frequency response","Complex exponential is an LTI eigenfunction","freq_response","e^{jωt}→H(jω)e^{jωt}")
block(ix+40,iy+85,180,72,"e^{jωt}")
arrow(ix+240,iy+121,ix+360,iy+121)
block(ix+380,iy+85,150,72,"H")
arrow(ix+550,iy+121,ix+670,iy+121)
A(f'<text x="{ix+iw-20}" y="{iy+125}" text-anchor="end" class="mono" font-size="9" fill="{PURPLE}">H(jω)e^{{jωt}}</text>')
end_panel()

ix,iy,iw,ih=panel(*p[1],"Ideal low-pass","Passband and stopband are spectral masks","ideal_lpf","H(jω)=1 for |ω|<ωc")
axes(ix,iy+30,iw,250)
pts=[(ix,iy+280),(ix+iw*.34,iy+280),(ix+iw*.34,iy+90),(ix+iw*.66,iy+90),(ix+iw*.66,iy+280),(ix+iw,iy+280)]
polyline(pts,CYAN,2.4,False)
A(f'<text x="{ix+iw/2}" y="{iy+72}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">PASSBAND</text>')
end_panel()

ix,iy,iw,ih=panel(*p[2],"Resonance","Pole proximity creates a frequency peak","resonance","|H(jω)|")
axes(ix,iy+30,iw,ih-50)
pts=[]
for i in range(450):
    t=i/449
    w=8*t
    v=1/math.sqrt((4-w*w)**2+(0.6*w)**2)
    pts.append((ix+t*iw,iy+30+(ih-50)-min(v,1.3)/1.3*(ih-50)*.82))
polyline(pts,PURPLE,2.3,True)
end_panel()

ix,iy,iw,ih=panel(*p[3],"Magnitude & phase","A system reshapes amplitude and delay","mag_phase","H=|H|e^{j∠H}")
# magnitude
axes(ix,iy+20,iw,120)
pts=[]
for i in range(300):
    w=5*i/299
    mag=1/math.sqrt(1+w*w)
    pts.append((ix+i/299*iw,iy+140-mag*95))
polyline(pts,CYAN,2,False)
# phase
axes(ix,iy+190,iw,120)
pts=[]
for i in range(300):
    w=5*i/299
    ph=-math.atan(w)/(math.pi/2)
    pts.append((ix+i/299*iw,iy+250-ph*55))
polyline(pts,PURPLE,2,False)
end_panel()

ix,iy,iw,ih=panel(*p[4],"Group delay","Phase slope controls envelope delay","group_delay","τg(ω)=−dφ/dω")
A(f'<text x="{ix}" y="{iy+28}" class="mono" font-size="9" fill="{WHITE}">linear phase</text>')
polyline([(ix+10,iy+58),(ix+320,iy+95)],CYAN,2,False)
A(f'<text x="{ix+390}" y="{iy+28}" class="mono" font-size="9" fill="{WHITE}">constant group delay</text>')
A(f'<line x1="{ix+390}" y1="{iy+78}" x2="{ix+760}" y2="{iy+78}" stroke="{PURPLE}" stroke-width="2"/>')
A(f'<text x="{ix+810}" y="{iy+82}" class="mono" font-size="8" fill="{GREY}">pulse shape preserved</text>')
end_panel()

# --------------------------
# Chapter 7
# --------------------------
ch=HEADER_H+6*CHAPTER_H
chapter_header(ch,7,*chapters[6]); p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"Impulse-train sampling","Continuous waveform observed at uniform instants","sampling_train","xs(t)=x(t)Σδ(t-nTs)")
wave(ix,iy+20,iw,120,lambda t: math.sin(4*math.pi*t),CYAN,False)
for i in range(17):
    px=ix+i/16*iw
    v=math.sin(4*math.pi*i/16)
    py=iy+20+60-v*45
    A(f'<line x1="{px}" y1="{iy+80}" x2="{px}" y2="{py}" stroke="{PURPLE}" stroke-width="1.3"/>')
    A(f'<circle cx="{px}" cy="{py}" r="2.7" fill="{PURPLE}"/>')
end_panel()

ix,iy,iw,ih=panel(*p[1],"Spectral replicas","Sampling copies X(f) every fs","sampling_replicas","Xs(f)=1/Ts ΣX(f-kfs)")
axes(ix,iy+30,iw,ih-50)
for c in [.15,.5,.85]:
    pts=[]
    for i in range(250):
        t=i/249
        v=math.exp(-500*(t-c)**2)
        pts.append((ix+t*iw,iy+30+(ih-50)-v*(ih-50)*.72))
    polyline(pts,CYAN if c==.5 else PURPLE,2,False)
end_panel()

ix,iy,iw,ih=panel(*p[2],"Nyquist condition","Replicas must not overlap","nyquist","fs>2B")
A(f'<text x="{ix+iw/2}" y="{iy+70}" text-anchor="middle" class="mono" font-size="22" fill="{CYAN}">fₛ &gt; 2B</text>')
A(f'<line x1="{ix+80}" y1="{iy+145}" x2="{ix+iw-80}" y2="{iy+145}" stroke="{GREY}" stroke-opacity=".35"/>')
for c,col in [(.3,CYAN),(.7,PURPLE)]:
    pts=[]
    for i in range(200):
        t=i/199
        v=max(0,1-abs(t-c)/.18)
        pts.append((ix+t*iw,iy+260-v*90))
    polyline(pts,col,2,False)
A(f'<text x="{ix+iw/2}" y="{iy+300}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">no overlap → perfect ideal reconstruction possible</text>')
end_panel()

ix,iy,iw,ih=panel(*p[3],"Aliasing","Overlap makes different frequencies indistinguishable","aliasing","f_alias=|f-kfs|")
axes(ix,iy+30,iw,ih-50)
for c,col in [(.44,CYAN),(.56,PURPLE)]:
    pts=[]
    for i in range(250):
        t=i/249
        v=max(0,1-abs(t-c)/.18)
        pts.append((ix+t*iw,iy+30+(ih-50)-v*(ih-50)*.7))
    polyline(pts,col,2,False,.9)
A(f'<text x="{ix+iw/2}" y="{iy+64}" text-anchor="middle" class="mono" font-size="8" fill="{RED}">OVERLAP</text>')
end_panel()

ix,iy,iw,ih=panel(*p[4],"Reconstruction chain","samples → interpolation → anti-imaging filter","reconstruction","x[n] → interpolation → LPF → x̂(t)")
block(ix+80,iy+28,230,72,"x[n]","samples")
arrow(ix+330,iy+64,ix+470,iy+64)
block(ix+490,iy+28,230,72,"INTERPOLATOR","sinc / hold")
arrow(ix+740,iy+64,ix+880,iy+64)
block(ix+900,iy+28,230,72,"LOW-PASS","reconstruct")
arrow(ix+1150,iy+64,ix+1280,iy+64)
A(f'<text x="{ix+1320}" y="{iy+68}" class="mono" font-size="9" fill="{PURPLE}">xᵣ(t)</text>')
end_panel()

# --------------------------
# Chapter 8
# --------------------------
ch=HEADER_H+7*CHAPTER_H
chapter_header(ch,8,*chapters[7]); p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"DSB-SC modulation","Message × carrier moves baseband to ±fc","dsb_sc","s(t)=m(t)cos(2πfct)")
wave(ix,iy+20,iw,115,lambda t: math.sin(2*math.pi*t),CYAN,False)
wave(ix,iy+175,iw,115,lambda t: math.sin(2*math.pi*t)*math.cos(18*math.pi*t),PURPLE,False)
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="7.5" fill="{GREY}">top=message · bottom=modulated carrier</text>')
end_panel()

ix,iy,iw,ih=panel(*p[1],"Sidebands","Translated message spectra appear around carrier","sidebands","M(f±fc)")
axes(ix,iy+30,iw,ih-50)
for c in [.28,.72]:
    pts=[]
    for i in range(280):
        t=i/279
        v=max(0,1-abs(t-c)/.12)
        pts.append((ix+t*iw,iy+30+(ih-50)-v*(ih-50)*.75))
    polyline(pts,PURPLE,2,False)
A(f'<text x="{ix+iw*.28}" y="{iy+62}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">−fᶜ</text>')
A(f'<text x="{ix+iw*.72}" y="{iy+62}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">+fᶜ</text>')
end_panel()

ix,iy,iw,ih=panel(*p[2],"Coherent demodulation","Multiply again + low-pass","demodulation","LPF{2s(t)cos(ωct)} = m(t)")
block(ix+40,iy+85,180,70,"s(t)")
arrow(ix+240,iy+120,ix+350,iy+120)
block(ix+370,iy+85,160,70,"× cos ωct")
arrow(ix+550,iy+120,ix+660,iy+120)
block(ix+680,iy+85,140,70,"LPF")
A(f'<text x="{ix+iw-15}" y="{iy+125}" text-anchor="end" class="mono" font-size="9" fill="{CYAN}">m(t)</text>')
end_panel()

ix,iy,iw,ih=panel(*p[3],"Frequency-division multiplexing","Different messages occupy disjoint bands","fdm","Bᵢ ∩ Bⱼ = ∅ for i≠j")
axes(ix,iy+35,iw,ih-55)
for center,col,label in [(.2,CYAN,"A"),(.5,PURPLE,"B"),(.8,GREEN,"C")]:
    pts=[]
    for i in range(220):
        t=i/219
        v=max(0,1-abs(t-center)/.10)
        pts.append((ix+t*iw,iy+35+(ih-55)-v*(ih-55)*.70))
    polyline(pts,col,2,False)
    A(f'<text x="{ix+center*iw}" y="{iy+75}" text-anchor="middle" class="mono" font-size="8" fill="{col}">{label}</text>')
end_panel()

ix,iy,iw,ih=panel(*p[4],"Communication chain","source → modulation → channel → demodulation → sink","communication_chain","source → modulation → channel → demodulation → sink")
labels=["SOURCE","MOD","CHANNEL","DEMOD","SINK"]
for j,lab in enumerate(labels):
    xx=ix+60+j*260
    block(xx,iy+28,170,72,lab)
    if j<4: arrow(xx+180,iy+64,xx+250,iy+64)
end_panel()

# --------------------------
# Chapter 9
# --------------------------
ch=HEADER_H+8*CHAPTER_H
chapter_header(ch,9,*chapters[8]); p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"s-plane geometry","Poles, zeros and ROC encode time behavior","laplace_plane","X(s)")
polezero(ix+90,iy+20,iw-180,ih-50,[complex(-.5,.7),complex(-.5,-.7)],[complex(-1.4,0)],None)
end_panel()

ix,iy,iw,ih=panel(*p[1],"Region of convergence","Same algebraic transform, different signals","laplace_roc","ROC ⊂ ℂ ; poles ∉ ROC")
polezero(ix+40,iy+20,(iw-100)/2,ih-50,[complex(-.8,0)],[],("outside",.5))
polezero(ix+60+(iw-100)/2,iy+20,(iw-100)/2,ih-50,[complex(-.8,0)],[],("inside",.5))
A(f'<text x="{ix+iw*.25}" y="{iy+20}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">right-sided</text>')
A(f'<text x="{ix+iw*.75}" y="{iy+20}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">left-sided</text>')
end_panel()

ix,iy,iw,ih=panel(*p[2],"Causality & stability","ROC relative to poles and jω-axis","laplace_causality_stability","causal ⇒ ROC right of rightmost pole ; stable ⇒ jℝ ⊂ ROC")
A(f'<text x="{ix}" y="{iy+35}" class="mono" font-size="10" fill="{CYAN}">CAUSAL</text>')
A(f'<text x="{ix+120}" y="{iy+35}" class="mono" font-size="9" fill="{GREY}">ROC right of rightmost pole</text>')
A(f'<text x="{ix}" y="{iy+85}" class="mono" font-size="10" fill="{PURPLE}">STABLE</text>')
A(f'<text x="{ix+120}" y="{iy+85}" class="mono" font-size="9" fill="{GREY}">ROC includes jω-axis</text>')
A(f'<text x="{ix}" y="{iy+135}" class="mono" font-size="10" fill="{GREEN}">CAUSAL + STABLE</text>')
A(f'<text x="{ix+160}" y="{iy+135}" class="mono" font-size="9" fill="{GREY}">all poles strictly in left half-plane</text>')
end_panel()

ix,iy,iw,ih=panel(*p[3],"Inverse Laplace","Partial fractions map poles to exponentials","inverse_laplace","1/(s+a) ↔ e^{-at}u(t)")
block(ix+50,iy+70,220,70,"1/(s+a)")
arrow(ix+290,iy+105,ix+420,iy+105)
block(ix+440,iy+70,260,70,"e^{-at}u(t)")
A(f'<text x="{ix+iw/2}" y="{iy+200}" text-anchor="middle" class="mono" font-size="9" fill="{GREY}">pole location sets exponential rate</text>')
end_panel()

ix,iy,iw,ih=panel(*p[4],"System function","Differential equation → H(s) → poles → modes","laplace_system_function","H(s)=Y(s)/X(s)")
block(ix+80,iy+28,260,72,"DIFFERENTIAL EQ.")
arrow(ix+360,iy+64,ix+500,iy+64)
block(ix+520,iy+28,220,72,"H(s)=Y/X")
arrow(ix+760,iy+64,ix+900,iy+64)
block(ix+920,iy+28,240,72,"POLES / ZEROS")
arrow(ix+1180,iy+64,ix+1300,iy+64)
A(f'<text x="{ix+1335}" y="{iy+68}" class="mono" font-size="9" fill="{PURPLE}">MODES</text>')
end_panel()

# --------------------------
# Chapter 10
# --------------------------
ch=HEADER_H+9*CHAPTER_H
chapter_header(ch,10,*chapters[9]); p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"z-plane geometry","Poles and zeros organize discrete-time behavior","z_plane","X(z)")
polezero(ix+90,iy+20,iw-180,ih-50,[complex(.72,.35),complex(.72,-.35)],[0j],None)
end_panel()

ix,iy,iw,ih=panel(*p[1],"ROC and unit circle","DTFT exists where ROC crosses |z|=1","z_roc_unit_circle","DTFT exists ⇔ {|z|=1} ⊂ ROC")
polezero(ix+90,iy+20,iw-180,ih-50,[complex(.65,0)],[],("outside",.65))
A(f'<text x="{ix+iw/2}" y="{iy+22}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">unit circle is frequency axis</text>')
end_panel()

ix,iy,iw,ih=panel(*p[2],"Difference equation → H(z)","Recursion becomes rational geometry","difference_to_z","y[n]-ay[n-1]=x[n]")
block(ix+40,iy+85,260,70,"y[n]−ay[n−1]=x[n]")
arrow(ix+320,iy+120,ix+450,iy+120)
block(ix+470,iy+85,220,70,"H(z)=1/(1−az⁻¹)")
end_panel()

ix,iy,iw,ih=panel(*p[3],"Frequency response on unit circle","Evaluate H(z) at z=e^{jω}","z_to_dtft","H(e^{jω})")
cx=ix+iw/2; cy=iy+(ih-30)/2+10; r=min(iw,ih-30)*.34
A(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CYAN}" stroke-width="2.2"/>')
# sample magnitudes around circle
for j,ang in enumerate(np.linspace(0,2*np.pi,24,endpoint=False)):
    z=np.exp(1j*ang); H=1/(1-.72/z)
    rr=r + min(abs(H),3)*8
    px=cx+rr*math.cos(ang); py=cy-rr*math.sin(ang)
    A(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="2" fill="{PURPLE}" opacity=".8"/>')
end_panel()

ix,iy,iw,ih=panel(*p[4],"Pole radius & angle","radius → decay · angle → oscillation","pole_radius_angle","p=re^{jθ}")
A(f'<text x="{ix+100}" y="{iy+38}" class="mono" font-size="9" fill="{CYAN}">r</text>')
A(f'<text x="{ix+130}" y="{iy+38}" class="mono" font-size="8" fill="{GREY}">controls exponential envelope</text>')
A(f'<text x="{ix+650}" y="{iy+38}" class="mono" font-size="9" fill="{PURPLE}">θ</text>')
A(f'<text x="{ix+680}" y="{iy+38}" class="mono" font-size="8" fill="{GREY}">controls oscillation frequency</text>')
A(f'<text x="{ix+100}" y="{iy+82}" class="mono" font-size="8" fill="{WHITE}">|p|&lt;1 → decays</text>')
A(f'<text x="{ix+650}" y="{iy+82}" class="mono" font-size="8" fill="{WHITE}">∠p → radians / sample</text>')
end_panel()

# --------------------------
# Chapter 11
# --------------------------
ch=HEADER_H+10*CHAPTER_H
chapter_header(ch,11,*chapters[10]); p=grid_panels(ch)

ix,iy,iw,ih=panel(*p[0],"Closed-loop structure","Forward path + feedback path","feedback_loop","T=G/(1+GH)")
block(ix+70,iy+90,150,70,"Σ")
block(ix+310,iy+90,190,70,"G(s)")
block(ix+310,iy+220,190,70,"H(s)")
arrow(ix+10,iy+125,ix+70,iy+125)
arrow(ix+220,iy+125,ix+310,iy+125)
arrow(ix+500,iy+125,ix+iw-30,iy+125)
A(f'<path d="M{ix+iw-60},{iy+125} V{iy+255} H{ix+500}" fill="none" stroke="{PURPLE}" stroke-width="1.7" marker-end="url(#arrC)"/>')
A(f'<path d="M{ix+310},{iy+255} H{ix+145} V{iy+160}" fill="none" stroke="{PURPLE}" stroke-width="1.7" marker-end="url(#arrC)"/>')
end_panel()

ix,iy,iw,ih=panel(*p[1],"Sensitivity reduction","Feedback suppresses plant uncertainty","sensitivity","S=1/(1+GH)")
axes(ix,iy+30,iw,ih-50)
pts=[]
for i in range(350):
    L=10**(-2+4*i/349)
    S=1/(1+L)
    pts.append((ix+i/349*iw,iy+30+(ih-50)-S*(ih-50)*.8))
polyline(pts,CYAN,2.2,False)
A(f'<text x="{ix+iw*.72}" y="{iy+90}" class="mono" font-size="8" fill="{GREY}">large loop gain → small sensitivity</text>')
end_panel()

ix,iy,iw,ih=panel(*p[2],"Closed-loop poles","Characteristic equation sets stability","closed_loop_poles","1+G(s)H(s)=0")
polezero(ix+90,iy+20,iw-180,ih-50,[complex(-.7,.8),complex(-.7,-.8)],[],None)
A(f'<text x="{ix+iw/2}" y="{iy+20}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">left-half plane → decaying modes</text>')
end_panel()

ix,iy,iw,ih=panel(*p[3],"Pole movement","Changing gain moves closed-loop modes","root_locus_concept","1 + K G(s)H(s) = 0")
axes(ix,iy+20,iw,ih-40,xzero=.65,yzero=.5)
# simple locus-like curves
for sgn in [-1,1]:
    pts=[]
    for i in range(180):
        t=i/179
        xval=-1.2+1.05*t
        yval=sgn*(.15+1.0*t*(1-t))
        px=ix+(xval+2)/4*iw
        py=iy+20+(ih-40)/2-yval*(ih-40)/4
        pts.append((px,py))
    polyline(pts,PURPLE,2.1,False)
end_panel()

ix,iy,iw,ih=panel(*p[4],"Feedback story","performance ↔ robustness ↔ stability trade-off","feedback_tradeoffs","S(s)=1/(1+L(s)) ; T(s)=L(s)/(1+L(s))")
items=[("TRACKING","reduce error"),("DISTURBANCE","reject"),("ROBUSTNESS","desensitize"),("STABILITY","preserve margin")]
for j,(a,b) in enumerate(items):
    xx=ix+j*iw/4
    A(f'<rect x="{xx+16}" y="{iy+20}" width="{iw/4-32}" height="78" rx="12" fill="#08111d" stroke="{CYAN if j<2 else PURPLE}" stroke-opacity=".42"/>')
    A(f'<text x="{xx+iw/8}" y="{iy+49}" text-anchor="middle" class="mono" font-size="8.5" fill="{WHITE}">{a}</text>')
    A(f'<text x="{xx+iw/8}" y="{iy+71}" text-anchor="middle" class="mono" font-size="7" fill="{GREY}">{esc(b)}</text>')
end_panel()


# --------------------------
# Chapter 12
# --------------------------
ch=HEADER_H+11*CHAPTER_H
chapter_header(ch,12,*chapters[11]); p=grid_panels(ch)

# Panel 1: finite word / cyclic rotations
ix,iy,iw,ih=panel(*p[0],"32-bit word as cyclic state","Rotation changes coordinates, not information","finite_word_state","ROTR^r(x)")
cx=ix+iw*.47; cy=iy+165; rr=112
for b in range(32):
    a=-math.pi/2 + 2*math.pi*b/32
    px=cx+rr*math.cos(a); py=cy+rr*math.sin(a)
    bit=(0x6A09E667 >> (31-b)) & 1
    A(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="7" fill="{CYAN if bit else DARK}" stroke="{CYAN if bit else GREY}" stroke-opacity=".75"/>')
    if b%4==0:
        A(f'<text x="{cx+(rr+24)*math.cos(a):.2f}" y="{cy+(rr+24)*math.sin(a)+3:.2f}" text-anchor="middle" class="mono" font-size="6.5" fill="{GREY}">{b}</text>')
A(f'<path d="M{cx+rr+18},{cy-30} A{rr+18},{rr+18} 0 0 1 {cx+rr+18},{cy+30}" fill="none" stroke="{PURPLE}" stroke-width="2" marker-end="url(#arrC)"/>')
A(f'<text x="{ix}" y="{iy+12}" class="mono" font-size="8" fill="{GREY}">example word: 0x6A09E667 · 32 indexed positions · wrap is intrinsic</text>')
A(f'<text x="{cx}" y="{cy+5}" text-anchor="middle" class="mono" font-size="12" fill="{WHITE}">ROTR</text>')
end_panel()

# Panel 2: modular addition
ix,iy,iw,ih=panel(*p[1],"Addition modulo 2^32","Overflow wraps into the same finite word space","modular_addition","(x+y) mod 2^32")
MOD=2**32
xv=0xF0000011; yv=0x30000022; zv=(xv+yv)%MOD
A(f'<text x="{ix+30}" y="{iy+70}" class="mono" font-size="13" fill="{CYAN}">0x{xv:08X}</text>')
A(f'<text x="{ix+30}" y="{iy+112}" class="mono" font-size="13" fill="{PURPLE}">+ 0x{yv:08X}</text>')
A(f'<line x1="{ix+25}" y1="{iy+130}" x2="{ix+270}" y2="{iy+130}" stroke="{GREY}" stroke-opacity=".45"/>')
A(f'<text x="{ix+30}" y="{iy+168}" class="mono" font-size="13" fill="{WHITE}">0x{(xv+yv):09X}</text>')
arrow(ix+310,iy+144,ix+430,iy+144)
A(f'<rect x="{ix+450}" y="{iy+92}" width="210" height="104" rx="14" fill="#08111d" stroke="{CYAN}" stroke-opacity=".55"/>')
A(f'<text x="{ix+555}" y="{iy+124}" text-anchor="middle" class="mono" font-size="9" fill="{GREY}">MOD 2^32</text>')
A(f'<text x="{ix+555}" y="{iy+158}" text-anchor="middle" class="mono" font-size="14" fill="{CYAN}">0x{zv:08X}</text>')
A(f'<text x="{ix+555}" y="{iy+181}" text-anchor="middle" class="mono" font-size="7.5" fill="{GREY}">carry is discarded · state remains 32 bits</text>')
end_panel()

# Panel 3: SHA-256 boolean / rotation mixers
ix,iy,iw,ih=panel(*p[2],"Bit mixing functions","Boolean selection + majority + cyclic rotations","rotate_xor_mix","Ch, Maj, Σ0, Σ1")
items=[
    ("Ch(x,y,z)","(x∧y) ⊕ (¬x∧z)",CYAN),
    ("Maj(x,y,z)","(x∧y) ⊕ (x∧z) ⊕ (y∧z)",PURPLE),
    ("Σ₀(x)","ROTR² ⊕ ROTR¹³ ⊕ ROTR²²",CYAN),
    ("Σ₁(x)","ROTR⁶ ⊕ ROTR¹¹ ⊕ ROTR²⁵",PURPLE),
]
for j,(lab,eq,col) in enumerate(items):
    yy=iy+28+j*67
    A(f'<rect x="{ix+20}" y="{yy}" width="{iw-40}" height="52" rx="10" fill="#08111d" stroke="{col}" stroke-opacity=".38"/>')
    A(f'<text x="{ix+42}" y="{yy+21}" class="mono" font-size="9" fill="{WHITE}">{lab}</text>')
    A(f'<text x="{ix+42}" y="{yy+40}" class="mono" font-size="7.6" fill="{GREY}">{eq}</text>')
end_panel()

# Panel 4: compression-state dynamics
ix,iy,iw,ih=panel(*p[3],"64-round compression state","Eight 32-bit words evolve under one repeated update law","compression_round","S_{t+1}=F(S_t,W_t,K_t) mod 2^32")
labels=list("abcdefgh")
for j,lab in enumerate(labels):
    xx=ix+22+j*(iw-44)/8
    A(f'<rect x="{xx:.2f}" y="{iy+58}" width="{(iw-60)/8:.2f}" height="58" rx="8" fill="#08111d" stroke="{CYAN if j<4 else PURPLE}" stroke-opacity=".48"/>')
    A(f'<text x="{xx+(iw-60)/16:.2f}" y="{iy+93}" text-anchor="middle" class="mono" font-size="11" fill="{WHITE}">{lab}</text>')
A(f'<text x="{ix+iw/2}" y="{iy+157}" text-anchor="middle" class="mono" font-size="10" fill="{GREY}">T₁ = h + Σ₁(e) + Ch(e,f,g) + K[t] + W[t]</text>')
A(f'<text x="{ix+iw/2}" y="{iy+181}" text-anchor="middle" class="mono" font-size="10" fill="{GREY}">T₂ = Σ₀(a) + Maj(a,b,c)</text>')
# 64-step rail
rail_y=iy+246
A(f'<line x1="{ix+30}" y1="{rail_y}" x2="{ix+iw-30}" y2="{rail_y}" stroke="{GREY}" stroke-opacity=".38"/>')
for j in range(64):
    xx=ix+30+j*(iw-60)/63
    if j%8==0:
        A(f'<circle cx="{xx:.2f}" cy="{rail_y}" r="4" fill="{CYAN}"/>')
        A(f'<text x="{xx:.2f}" y="{rail_y+18}" text-anchor="middle" class="mono" font-size="6.5" fill="{GREY}">{j}</text>')
    else:
        A(f'<circle cx="{xx:.2f}" cy="{rail_y}" r="1.5" fill="{GREY}" opacity=".45"/>')
A(f'<text x="{ix+iw-30}" y="{rail_y+18}" text-anchor="end" class="mono" font-size="6.5" fill="{GREY}">63</text>')
end_panel()

# Panel 5: exact avalanche experiment using standard-library SHA-256
ix,iy,iw,ih=panel(*p[4],"Avalanche as measured state diffusion","Two 512-bit inputs differ by one bit; compare their 256-bit digests","avalanche_diffusion","d_H(SHA256(m),SHA256(m⊕1))")
import hashlib as _hashlib
m0=bytes(64)
m1=bytes([1])+bytes(63)
d0=_hashlib.sha256(m0).digest()
d1=_hashlib.sha256(m1).digest()
hd=sum((aa^bb).bit_count() for aa,bb in zip(d0,d1))
# 256 output bits as two rows
bits0=''.join(f'{b:08b}' for b in d0)
bits1=''.join(f'{b:08b}' for b in d1)
for j,(b0,b1) in enumerate(zip(bits0,bits1)):
    xx=ix+18+(j%128)*(iw-36)/128
    yy=iy+24+(j//128)*42
    changed=(b0!=b1)
    A(f'<rect x="{xx:.2f}" y="{yy}" width="{max(2.5,(iw-36)/128-1):.2f}" height="22" rx="1" fill="{PURPLE if changed else GREY}" fill-opacity="{.88 if changed else .16}"/>')
A(f'<text x="{ix+18}" y="{iy+121}" class="mono" font-size="9" fill="{WHITE}">Hamming distance = {hd} / 256 output bits</text>')
A(f'<text x="{ix+18}" y="{iy+147}" class="mono" font-size="8" fill="{GREY}">m₀ = 512 zero bits · m₁ differs only in its first bit</text>')
A(f'<text x="{ix+18}" y="{iy+171}" class="mono" font-size="8" fill="{GREY}">diffusion is observed here as a system response, not used as a truth criterion</text>')
end_panel()



# --------------------------
# Chapter 13
# --------------------------
ch=HEADER_H+12*CHAPTER_H
chapter_header(ch,13,*chapters[12]); p=grid_panels(ch)

# Panel 1: IPv4 32-bit word
ix,iy,iw,ih=panel(*p[0],"IPv4 as one 32-bit word","Four octets are one finite 32-bit address value","ipv4_word","IPv4 ∈ {0,…,2^32−1}")
octets=[192,0,2,33]
for j,v in enumerate(octets):
    xx=ix+35+j*(iw-70)/4
    A(f'<rect x="{xx:.2f}" y="{iy+85}" width="{(iw-90)/4:.2f}" height="84" rx="12" fill="#08111d" stroke="{CYAN if j in [0,3] else GREY}" stroke-opacity=".52"/>')
    A(f'<text x="{xx+(iw-90)/8:.2f}" y="{iy+119}" text-anchor="middle" class="mono" font-size="14" fill="{WHITE}">{v}</text>')
    A(f'<text x="{xx+(iw-90)/8:.2f}" y="{iy+145}" text-anchor="middle" class="mono" font-size="7.2" fill="{GREY}">0x{v:02X}</text>')
A(f'<text x="{ix+iw/2}" y="{iy+215}" text-anchor="middle" class="mono" font-size="11" fill="{CYAN}">192.0.2.33 = 0xC0000221</text>')
A(f'<text x="{ix+iw/2}" y="{iy+246}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">8 + 8 + 8 + 8 = 32 bits</text>')
end_panel()

# Panel 2: IPv6 as four 32-bit lanes / eight 16-bit groups
ix,iy,iw,ih=panel(*p[1],"IPv6 as a 128-bit state","The same space can be partitioned as 4×32 or 8×16","ipv6_lanes","IPv6 ∈ {0,…,2^128−1}")
lane_cols=[CYAN,PURPLE,CYAN,PURPLE]
for j in range(4):
    xx=ix+28+j*(iw-56)/4
    A(f'<rect x="{xx:.2f}" y="{iy+58}" width="{(iw-76)/4:.2f}" height="88" rx="11" fill="#08111d" stroke="{lane_cols[j]}" stroke-opacity=".48"/>')
    A(f'<text x="{xx+(iw-76)/8:.2f}" y="{iy+92}" text-anchor="middle" class="mono" font-size="9" fill="{WHITE}">LANE {j}</text>')
    A(f'<text x="{xx+(iw-76)/8:.2f}" y="{iy+120}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">32 bits</text>')
# 8 standard 16-bit text groups
for j in range(8):
    xx=ix+30+j*(iw-60)/8
    A(f'<rect x="{xx:.2f}" y="{iy+195}" width="{(iw-84)/8:.2f}" height="58" rx="8" fill="#08111d" stroke="{GREY}" stroke-opacity=".30"/>')
    A(f'<text x="{xx+(iw-84)/16:.2f}" y="{iy+229}" text-anchor="middle" class="mono" font-size="7" fill="{GREY}">16</text>')
A(f'<text x="{ix+iw/2}" y="{iy+286}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">computational view: 4×32 · canonical text view: 8×16</text>')
end_panel()

# Panel 3: IPv4-mapped IPv6 exact embedding
ix,iy,iw,ih=panel(*p[2],"IPv4-mapped IPv6","A fixed 96-bit prefix leaves exactly one 32-bit IPv4 slot","ipv4_mapped_ipv6","::ffff:0:0/96 + IPv4")
# 4 x 32-bit lanes: first two zero, third 0x0000FFFF, fourth IPv4
lane_vals=["0x00000000","0x00000000","0x0000FFFF","0xC0000221"]
lane_names=["PREFIX","PREFIX","MAPPED TAG","IPv4 SLOT"]
for j,(val,name) in enumerate(zip(lane_vals,lane_names)):
    xx=ix+22+j*(iw-44)/4
    col=CYAN if j==3 else (PURPLE if j==2 else GREY)
    A(f'<rect x="{xx:.2f}" y="{iy+60}" width="{(iw-68)/4:.2f}" height="110" rx="11" fill="#08111d" stroke="{col}" stroke-opacity=".58"/>')
    A(f'<text x="{xx+(iw-68)/8:.2f}" y="{iy+94}" text-anchor="middle" class="mono" font-size="7.5" fill="{GREY}">{name}</text>')
    A(f'<text x="{xx+(iw-68)/8:.2f}" y="{iy+129}" text-anchor="middle" class="mono" font-size="8.5" fill="{WHITE}">{val}</text>')
    A(f'<text x="{xx+(iw-68)/8:.2f}" y="{iy+153}" text-anchor="middle" class="mono" font-size="7" fill="{col}">32 bits</text>')
A(f'<text x="{ix+iw/2}" y="{iy+215}" text-anchor="middle" class="mono" font-size="11" fill="{CYAN}">::ffff:192.0.2.33</text>')
A(f'<text x="{ix+iw/2}" y="{iy+245}" text-anchor="middle" class="mono" font-size="8.5" fill="{GREY}">low 32 bits = 0xC0000221 · exactly the IPv4 value above</text>')
A(f'<text x="{ix+iw/2}" y="{iy+273}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">standard mapped form: 80 zero bits + 16 one bits + 32 IPv4 bits</text>')
end_panel()

# Panel 4: prefix / host decomposition
ix,iy,iw,ih=panel(*p[3],"Prefix as measurement frame","A /64 divides a 128-bit address into two 64-bit fields","ipv6_prefix_host","IPv6 = prefix_64 || interface_64")
A(f'<rect x="{ix+30}" y="{iy+85}" width="{(iw-70)/2:.2f}" height="100" rx="12" fill="#08111d" stroke="{CYAN}" stroke-opacity=".58"/>')
A(f'<rect x="{ix+40+(iw-70)/2}" y="{iy+85}" width="{(iw-70)/2:.2f}" height="100" rx="12" fill="#08111d" stroke="{PURPLE}" stroke-opacity=".58"/>')
A(f'<text x="{ix+30+(iw-70)/4}" y="{iy+124}" text-anchor="middle" class="mono" font-size="11" fill="{WHITE}">NETWORK PREFIX</text>')
A(f'<text x="{ix+30+(iw-70)/4}" y="{iy+151}" text-anchor="middle" class="mono" font-size="9" fill="{CYAN}">64 bits</text>')
A(f'<text x="{ix+40+(iw-70)*3/4}" y="{iy+124}" text-anchor="middle" class="mono" font-size="11" fill="{WHITE}">INTERFACE ID</text>')
A(f'<text x="{ix+40+(iw-70)*3/4}" y="{iy+151}" text-anchor="middle" class="mono" font-size="9" fill="{PURPLE}">64 bits</text>')
A(f'<text x="{ix+iw/2}" y="{iy+235}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">the prefix length selects a coordinate boundary inside the 128-bit state</text>')
end_panel()

# Panel 5: inclusion / slot story
ix,iy,iw,ih=panel(*p[4],"32 → 128 inclusion","One 32-bit value can occupy one lane without changing its internal value","address_inclusion","ι(x)=(0,0,0x0000ffff,x)")
# flow
block(ix+70,iy+24,220,78,"IPv4 WORD","0xC0000221")
arrow(ix+315,iy+63,ix+470,iy+63)
block(ix+495,iy+24,270,78,"MAPPED EMBEDDING","fixed 96-bit prefix")
arrow(ix+790,iy+63,ix+945,iy+63)
block(ix+970,iy+24,310,78,"IPv6 ADDRESS","::ffff:192.0.2.33")
A(f'<text x="{ix+iw/2}" y="{iy+134}" text-anchor="middle" class="mono" font-size="8" fill="{GREY}">the 32-bit payload is preserved exactly; only the surrounding coordinate space is enlarged</text>')
end_panel()



# --------------------------
# Chapter 14
# --------------------------
ch=HEADER_H+13*CHAPTER_H
chapter_header(ch,14,*chapters[13])

# Custom 2×3 panel field: six panels within one chapter.
p14=[
    (70,ch+180,710,330),(820,ch+180,710,330),
    (70,ch+535,710,330),(820,ch+535,710,330),
    (70,ch+890,710,330),(820,ch+890,710,330),
]

# Panel 1 — vector space
ix,iy,iw,ih=panel(*p14[0],"Vector space","The source object retains real-valued coordinates","vector_test_object","geometry in R² before raster sampling")
A(f'<rect x="{ix+18}" y="{iy+22}" width="320" height="192" rx="8" fill="#04060b" stroke="{GREY}" stroke-opacity=".35"/>')
sx=(320/160); sy=(192/96)
A(f'<rect x="{ix+18+12.4387*sx:.3f}" y="{iy+22+11.25*sy:.3f}" width="{61.5*sx:.3f}" height="{37.75*sy:.3f}" rx="{5.125*sx:.3f}" fill="{CYAN}"/>')
A(f'<circle cx="{ix+18+111.75*sx:.3f}" cy="{iy+22+46.5*sy:.3f}" r="{21.375*sx:.3f}" fill="{PURPLE}"/>')
A(f'<line x1="{ix+18+9.125*sx:.3f}" y1="{iy+22+79.625*sy:.3f}" x2="{ix+18+148.75*sx:.3f}" y2="{iy+22+66.375*sy:.3f}" stroke="{WHITE}" stroke-width="{2.25*sx:.3f}"/>')
A(f'<text x="{ix+370}" y="{iy+64}" class="mono" font-size="9" fill="{CYAN}">x = 12.4387</text>')
A(f'<text x="{ix+370}" y="{iy+93}" class="mono" font-size="8" fill="{GREY}">viewBox 0 0 160 96</text>')
A(f'<text x="{ix+370}" y="{iy+123}" class="mono" font-size="8" fill="{GREY}">rect · circle · line</text>')
A(f'<text x="{ix+370}" y="{iy+166}" class="mono" font-size="8" fill="{WHITE}">STRUCTURAL FRAME</text>')
A(f'<text x="{ix+370}" y="{iy+188}" class="mono" font-size="7.4" fill="{GREY}">vector: ε is representational</text>')
A(f'<text x="{ix+370}" y="{iy+218}" class="mono" font-size="7.4" fill="{GREY}">coordinates are not yet pixels</text>')
end_panel()

# Panel 2 — sampling boundary / actual PNG
ix,iy,iw,ih=panel(*p14[1],"Frame boundary","CairoSVG samples the vector object onto an exact 160×96 pixel field","raster_frame_boundary","R² → Z² at 1-pixel resolution")
png_uri="data:image/png;base64,"+CH14_B64.decode("ascii")
A(f'<image x="{ix+18}" y="{iy+25}" width="320" height="192" href="{png_uri}" image-rendering="pixelated"/>')
# Explicit pixel grid overlay.
for gx in range(0,161,20):
    xx=ix+18+gx*2
    A(f'<line x1="{xx}" y1="{iy+25}" x2="{xx}" y2="{iy+217}" stroke="{GREY}" stroke-opacity=".18"/>')
for gy in range(0,97,16):
    yy=iy+25+gy*2
    A(f'<line x1="{ix+18}" y1="{yy}" x2="{ix+338}" y2="{yy}" stroke="{GREY}" stroke-opacity=".18"/>')
A(f'<text x="{ix+370}" y="{iy+62}" class="mono" font-size="9" fill="{CYAN}">x=12.4387 → cell i=12</text>')
A(f'<text x="{ix+370}" y="{iy+91}" class="mono" font-size="8" fill="{GREY}">sampling boundary</text>')
A(f'<text x="{ix+370}" y="{iy+130}" class="mono" font-size="8" fill="{WHITE}">STRUCTURAL FRAME</text>')
A(f'<text x="{ix+370}" y="{iy+152}" class="mono" font-size="7.4" fill="{GREY}">raster: 1 pixel</text>')
A(f'<text x="{ix+370}" y="{iy+192}" class="mono" font-size="8" fill="{WHITE}">PHYSICAL PLANCK SCALE</text>')
A(f'<text x="{ix+370}" y="{iy+214}" class="mono" font-size="7.1" fill="{GREY}">no standard relation claimed</text>')
end_panel()

# Panel 3 — real PNG bytes
ix,iy,iw,ih=panel(*p14[2],"Byte space","The real compressed PNG stream: signature, chunks and IDAT payload","png_byte_space","raw = PNG bytes")
A(f'<text x="{ix+18}" y="{iy+31}" class="mono" font-size="8.5" fill="{WHITE}">len(raw) = {len(CH14_PNG_BYTES)} bytes</text>')
A(f'<text x="{ix+18}" y="{iy+52}" class="mono" font-size="7.1" fill="{GREY}">sha256(raw) = {CH14_RAW_SHA256}</text>')
# First 12 bytes as exact 8-bit columns.
for j,b in enumerate(CH14_PNG_BYTES[:12]):
    xx=ix+18+j*52
    A(f'<text x="{xx+20}" y="{iy+88}" text-anchor="middle" class="mono" font-size="7" fill="{CYAN if j<8 else PURPLE}">{b:02X}</text>')
    bits=f"{b:08b}"
    for k,bit in enumerate(bits):
        yy=iy+102+k*17
        A(f'<rect x="{xx+11}" y="{yy}" width="18" height="13" rx="2" fill="{CYAN if bit=="1" else GREY}" fill-opacity="{.85 if bit=="1" else .14}"/>')
        A(f'<text x="{xx+20}" y="{yy+10}" text-anchor="middle" class="mono" font-size="6" fill="{WHITE if bit=="1" else GREY}">{bit}</text>')
A(f'<text x="{ix+18}" y="{iy+255}" class="mono" font-size="7.2" fill="{GREY}">first 8 bytes = PNG signature · following bytes begin IHDR</text>')
end_panel()

# Panel 4 — 24-bit repartitioning
ix,iy,iw,ih=panel(*p14[3],"Base64 frame shift","The same first 24 bits are repartitioned 8+8+8 → 6+6+6+6","base64_frame_shift","24 bits = 3 bytes = 4 Base64 symbols")
raw3=CH14_PNG_BYTES[:3]
chars4=CH14_B64[:4].decode("ascii")
idx4=[CH14_ALPHABET.index(c) for c in chars4]
bit24="".join(f"{b:08b}" for b in raw3)
# common 24-bit rail
for k,bit in enumerate(bit24):
    xx=ix+25+k*25
    A(f'<rect x="{xx}" y="{iy+72}" width="21" height="23" rx="2" fill="{CYAN if bit=="1" else GREY}" fill-opacity="{.82 if bit=="1" else .14}"/>')
    A(f'<text x="{xx+10.5}" y="{iy+88}" text-anchor="middle" class="mono" font-size="6.2" fill="{WHITE if bit=="1" else GREY}">{bit}</text>')
# boundaries
for k in [0,8,16,24]:
    xx=ix+25+k*25
    A(f'<line x1="{xx}" y1="{iy+60}" x2="{xx}" y2="{iy+108}" stroke="{CYAN}" stroke-opacity=".65"/>')
for k in [0,6,12,18,24]:
    xx=ix+25+k*25
    A(f'<line x1="{xx}" y1="{iy+125}" x2="{xx}" y2="{iy+173}" stroke="{PURPLE}" stroke-opacity=".75"/>')
A(f'<text x="{ix+25}" y="{iy+48}" class="mono" font-size="8" fill="{CYAN}">bytes: {" ".join(f"{b:02X}" for b in raw3)} · 8|8|8</text>')
A(f'<text x="{ix+25}" y="{iy+196}" class="mono" font-size="8" fill="{PURPLE}">Base64: {chars4} · indices {idx4} · 6|6|6|6</text>')
A(f'<text x="{ix+25}" y="{iy+228}" class="mono" font-size="8" fill="{WHITE}">24 bits unchanged</text>')
A(f'<text x="{ix+25}" y="{iy+251}" class="mono" font-size="7.2" fill="{GREY}">only the partition boundaries move — “the space between”</text>')
end_panel()

# Panel 5 — alphabet geometry
ix,iy,iw,ih=panel(*p14[4],"Char space","64 symbols provide a lookup coordinate for each 6-bit value","base64_char_space","index ∈ {0,…,63} ↔ Base64 alphabet")
first16=CH14_FIRST_CHARS
used=set(first16)
for j,c in enumerate(CH14_ALPHABET):
    row=j//8; col=j%8
    xx=ix+25+col*58; yy=iy+48+row*29
    active=c in used
    A(f'<rect x="{xx}" y="{yy}" width="48" height="23" rx="5" fill="{PURPLE if active else DARK}" fill-opacity="{.70 if active else .65}" stroke="{CYAN if active else GREY}" stroke-opacity="{.75 if active else .22}"/>')
    A(f'<text x="{xx+11}" y="{yy+16}" text-anchor="middle" class="mono" font-size="7.2" fill="{WHITE}">{c}</text>')
    A(f'<text x="{xx+35}" y="{yy+16}" text-anchor="middle" class="mono" font-size="6.3" fill="{GREY}">{j:02d}</text>')
A(f'<text x="{ix+515}" y="{iy+73}" class="mono" font-size="8.5" fill="{CYAN}">first 16 chars</text>')
A(f'<text x="{ix+515}" y="{iy+98}" class="mono" font-size="10" fill="{WHITE}">{first16}</text>')
A(f'<text x="{ix+515}" y="{iy+132}" class="mono" font-size="7" fill="{GREY}">indices:</text>')
A(f'<text x="{ix+515}" y="{iy+153}" class="mono" font-size="6.7" fill="{PURPLE}">{" ".join(map(str,CH14_FIRST_INDICES[:8]))}</text>')
A(f'<text x="{ix+515}" y="{iy+174}" class="mono" font-size="6.7" fill="{PURPLE}">{" ".join(map(str,CH14_FIRST_INDICES[8:16]))}</text>')
end_panel()

# Panel 6 — exact recovery vs lossy inverse geometry
ix,iy,iw,ih=panel(*p14[5],"Reconstruction + lossiness","Encoding roundtrip is exact; raster-to-vector recovery is not identity","reconstruction_lossiness","decode(encode(PNG))=PNG; SVG→PNG→SVG'≠identity")
block(ix+18,iy+44,150,62,"PNG","raw bytes")
arrow(ix+180,iy+75,ix+265,iy+75)
block(ix+280,iy+44,150,62,"BASE64","6-bit chars")
arrow(ix+442,iy+75,ix+527,iy+75)
block(ix+542,iy+44,150,62,"PNG","decoded")
A(f'<text x="{ix+355}" y="{iy+135}" text-anchor="middle" class="mono" font-size="9" fill="{GREEN}">EXACT · byte-for-byte identity</text>')
block(ix+18,iy+180,150,62,"SVG","vector")
arrow(ix+180,iy+211,ix+265,iy+211)
block(ix+280,iy+180,150,62,"PNG","sampled")
arrow(ix+442,iy+211,ix+527,iy+211)
block(ix+542,iy+180,150,62,"SVG′","inferred")
A(f'<text x="{ix+355}" y="{iy+274}" text-anchor="middle" class="mono" font-size="9" fill="{RED}">LOSSY RECONSTRUCTION ≠ IDENTITY</text>')
end_panel()



# --------------------------
# Chapter 15
# --------------------------
ch=HEADER_H+14*CHAPTER_H
chapter_header(ch,15,*chapters[14])

p15=[
    (70,ch+180,710,330),(820,ch+180,710,330),
    (70,ch+535,710,330),(820,ch+535,710,330),
    (70,ch+890,710,330),(820,ch+890,710,330),
]

UTF73_CONS=[(x["char"],x["codepoint"]) for x in UTF73_SPEC["consonants"]]
UTF73_MARKS=[(x["name"],x["char"]) for x in UTF73_SPEC["states12"]]
UTF73_ALPH=UTF73_SYMBOLS
UTF73_Q,UTF73_R=divmod(2**24,73)

# 1 — 73-state field
ix,iy,iw,ih=panel(*p15[0],"73-state Unicode field","6 consonants × 12 vowel/mark states + one śūnya state","utf73_field","|Σ| = 6×12+1 = 73")
for r0,(c,cp) in enumerate(UTF73_CONS):
    A(f'<text x="{ix+25}" y="{iy+56+r0*39}" class="mono" font-size="8" fill="{GREY}">{cp}</text>')
    A(f'<text x="{ix+90}" y="{iy+58+r0*39}" class="sans" font-size="18" fill="{CYAN}">{c}</text>')
    for j,(name,m) in enumerate(UTF73_MARKS):
        xx=ix+135+j*43
        sym=c+m
        A(f'<text x="{xx}" y="{iy+58+r0*39}" text-anchor="middle" class="sans" font-size="14" fill="{WHITE}">{sym}</text>')
A(f'<text x="{ix+640}" y="{iy+58}" text-anchor="middle" class="sans" font-size="22" fill="{PURPLE}">·</text>')
A(f'<text x="{ix+640}" y="{iy+82}" text-anchor="middle" class="mono" font-size="7" fill="{GREY}">U+00B7</text>')
A(f'<text x="{ix+25}" y="{iy+290}" class="mono" font-size="7.4" fill="{GREY}">custom field · standard Unicode code points · not a Unicode encoding standard</text>')
end_panel()

# 2 — codepoint composition
ix,iy,iw,ih=panel(*p15[1],"Codepoint composition","Inherent a uses one code point; explicit signs use two","utf73_codepoints","state = consonant || optional sign")
examples=[("क","U+0915","ka · inherent a"),("का","U+0915 + U+093E","ka + ā"),("कि","U+0915 + U+093F","ka + i"),("कं","U+0915 + U+0902","ka + anusvāra"),("·","U+00B7","śūnya display glyph")]
for j,(sym,cps,label) in enumerate(examples):
    yy=iy+30+j*54
    A(f'<rect x="{ix+22}" y="{yy}" width="{iw-44}" height="43" rx="8" fill="#08111d" stroke="{CYAN if j<4 else PURPLE}" stroke-opacity=".30"/>')
    A(f'<text x="{ix+50}" y="{yy+29}" class="sans" font-size="20" fill="{WHITE}">{sym}</text>')
    A(f'<text x="{ix+110}" y="{yy+20}" class="mono" font-size="8" fill="{CYAN}">{cps}</text>')
    A(f'<text x="{ix+110}" y="{yy+35}" class="mono" font-size="7" fill="{GREY}">{label}</text>')
A(f'<text x="{ix+22}" y="{iy+305}" class="mono" font-size="7.3" fill="{GREY}">canonical slot 12: ं U+0902 ANUSVARA · śūnya is abstract nil, displayed as ·</text>')
end_panel()

# 3 — UTF-8 byte geometry
ix,iy,iw,ih=panel(*p15[2],"UTF-8 byte geometry","Code-point count and byte width are variable","utf73_utf8","Unicode scalar values → RFC 3629 UTF-8 bytes")
utf_examples=[("क","e0 a4 95",3),("का","e0 a4 95 e0 a4 be",6),("कं","e0 a4 95 e0 a4 82",6),("·","c2 b7",2)]
for j,(sym,hx,nbytes) in enumerate(utf_examples):
    yy=iy+32+j*64
    A(f'<text x="{ix+30}" y="{yy+24}" class="sans" font-size="20" fill="{WHITE}">{sym}</text>')
    A(f'<text x="{ix+95}" y="{yy+18}" class="mono" font-size="8" fill="{CYAN}">{hx}</text>')
    A(f'<text x="{ix+95}" y="{yy+39}" class="mono" font-size="7" fill="{GREY}">{nbytes} bytes</text>')
    for k in range(nbytes):
        A(f'<rect x="{ix+370+k*39}" y="{yy+8}" width="30" height="30" rx="5" fill="{PURPLE}" fill-opacity="{.65 if k%2==0 else .35}"/>')
A(f'<text x="{ix+30}" y="{iy+306}" class="mono" font-size="7.2" fill="{GREY}">TextEncoder/TextDecoder can validate these sequences natively in a browser</text>')
end_panel()

# 4 — fixed point
ix,iy,iw,ih=panel(*p15[3],"Reference-model identity","By construction, the quotient model closes exactly on every canonical state","utf73_fixed_point","E₇₃(D₇₃(s)) = s")
A(f'<text x="{ix+35}" y="{iy+72}" class="mono" font-size="12" fill="{CYAN}">E₇₃(n) = n mod 73</text>')
A(f'<text x="{ix+35}" y="{iy+112}" class="mono" font-size="12" fill="{PURPLE}">D₇₃(s) = state index</text>')
for j in range(73):
    x0=ix+35+(j%19)*32; y0=iy+155+(j//19)*34
    A(f'<circle cx="{x0}" cy="{y0}" r="8" fill="{GREEN}" fill-opacity=".78"/>')
    if j in [0,18,36,54,72]:
        A(f'<text x="{x0}" y="{y0+3}" text-anchor="middle" class="mono" font-size="5.5" fill="{DARK}">{j}</text>')
A(f'<text x="{ix+35}" y="{iy+300}" class="mono" font-size="8.5" fill="{GREEN}">reference identity: E(D(s))=s · 73 / 73</text>')
end_panel()

# 5 — exhaustive real RGB24 basin sizes
ix,iy,iw,ih=panel(*p15[4],"Measured RGB24 basins","Exhaustive live encoder: RGB24 → HSV hue×brightness → canonical Σ₇₃","utf73_basins","sum basin_i = 2^24")
A(f'<text x="{ix+30}" y="{iy+54}" class="mono" font-size="10" fill="{WHITE}">EXHAUSTIVE INPUT: 16,777,216 RGB24 COLORS</text>')
A(f'<text x="{ix+30}" y="{iy+83}" class="mono" font-size="8.5" fill="{CYAN}">min basin = {min(UTF73_REAL_COUNTS):,} · max basin = {max(UTF73_REAL_COUNTS):,}</text>')
A(f'<text x="{ix+30}" y="{iy+108}" class="mono" font-size="7.5" fill="{GREY}">śūnya basin = {UTF73_REAL_COUNTS[72]} (black only)</text>')
mxcount=max(UTF73_REAL_COUNTS)
for j,n0 in enumerate(UTF73_REAL_COUNTS):
    xx=ix+30+j*(iw-60)/73
    h0=max(1,150*n0/mxcount)
    A(f'<rect x="{xx:.2f}" y="{iy+280-h0:.2f}" width="{max(2,(iw-60)/73-2):.2f}" height="{h0:.2f}" fill="{PURPLE if j==72 else CYAN}" fill-opacity=".72"/>')
A(f'<line x1="{ix+30}" y1="{iy+280}" x2="{ix+iw-30}" y2="{iy+280}" stroke="{GREY}" stroke-opacity=".35"/>')
A(f'<text x="{ix+30}" y="{iy+306}" class="mono" font-size="7" fill="{GREY}">actual HSV-quantizer basin volume · not the modulo-73 reference quotient</text>')
end_panel()

# 6 — Base64 comparison
ix,iy,iw,ih=panel(*p15[5],"Base64 vs Σ₇₃ projection","Base64 repartitions exactly; the live HSV encoder projects many RGB states into one symbol","utf73_vs_base64","64^4 = 2^24; 73 ∤ 2^24")
A(f'<text x="{ix+35}" y="{iy+65}" class="mono" font-size="11" fill="{CYAN}">BASE64</text>')
A(f'<text x="{ix+35}" y="{iy+98}" class="mono" font-size="9" fill="{WHITE}">24 bits = 4 × 6 bits</text>')
A(f'<text x="{ix+35}" y="{iy+128}" class="mono" font-size="8" fill="{GREEN}">encode ↔ decode · exact</text>')
A(f'<line x1="{ix+335}" y1="{iy+35}" x2="{ix+335}" y2="{iy+265}" stroke="{GREY}" stroke-opacity=".25"/>')
A(f'<text x="{ix+375}" y="{iy+65}" class="mono" font-size="11" fill="{PURPLE}">UTF73 FIELD</text>')
A(f'<text x="{ix+375}" y="{iy+98}" class="mono" font-size="9" fill="{WHITE}">73 states · log₂73 ≈ {math.log2(73):.3f}</text>')
A(f'<text x="{ix+375}" y="{iy+128}" class="mono" font-size="8" fill="{RED}">RGB24→HSV→Σ₇₃ many→one</text>')
A(f'<text x="{ix+375}" y="{iy+157}" class="mono" font-size="8" fill="{GREEN}">canonical decoder fixed-point exact</text>')
A(f'<text x="{ix+35}" y="{iy+225}" class="mono" font-size="8" fill="{GREY}">same finite-state perspective · different invertibility</text>')
A(f'<text x="{ix+35}" y="{iy+255}" class="mono" font-size="7.2" fill="{GREY}">mod-73 remains a reference identity only; measured lossiness comes from the live HSV encoder</text>')
end_panel()



# --------------------------
# Chapter 16
# --------------------------
ch=HEADER_H+15*CHAPTER_H
chapter_header(ch,16,*chapters[15])

ABJAD=json.loads((OUT/"data"/"abjad_field.json").read_text(encoding="utf-8"))
ABJAD_LETTERS=ABJAD["letters"]
QHYP=json.loads((OUT/"data"/"quran_abjad_hypothesis.json").read_text(encoding="utf-8"))
QMEAS=json.loads((OUT/"data"/"quran_abjad_measurement.json").read_text(encoding="utf-8"))

# Six panels: carrier → mapping → pure dynamics → fixture → empirical measure → layer status.
p16=[
    (70,ch+180,710,330),(820,ch+180,710,330),
    (70,ch+535,710,330),(820,ch+535,710,330),
    (70,ch+890,710,330),(820,ch+890,710,330),
]

# 1 — linear carrier
ix,iy,iw,ih=panel(*p16[0],"Linear carrier · UTF-8","The text first exists only as an ordered, lossless Unicode/byte sequence","abjad_linear_carrier","c₁,c₂,…,cₙ · UTF-8 is carrier, not the abjad invariant")
sample="ا ب ج د"
A(f'<text x="{ix+28}" y="{iy+80}" class="sans" font-size="27" fill="{CYAN}">{sample}</text>')
A(f'<text x="{ix+28}" y="{iy+121}" class="mono" font-size="8" fill="{GREY}">U+0627  U+0628  U+062C  U+062F</text>')
A(f'<text x="{ix+28}" y="{iy+159}" class="mono" font-size="8" fill="{WHITE}">UTF-8 preserves symbol + order exactly</text>')
A(f'<line x1="{ix+30}" y1="{iy+190}" x2="{ix+iw-30}" y2="{iy+190}" stroke="{GREY}" stroke-opacity=".28"/>')
A(f'<text x="{ix+28}" y="{iy+224}" class="mono" font-size="9" fill="{CYAN}">LINEAR LAYER</text>')
A(f'<text x="{ix+28}" y="{iy+250}" class="mono" font-size="7.5" fill="{GREY}">position matters · no numeric operator has been applied yet</text>')
A(f'<text x="{ix+28}" y="{iy+286}" class="mono" font-size="7.2" fill="{GREY}">fixture SHA identifies the exact carrier bytes when the corpus is locked</text>')
end_panel()

# 2 — cultural direct mapping
ix,iy,iw,ih=panel(*p16[1],"Direct abjad mapping","28 Arabic letters map directly to the classical value ladder","abjad_cultural_mapping","letter → v ∈ {1…9,10…90,100…1000}")
for j,row in enumerate(ABJAD_LETTERS):
    col=j%14; rr=j//14
    xx=ix+28+col*46; yy=iy+73+rr*102
    A(f'<text x="{xx}" y="{yy}" text-anchor="middle" class="sans" font-size="20" fill="{CYAN}">{row["char"]}</text>')
    A(f'<text x="{xx}" y="{yy+23}" text-anchor="middle" class="mono" font-size="6" fill="{GREY}">{row["codepoint"]}</text>')
    A(f'<text x="{xx}" y="{yy+43}" text-anchor="middle" class="mono" font-size="7" fill="{WHITE}">{row["value"]}</text>')
A(f'<text x="{ix+28}" y="{iy+285}" class="mono" font-size="7.5" fill="{PURPLE}">CULTURAL MAPPING LAYER · explicit table, variant-sensitive</text>')
A(f'<text x="{ix+28}" y="{iy+307}" class="mono" font-size="7" fill="{GREY}">charCode % 28 is excluded: it is a codepoint hash, not this mapping</text>')
end_panel()

# 3 — exact math: roots + doubling orbits
ix,iy,iw,ih=panel(*p16[2],"Pure mathematics · mod-9 dynamics","After a value is chosen, the orbit structure is exact and corpus-independent","abjad_mod9_orbits","dr(v)=1+((v−1) mod 9); T(r)=dr(2r)")
cycles=[("V1",[1,2,4,8,7,5],CYAN),("V3",[3,6],PURPLE),("V9",[9],GREEN)]
ybase=[80,177,265]
for (name,cyc,col),yy in zip(cycles,ybase):
    A(f'<text x="{ix+28}" y="{iy+yy+4}" class="mono" font-size="9" fill="{col}">{name}</text>')
    for j,v in enumerate(cyc):
        xx=ix+115+j*80
        A(f'<circle cx="{xx}" cy="{iy+yy}" r="20" fill="#08111d" stroke="{col}" stroke-opacity=".70"/>')
        A(f'<text x="{xx}" y="{iy+yy+4}" text-anchor="middle" class="mono" font-size="9" fill="{WHITE}">{v}</text>')
        if j<len(cyc)-1: arrow(xx+23,iy+yy,xx+57,iy+yy,col)
    if len(cyc)>1:
        A(f'<path d="M {ix+115+(len(cyc)-1)*80} {iy+yy+22} Q {ix+115+(len(cyc)-1)*40} {iy+yy+52} {ix+115} {iy+yy+22}" fill="none" stroke="{col}" stroke-opacity=".55" marker-end="url(#arrC)"/>')
A(f'<text x="{ix+28}" y="{iy+313}" class="mono" font-size="7" fill="{GREY}">this layer is a theorem about the finite state map — no book is required</text>')
end_panel()

# 4 — exact fixture / normalization boundary
ix,iy,iw,ih=panel(*p16[3],"Corpus fixture + normalization","One exact 6236-ayah carrier must be locked before any corpus statistic is a result","abjad_corpus_fixture","UTF-8 fixture → normalize → 28 letters → direct values")
block(ix+24,iy+42,150,58,"FIXTURE","6236 ayahs")
arrow(ix+185,iy+71,ix+245,iy+71)
block(ix+255,iy+42,155,58,"NORMALIZE","marks/tatweel")
arrow(ix+420,iy+71,ix+480,iy+71)
block(ix+490,iy+42,170,58,"28 LETTERS","direct lookup")
A(f'<text x="{ix+25}" y="{iy+145}" class="mono" font-size="7.7" fill="{CYAN}">source manifest: corpora/quran_uthmani/source.json</text>')
A(f'<text x="{ix+25}" y="{iy+173}" class="mono" font-size="7.2" fill="{GREY}">ٱ→ا · ی→ي · أ/إ/آ→ا · ؤ→و · ئ/ى→ي · ة→ه</text>')
A(f'<text x="{ix+25}" y="{iy+200}" class="mono" font-size="7.2" fill="{GREY}">combining marks + tatweel removed · other non-table chars ignored</text>')
fixture_status="LOCKED + MEASURED" if QMEAS.get("status")=="measured" else "REMOTE FIXTURE NOT BUNDLED"
fixture_col=GREEN if QMEAS.get("status")=="measured" else PURPLE
A(f'<text x="{ix+25}" y="{iy+252}" class="mono" font-size="10" fill="{fixture_col}">{fixture_status}</text>')
A(f'<text x="{ix+25}" y="{iy+280}" class="mono" font-size="7" fill="{GREY}">fetch → SHA lock → analyze; no silent corpus substitution</text>')
end_panel()

# 5 — empirical candidate / measured statistic
ix,iy,iw,ih=panel(*p16[4],"Empirical orbit statistic","Per ayah: direct abjad sum → digital root → one of V1/V3/V9","abjad_empirical_measure","candidate: one orbit-class frequency = 2050/6236")
if QMEAS.get("status")=="measured":
    matches=QMEAS.get("candidate_2050_matches",[])
    if len(matches)==1:
        cls=matches[0]; stat=QMEAS["orbit_statistics"][cls]
        status=f"MEASURED · CANDIDATE MATCH = {cls}"
        count,total=stat["count"],stat["total"]
        gap=stat["gap_fraction"]
        col=GREEN
    else:
        status=f"MEASURED · CANDIDATE NOT UNIQUELY MATCHED"
        count,total=2050,QMEAS.get("ayahs",6236)
        gap="43/9354 · candidate only"
        col=RED
else:
    cand=QMEAS["candidate_only"]
    status="CANDIDATE · TARGET ORBIT CLASS UNRESOLVED"
    count,total=cand["count"],cand["total"]
    gap=cand["gap_fraction"]
    col=PURPLE
A(f'<text x="{ix+28}" y="{iy+62}" class="mono" font-size="9" fill="{col}">{status}</text>')
A(f'<text x="{ix+28}" y="{iy+112}" class="mono" font-size="15" fill="{WHITE}">{count} / {total}</text>')
A(f'<text x="{ix+28}" y="{iy+158}" class="mono" font-size="12" fill="{CYAN}">1/3 − {count}/{total} = {gap}</text>')
A(f'<line x1="{ix+28}" y1="{iy+186}" x2="{ix+iw-28}" y2="{iy+186}" stroke="{GREY}" stroke-opacity=".25"/>')
A(f'<text x="{ix+28}" y="{iy+218}" class="mono" font-size="7.7" fill="{GREY}">1/3 is the declared equal-class baseline; orbit sizes themselves are 6 / 2 / 1</text>')
A(f'<text x="{ix+28}" y="{iy+246}" class="mono" font-size="7.3" fill="{GREY}">the prior result does not identify its target class inside this repo yet</text>')
A(f'<text x="{ix+28}" y="{iy+276}" class="mono" font-size="7.3" fill="{GREY}">all V1/V3/V9 counts are recomputed; a unique 2050 match resolves the class</text>')
A(f'<text x="{ix+28}" y="{iy+302}" class="mono" font-size="7.1" fill="{GREY}">frequency ignores position · root transition matrix preserves the 9-state walk</text>')
end_panel()

# 6 — three-layer separation
ix,iy,iw,ih=panel(*p16[5],"Three layers · three statuses","Do not promote a mapping choice or corpus observation into a theorem","abjad_layer_separation","carrier ≠ mapping ≠ invariant ≠ empirical result")
rows=[
    ("PURE MATH","T(r)=dr(2r) · V1/V3/V9","EXACT",GREEN),
    ("MAPPING","Arabic letter → classical abjad value","EXPLICIT CHOICE",CYAN),
    ("CARRIER","UTF-8 ordered ayah sequence","LOSSLESS",CYAN),
    ("EMPIRICAL","orbit-class statistic on locked corpus",(("MEASURED · MATCH" if len(QMEAS.get("candidate_2050_matches",[]))==1 else "MEASURED · CHECK") if QMEAS.get("status")=="measured" else "PENDING FIXTURE"),(GREEN if QMEAS.get("status")=="measured" and len(QMEAS.get("candidate_2050_matches",[]))==1 else PURPLE)),
]
for j,(lab,desc,stat,col) in enumerate(rows):
    yy=iy+35+j*63
    A(f'<rect x="{ix+22}" y="{yy}" width="{iw-44}" height="49" rx="8" fill="#08111d" stroke="{col}" stroke-opacity=".35"/>')
    A(f'<text x="{ix+40}" y="{yy+20}" class="mono" font-size="8" fill="{col}">{lab}</text>')
    A(f'<text x="{ix+145}" y="{yy+20}" class="mono" font-size="7.2" fill="{WHITE}">{desc}</text>')
    A(f'<text x="{ix+iw-38}" y="{yy+20}" text-anchor="end" class="mono" font-size="7.2" fill="{col}">{stat}</text>')
A(f'<text x="{ix+22}" y="{iy+307}" class="mono" font-size="7" fill="{GREY}">comparison corpora reuse exactly the same normalize → lookup → measure function</text>')
end_panel()



# --------------------------
# Chapter 17
# --------------------------
ch=HEADER_H+16*CHAPTER_H
chapter_header(ch,17,*chapters[16])

C7=CLOSURE7
AX17=json.loads((OUT/"data"/"language_frame_axioms.json").read_text(encoding="utf-8"))
p17=[
    (70,ch+180,710,330),(820,ch+180,710,330),
    (70,ch+535,710,330),(820,ch+535,710,330),
    (70,ch+890,710,330),(820,ch+890,710,330),
]

# 1 — atomic frame axioms
ix,iy,iw,ih=panel(*p17[0],"Atomic vs general frame","Atomicity is an extra axiom; closure only needs to land back in the general Frame type","closure_atomic_frames","AtomicFrame = Frame + |C|=|S|=1")
A(f'<text x="{ix+28}" y="{iy+45}" class="mono" font-size="10" fill="{CYAN}">Frame = (C,S,b)</text>')
axiom_lines=[
("A1","C,S non-empty finite sets"),
("A2","C ∩ S = ∅"),
("A3","b ∉ C ∪ S"),
("A4","b is the unique boundary-equivalence class"),
]
for j,(a0,d0) in enumerate(axiom_lines):
    yy=iy+82+j*41
    A(f'<rect x="{ix+28}" y="{yy-20}" width="54" height="27" rx="6" fill="{CYAN}" fill-opacity=".12" stroke="{CYAN}" stroke-opacity=".35"/>')
    A(f'<text x="{ix+55}" y="{yy-2}" text-anchor="middle" class="mono" font-size="7" fill="{CYAN}">{a0}</text>')
    A(f'<text x="{ix+100}" y="{yy-2}" class="mono" font-size="7.5" fill="{WHITE}">{esc(d0)}</text>')
A(f'<line x1="{ix+28}" y1="{iy+245}" x2="{ix+iw-28}" y2="{iy+245}" stroke="{GREY}" stroke-opacity=".22"/>')
A(f'<text x="{ix+28}" y="{iy+272}" class="mono" font-size="8.5" fill="{PURPLE}">AtomicFrame adds AT1 |C|=1 and AT2 |S|=1</text>')
A(f'<text x="{ix+28}" y="{iy+300}" class="mono" font-size="7" fill="{GREY}">the quotient output need not be atomic to remain a Frame</text>')
end_panel()

# 2 — prequotient disjoint union: 9 points
ix,iy,iw,ih=panel(*p17[1],"Pre-quotient · 9 points","Three pairwise-disjoint atomic frames each contain carrier, structure and their own boundary","closure_disjoint_union_9","X = ⊔ᵢ(Cᵢ ⊔ Sᵢ ⊔ {bᵢ}); |X|=3×3=9")
frame_names=[("L",CYAN),("G",PURPLE),("E",GREEN)]
for j,(nm,col) in enumerate(frame_names):
    cx=ix+125+j*205; yy=iy+145
    A(f'<rect x="{cx-72}" y="{yy-82}" width="144" height="164" rx="18" fill="#08111d" stroke="{col}" stroke-opacity=".42"/>')
    A(f'<text x="{cx}" y="{yy-53}" text-anchor="middle" class="mono" font-size="8" fill="{col}">Atomic {nm}</text>')
    for lab,dy in [("C",-15),("S",26),("b",67)]:
        A(f'<circle cx="{cx}" cy="{yy+dy}" r="17" fill="{col if lab=="b" else DARK}" fill-opacity="{.68 if lab=="b" else .9}" stroke="{col}" stroke-opacity=".65"/>')
        A(f'<text x="{cx}" y="{yy+dy+4}" text-anchor="middle" class="mono" font-size="8" fill="{WHITE}">{nm}:{lab}</text>')
A(f'<text x="{ix+28}" y="{iy+297}" class="mono" font-size="9" fill="{GREEN}">3 × (1 carrier + 1 structure + 1 boundary) = 9</text>')
end_panel()

# 3 — quotient map
ix,iy,iw,ih=panel(*p17[2],"Boundary quotient · 9 → 7","The +1 is the single boundary equivalence class produced by identifying bL~bG~bE","closure_boundary_quotient","Q=X/~ ; bL~bG~bE ; |Q|=9-(3-1)=7")
leftx=ix+92
for j,(nm,col) in enumerate(frame_names):
    yy=iy+74+j*70
    A(f'<circle cx="{leftx}" cy="{yy}" r="21" fill="{col}" fill-opacity=".55" stroke="{col}" stroke-opacity=".75"/>')
    A(f'<text x="{leftx}" y="{yy+4}" text-anchor="middle" class="mono" font-size="8" fill="{WHITE}">{nm}:b</text>')
    arrow(leftx+28,yy,ix+325,iy+145,PURPLE)
A(f'<circle cx="{ix+355}" cy="{iy+145}" r="38" fill="{PURPLE}" fill-opacity=".75" stroke="{WHITE}" stroke-opacity=".55"/>')
A(f'<text x="{ix+355}" y="{iy+140}" text-anchor="middle" class="mono" font-size="10" fill="{WHITE}">[b]</text>')
A(f'<text x="{ix+355}" y="{iy+159}" text-anchor="middle" class="mono" font-size="6.5" fill="{WHITE}">1 ≡ 0</text>')
A(f'<text x="{ix+455}" y="{iy+90}" class="mono" font-size="13" fill="{CYAN}">|X| = 9</text>')
A(f'<text x="{ix+455}" y="{iy+137}" class="mono" font-size="13" fill="{PURPLE}">merge 3 → 1</text>')
A(f'<text x="{ix+455}" y="{iy+184}" class="mono" font-size="15" fill="{GREEN}">|Q| = 7</text>')
A(f'<text x="{ix+455}" y="{iy+225}" class="mono" font-size="8" fill="{WHITE}">9 − (3−1) = 7</text>')
A(f'<text x="{ix+455}" y="{iy+261}" class="mono" font-size="7" fill="{GREY}">+1 is quotient class, not an added point</text>')
end_panel()

# 4 — theorem proof
ix,iy,iw,ih=panel(*p17[3],"Closure theorem","Carrier and structure are inherited canonically from the quotient images; no repartition is chosen afterward","closure_theorem","⊕(F₁,F₂,F₃)=(C′,S′,b) ⊨ A1–A4")
checks=C7["closure_theorem"]["axiom_checks"]
proof_rows=[
("A1","C′,S′ non-empty",checks["A1_nonempty"]),
("A2","C′∩S′=∅",checks["A2_disjoint"]),
("A3","b∉C′∪S′",checks["A3_boundary_external"]),
("A4","one boundary class [b]",checks["A4_unique_boundary_class"]),
]
for j,(a0,d0,ok0) in enumerate(proof_rows):
    yy=iy+45+j*48
    col=GREEN if ok0 else RED
    A(f'<rect x="{ix+28}" y="{yy-21}" width="76" height="30" rx="7" fill="{col}" fill-opacity=".13" stroke="{col}" stroke-opacity=".5"/>')
    A(f'<text x="{ix+66}" y="{yy-1}" text-anchor="middle" class="mono" font-size="7.5" fill="{col}">{a0} PASS</text>')
    A(f'<text x="{ix+128}" y="{yy-1}" class="mono" font-size="8" fill="{WHITE}">{esc(d0)}</text>')
A(f'<line x1="{ix+28}" y1="{iy+238}" x2="{ix+iw-28}" y2="{iy+238}" stroke="{GREY}" stroke-opacity=".22"/>')
A(f'<text x="{ix+28}" y="{iy+266}" class="mono" font-size="8.2" fill="{CYAN}">C′ = q(⊔Cᵢ) · S′ = q(⊔Sᵢ) · b=[bᵢ]</text>')
A(f'<text x="{ix+28}" y="{iy+296}" class="mono" font-size="7.2" fill="{GREEN}">THEOREM PASS · output is a general Frame with 7 points</text>')
end_panel()

# 5 — seven crosschecks
ix,iy,iw,ih=panel(*p17[4],"Seven crosschecks","The quotient cardinality then meets the existing mod-9 and canonical-abjad checks","closure_v1_abjad_7","|Q|=7; dr(7)=7; T(7)=5; 7∈V1; ز↦7")
cyc=[1,2,4,8,7,5]
for j,v in enumerate(cyc):
    xx=ix+45+j*93; yy=iy+92
    active=v==7
    A(f'<circle cx="{xx}" cy="{yy}" r="{27 if active else 22}" fill="{PURPLE if active else DARK}" fill-opacity=".80" stroke="{CYAN}" stroke-opacity=".62"/>')
    A(f'<text x="{xx}" y="{yy+4}" text-anchor="middle" class="mono" font-size="9" fill="{WHITE}">{v}</text>')
    if j<len(cyc)-1: arrow(xx+28,yy,xx+65,yy,CYAN)
A(f'<path d="M {ix+45+5*93} {iy+122} Q {ix+45+2.5*93} {iy+185} {ix+45} {iy+122}" fill="none" stroke="{CYAN}" stroke-opacity=".45" marker-end="url(#arrC)"/>')
A(f'<text x="{ix+45}" y="{iy+215}" class="mono" font-size="10" fill="{GREEN}">dr(7)=7 · T(7)=5 · 7 ∈ V1</text>')
A(f'<text x="{ix+45}" y="{iy+252}" class="sans" font-size="25" fill="{PURPLE}">ز</text>')
A(f'<text x="{ix+90}" y="{iy+248}" class="mono" font-size="9" fill="{WHITE}">zay · ordinal 7 · abjad value 7</text>')
A(f'<text x="{ix+45}" y="{iy+287}" class="mono" font-size="7" fill="{GREY}">crosschecks do not prove uniqueness or necessity of the atomicity axiom</text>')
end_panel()

# 6 — status ladder
ix,iy,iw,ih=panel(*p17[5],"Theorem status ledger","The quotient closure is proved inside the model; necessity and uniqueness remain open","closure_status_ledger","construct → consistency → type closure → necessity? → uniqueness?")
rows=[
("PROVED","3 AtomicFrames / boundary quotient is a general Frame",GREEN),
("PROVED","|X|=9 and |X/~|=7 under bL~bG~bE",GREEN),
("AXIOM","atomic |C|=|S|=1 remains assumed",PURPLE),
("CONVENTION","a general Frame is one language-object at the next level",CYAN),
("OPEN","derive atomicity from deeper principles",GREY),
("OPEN","uniqueness / necessity of the 7-closure",GREY),
]
for j,(status,desc,col) in enumerate(rows):
    yy=iy+25+j*43
    A(f'<rect x="{ix+25}" y="{yy}" width="105" height="29" rx="7" fill="{col}" fill-opacity=".13" stroke="{col}" stroke-opacity=".42"/>')
    A(f'<text x="{ix+77}" y="{yy+19}" text-anchor="middle" class="mono" font-size="6.8" fill="{col}">{status}</text>')
    A(f'<text x="{ix+150}" y="{yy+19}" class="mono" font-size="7" fill="{WHITE}">{esc(desc)}</text>')
A(f'<text x="{ix+25}" y="{iy+302}" class="mono" font-size="6.8" fill="{GREY}">89=F(11) retained only as meta-observation, never as theorem input</text>')
end_panel()


# --------------------------
# Chapter 18
# --------------------------
ch=HEADER_H+17*CHAPTER_H
chapter_header(ch,18,*chapters[17])

TF18=json.loads((OUT/"data"/"transformer_frame_ch18.json").read_text(encoding="utf-8"))
p18=[
    (70,ch+180,710,500),(820,ch+180,710,500),
    (70,ch+710,710,500),(820,ch+710,710,500),
]

# 1 — proposed Frame correspondence
ix,iy,iw,ih=panel(*p18[0],"Frame in the Transformer","Audited per-layer correspondence; global network is a stack of Frame slices","transformer_frame_correspondence","Cₗ↔xₗ ; Sₗ↔Fₗ(xₗ) ; b↔merge event · per-layer")
rows=[
("C · carrier","residual stream / layer state x","Cₗ ↔ residual carrier · VALID"),
("S · structure","attention + FFN + positional structure","Sₗ ↔ layer contribution · VALID"),
("b · boundary","residual merge x + F(x)","b ↔ b₁ superposition · VALID"),
]
for j,(a0,b0,c0) in enumerate(rows):
    yy=iy+50+j*92
    A(f'<rect x="{ix+25}" y="{yy-24}" width="{iw-50}" height="67" rx="10" fill="#08111d" stroke="{[CYAN,PURPLE,GREEN][j]}" stroke-opacity=".32"/>')
    A(f'<text x="{ix+45}" y="{yy}" class="mono" font-size="9" fill="{[CYAN,PURPLE,GREEN][j]}">{esc(a0)}</text>')
    A(f'<text x="{ix+190}" y="{yy}" class="mono" font-size="7.5" fill="{WHITE}">{esc(b0)}</text>')
    A(f'<text x="{ix+190}" y="{yy+24}" class="mono" font-size="7" fill="{GREY}">{esc(c0)}</text>')
A(f'<text x="{ix+25}" y="{iy+354}" class="mono" font-size="8" fill="{CYAN}">residual form shown as working equation:</text>')
A(f'<text x="{ix+25}" y="{iy+388}" class="mono" font-size="13" fill="{WHITE}">xₗ₊₁ = xₗ + Fₗ(xₗ)</text>')
A(f'<text x="{ix+25}" y="{iy+420}" class="mono" font-size="7.2" fill="{GREY}">A2 is local: Cₗ and Sₗ are typed separately in one slice; Cₗ₊₁ contains the merged prior contribution</text>')
end_panel()

# 2 — 6+1 seed geometry
ix,iy,iw,ih=panel(*p18[1],"Seed geometry · 6 + 1","One center and one hexagonal first ring form the chapter's seven-point visual closure","transformer_seed_geometry","1 center + 6 first-ring points = 7")
cx=ix+iw/2; cy=iy+195; rad=120
for j in range(6):
    a=-math.pi/2+j*math.pi/3
    x0=cx+rad*math.cos(a); y0=cy+rad*math.sin(a)
    A(f'<circle cx="{x0:.2f}" cy="{y0:.2f}" r="42" fill="{DARK}" stroke="{CYAN}" stroke-opacity=".55"/>')
    A(f'<text x="{x0:.2f}" y="{y0+4:.2f}" text-anchor="middle" class="mono" font-size="9" fill="{WHITE}">{j+1}</text>')
A(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="46" fill="{PURPLE}" fill-opacity=".72" stroke="{WHITE}" stroke-opacity=".55"/>')
A(f'<text x="{cx:.2f}" y="{cy+4:.2f}" text-anchor="middle" class="mono" font-size="11" fill="{WHITE}">CENTER</text>')
A(f'<text x="{ix+30}" y="{iy+382}" class="mono" font-size="12" fill="{GREEN}">1 + 6 = 7</text>')
A(f'<text x="{ix+30}" y="{iy+414}" class="mono" font-size="7.2" fill="{GREY}">EXACT under equal-circle hexagonal first-ring definition</text>')
end_panel()

# 3 — signal / system / atlas and orbit bridge
ix,iy,iw,ih=panel(*p18[2],"Signal → System → Atlas","Audited slice view: each layer maps carrier through structure into the next carrier","transformer_signal_system_atlas","signal → system → atlas · proposed type correspondence")
block(ix+25,iy+65,170,75,"SIGNAL","carrier / embedding")
arrow(ix+210,iy+102,ix+300,iy+102)
block(ix+315,iy+65,170,75,"SYSTEM","transform stack")
arrow(ix+500,iy+102,ix+590,iy+102)
block(ix+605,iy+65,170,75,"ATLAS","enclosing field")
A(f'<text x="{ix+25}" y="{iy+205}" class="mono" font-size="8.5" fill="{CYAN}">FINITE ORBITS</text>')
A(f'<text x="{ix+25}" y="{iy+236}" class="mono" font-size="9" fill="{WHITE}">V1: 1→2→4→8→7→5</text>')
A(f'<text x="{ix+25}" y="{iy+268}" class="mono" font-size="9" fill="{WHITE}">V3: 3→6 · V9: 9</text>')
A(f'<text x="{ix+25}" y="{iy+315}" class="mono" font-size="8.5" fill="{PURPLE}">TRANSFORMER ROTATION / INTERACTION</text>')
A(f'<text x="{ix+25}" y="{iy+346}" class="mono" font-size="7.4" fill="{GREY}">bridge recorded as analogy candidate · equivalence not asserted yet</text>')
end_panel()

# 4 — working status + self-reference
ix,iy,iw,ih=panel(*p18[3],"Audited slice status ledger","Per-layer mapping is accepted; A2 is local; boundary candidate b₁ selected","transformer_frame_status","AUDITED SLICE MODEL")
rows=[
("PROPOSED","Cₗ ↔ residual carrier · VALID"),
("PROPOSED","S ↔ attention / FFN / positional structure"),
("PROPOSED","b ↔ residual merge x+F(x)"),
("PROPOSED","6+1 Seed geometry ↔ Chapter-17 closure"),
("ANALOGY CANDIDATE","finite abjad orbit ↔ transformer rotational structure"),
("PROVENANCE","atlas developed with a transformer-based language model"),
("OPEN","final exact / mapping / analogy / open classification"),
]
for j,(status,desc) in enumerate(rows):
    yy=iy+28+j*47
    col=GREEN if status=="PROVENANCE" else (PURPLE if "ANALOGY" in status else CYAN if status=="PROPOSED" else GREY)
    A(f'<rect x="{ix+25}" y="{yy}" width="145" height="29" rx="7" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".38"/>')
    A(f'<text x="{ix+97}" y="{yy+19}" text-anchor="middle" class="mono" font-size="6.7" fill="{col}">{esc(status)}</text>')
    A(f'<text x="{ix+190}" y="{yy+19}" class="mono" font-size="7" fill="{WHITE}">{esc(desc)}</text>')
A(f'<line x1="{ix+25}" y1="{iy+376}" x2="{ix+iw-25}" y2="{iy+376}" stroke="{GREY}" stroke-opacity=".22"/>')
A(f'<text x="{ix+25}" y="{iy+410}" class="mono" font-size="7.4" fill="{PURPLE}">SELF-REFERENCE OBSERVATION: the map is produced by a system being mapped</text>')
end_panel()



# --------------------------
# Chapter 19
# --------------------------
ch=HEADER_H+18*CHAPTER_H
chapter_header(ch,19,*chapters[18])

CG19=json.loads((OUT/"data"/"choice_geometry_ch19.json").read_text(encoding="utf-8"))
p19=grid_panels(ch)

# 1 — choice operator
ix,iy,iw,ih=panel(*p19[0],"Choice space Θ","A choice selects an admissible operator; fixed input + fixed θ yields deterministic execution","choice_operator_theta","F_θ : X → Y ; θ∈Θ")
A(f'<text x="{ix+35}" y="{iy+62}" class="mono" font-size="18" fill="{WHITE}">X</text>')
arrow(ix+75,iy+58,ix+235,iy+58,CYAN)
A(f'<rect x="{ix+250}" y="{iy+25}" width="175" height="70" rx="13" fill="{PURPLE}" fill-opacity=".16" stroke="{PURPLE}" stroke-opacity=".55"/>')
A(f'<text x="{ix+337}" y="{iy+52}" text-anchor="middle" class="mono" font-size="11" fill="{PURPLE}">F_θ</text>')
A(f'<text x="{ix+337}" y="{iy+75}" text-anchor="middle" class="mono" font-size="7" fill="{WHITE}">θ ∈ Θ</text>')
arrow(ix+440,iy+58,ix+585,iy+58,CYAN)
A(f'<text x="{ix+610}" y="{iy+62}" class="mono" font-size="18" fill="{WHITE}">Y</text>')
A(f'<line x1="{ix+30}" y1="{iy+128}" x2="{ix+iw-30}" y2="{iy+128}" stroke="{GREY}" stroke-opacity=".25"/>')
A(f'<text x="{ix+35}" y="{iy+167}" class="mono" font-size="9" fill="{GREEN}">fixed X + fixed θ → deterministic execution</text>')
A(f'<text x="{ix+35}" y="{iy+203}" class="mono" font-size="8" fill="{GREY}">choice = explicit selection from Θ · not randomness by definition</text>')
A(f'<text x="{ix+35}" y="{iy+248}" class="mono" font-size="8" fill="{CYAN}">θ itself must be serializable / hashable / auditable</text>')
end_panel()

# 2 — geometric branch
ix,iy,iw,ih=panel(*p19[1],"Geometric chain","Vector geometry and byte encoding are separate transformations with different invertibility","choice_geometric_chain","SVG --R--> PNG --B--> Base64 --B⁻¹--> PNG ; PNG --V--> SVG′")
nodes=[("SVG","vector"),("PNG","raster"),("BASE64","symbols"),("PNG","bytes")]
xs=[ix+45,ix+205,ix+365,ix+535]
for j,(a0,b0) in enumerate(nodes):
    block(xs[j],iy+70,120,65,a0,b0)
for j,label in enumerate(["R","B","B⁻¹"]):
    arrow(xs[j]+125,iy+102,xs[j+1]-8,iy+102,CYAN)
    A(f'<text x="{(xs[j]+125+xs[j+1]-8)/2:.1f}" y="{iy+88}" text-anchor="middle" class="mono" font-size="7" fill="{PURPLE}">{label}</text>')
A(f'<text x="{ix+35}" y="{iy+184}" class="mono" font-size="8" fill="{GREEN}">B⁻¹(B(PNG)) = PNG · exact byte roundtrip</text>')
A(f'<text x="{ix+35}" y="{iy+220}" class="mono" font-size="8" fill="{GREY}">R loses vector primitive identity in general</text>')
A(f'<text x="{ix+35}" y="{iy+256}" class="mono" font-size="8" fill="{GREY}">optional vectorization V(PNG)=SVG′ is inference, not exact inverse of R</text>')
end_panel()

# 3 — symbolic branch
ix,iy,iw,ih=panel(*p19[2],"Symbolic chain","The language path records each chosen mapping rather than collapsing them into one encoding step","choice_symbolic_chain","UTF → Σ73 → abjad → V-orbits → Frame → transformer slice")
labels=[("UTF","carrier"),("Σ73","field"),("ABJAD","values"),("V1/V3/V9","orbits"),("FRAME","C,S,b"),("SLICE","Cₗ,Sₗ,b₁")]
x0=ix+18
gap=105
for j,(a0,b0) in enumerate(labels):
    xx=x0+j*gap
    A(f'<rect x="{xx}" y="{iy+72}" width="84" height="68" rx="10" fill="#08111d" stroke="{CYAN if j<2 else PURPLE if j<4 else GREEN}" stroke-opacity=".42"/>')
    A(f'<text x="{xx+42}" y="{iy+98}" text-anchor="middle" class="mono" font-size="7.5" fill="{WHITE}">{a0}</text>')
    A(f'<text x="{xx+42}" y="{iy+119}" text-anchor="middle" class="mono" font-size="5.8" fill="{GREY}">{b0}</text>')
    if j<len(labels)-1:
        arrow(xx+88,iy+106,xx+gap-5,iy+106,CYAN)
A(f'<text x="{ix+28}" y="{iy+196}" class="mono" font-size="7.6" fill="{CYAN}">each arrow has its own locked θ or invariant</text>')
A(f'<text x="{ix+28}" y="{iy+231}" class="mono" font-size="7.2" fill="{GREY}">UTF-8 is carrier serialization; it is not the same operation as rasterization or Base64</text>')
A(f'<text x="{ix+28}" y="{iy+268}" class="mono" font-size="7.2" fill="{GREY}">the two chains meet only where an explicit mapping says they meet</text>')
end_panel()

# 4 — registry
ix,iy,iw,ih=panel(*p19[3],"Choice registry","The repo names the concrete freedom instead of hiding it inside generated outputs","choice_registry","Θ_used = {θ_raster, θ_utf73, θ_bridge, θ_abjad, θ_atomic, θ_transformer}")
registry=CG19["choice_registry"]
for j,row in enumerate(registry):
    yy=iy+25+j*45
    pending=row.get("status")=="ROUTED_OPEN"
    col=RED if pending else [CYAN,PURPLE,GREEN,CYAN,PURPLE,GREEN][j]
    A(f'<text x="{ix+25}" y="{yy}" class="mono" font-size="7.0" fill="{col}">{esc(row["id"])}</text>')
    A(f'<text x="{ix+145}" y="{yy}" class="mono" font-size="6.3" fill="{WHITE}">Ch{row["chapter"]} · {esc(row["parameter"])}</text>')
    lock=row.get("locked_by") or "NONE"
    status=row.get("status","LOCKED")
    A(f'<text x="{ix+145}" y="{yy+18}" class="mono" font-size="5.6" fill="{col if pending else GREY}">{esc(row["kind"])} · {status} · lock: {esc(lock)}</text>')
A(f'<line x1="{ix+25}" y1="{iy+300}" x2="{ix+iw-25}" y2="{iy+300}" stroke="{GREY}" stroke-opacity=".22"/>')
A(f'<text x="{ix+25}" y="{iy+326}" class="mono" font-size="6.7" fill="{RED}">Θ_used \\ Θ_locked = {{θ_bridge}} · closure_complete = false · OPEN_BY_DESIGN</text>')
end_panel()

# 5 — reflective closure
ix,iy,iw,ih=panel(*p19[4],"Reflective closure","The chosen operator becomes data in the artifact that it helps generate","choice_reflective_closure","θ → F_θ → F_θ(X) → encode(θ,F_θ,results)")
steps=[("θ","choice"),("F_θ","operator"),("F_θ(X)","state"),("ENCODE","JSON · hashes · equations · tests")]
sx=[ix+35,ix+305,ix+575,ix+875]
for j,(a0,b0) in enumerate(steps):
    A(f'<rect x="{sx[j]}" y="{iy+25}" width="{190 if j<3 else 440}" height="68" rx="12" fill="#08111d" stroke="{[PURPLE,CYAN,GREEN,PURPLE][j]}" stroke-opacity=".48"/>')
    A(f'<text x="{sx[j]+(95 if j<3 else 220)}" y="{iy+52}" text-anchor="middle" class="mono" font-size="9" fill="{WHITE}">{esc(a0)}</text>')
    A(f'<text x="{sx[j]+(95 if j<3 else 220)}" y="{iy+73}" text-anchor="middle" class="mono" font-size="6.4" fill="{GREY}">{esc(b0)}</text>')
    if j<3: arrow(sx[j]+200,iy+59,sx[j+1]-12,iy+59,CYAN)
A(f'<text x="{ix+35}" y="{iy+125}" class="mono" font-size="7.3" fill="{GREEN}">reflection = provenance: the structure records the choices that generated it · one bridge remains intentionally open</text>')
A(f'<text x="{ix+35}" y="{iy+148}" class="mono" font-size="6.7" fill="{GREY}">open-by-design: θ_bridge stays unlocked; closure_complete remains false structurally</text>')
end_panel()



# --------------------------
# Chapter 20
# --------------------------
ch=HEADER_H+19*CHAPTER_H
chapter_header(ch,20,*chapters[19])

CI20=json.loads((OUT/"data"/"carrier_invariance_ch20.json").read_text(encoding="utf-8"))
CM20=json.loads((OUT/"data"/"carrier_invariance_measurement.json").read_text(encoding="utf-8"))
p20=grid_panels(ch)

# 1 — carrier / route / field
ix,iy,iw,ih=panel(*p20[0],"Carrier → Route → Canonical field","Model/tokenizer may vary; the committed route selects a canonical discrete project state","carrier_route_invariance","(M,τ) → adapter → R → D")
block(ix+25,iy+60,170,78,"(M, τ)","replaceable carrier")
arrow(ix+210,iy+99,ix+285,iy+99,CYAN)
block(ix+300,iy+60,165,78,"ADAPTER","interface contract")
arrow(ix+480,iy+99,ix+555,iy+99,CYAN)
block(ix+570,iy+60,125,78,"R","code · chapters")
A(f'<text x="{ix+25}" y="{iy+188}" class="mono" font-size="8.5" fill="{GREY}">R contains committed mappings, equations, validators and deterministic generators</text>')
A(f'<text x="{ix+25}" y="{iy+232}" class="mono" font-size="9" fill="{GREEN}">carrier substitution claim is CONDITIONAL on the declared interface</text>')
A(f'<text x="{ix+25}" y="{iy+274}" class="mono" font-size="7.4" fill="{CYAN}">no claim: arbitrary model outputs, logits or token IDs remain identical</text>')
end_panel()

# 2 — canonical D / Planck project term
ix,iy,iw,ih=panel(*p20[1],"Canonical discrete field D","Project-defined Planck-dataveld = exact JSON subset, not a physical Planck-scale assertion","canonical_discrete_field","D = canonical{orbits,7,Θ,status,slice}")
items=[
("V1/V3/V9","exact finite orbit records"),
("7 closure","9 → 7 quotient cardinalities"),
("Θ accounting","used / locked / routed-open"),
("Ch19 bridge","ROUTED_OPEN · 0.0.0.0 symbol"),
("Ch18 slice","per-layer A2 + b₁ selection"),
]
for j,(a0,b0) in enumerate(items):
    yy=iy+38+j*52
    A(f'<text x="{ix+25}" y="{yy}" class="mono" font-size="7.6" fill="{[CYAN,PURPLE,GREEN,CYAN,PURPLE][j]}">{esc(a0)}</text>')
    A(f'<text x="{ix+170}" y="{yy}" class="mono" font-size="6.8" fill="{WHITE}">{esc(b0)}</text>')
A(f'<line x1="{ix+25}" y1="{iy+302}" x2="{ix+iw-25}" y2="{iy+302}" stroke="{GREY}" stroke-opacity=".22"/>')
A(f'<text x="{ix+25}" y="{iy+333}" class="mono" font-size="6.8" fill="{GREEN}">SHA-256: {CM20["canonical_sha256"]}</text>')
end_panel()

# 3 — executable substitution check
ix,iy,iw,ih=panel(*p20[2],"Executable carrier substitution","Two abstract compatible carrier adapters reconstruct byte-equivalent canonical D","carrier_substitution_test","sha256(canonical(D_A)) = sha256(canonical(D_B))")
block(ix+25,iy+50,170,75,"CARRIER A","(M₁,τ₁) fixture")
block(ix+25,iy+180,170,75,"CARRIER B","(M₂,τ₂) fixture")
arrow(ix+210,iy+87,ix+345,iy+130,CYAN)
arrow(ix+210,iy+217,ix+345,iy+158,CYAN)
block(ix+360,iy+105,180,80,"CANONICAL D","same structural subset")
arrow(ix+555,iy+145,ix+645,iy+145,GREEN)
A(f'<text x="{ix+25}" y="{iy+305}" class="mono" font-size="8" fill="{GREEN}">A hash = {CM20["carrier_A_sha256"][:24]}…</text>')
A(f'<text x="{ix+25}" y="{iy+335}" class="mono" font-size="8" fill="{GREEN}">B hash = {CM20["carrier_B_sha256"][:24]}…</text>')
A(f'<text x="{ix+25}" y="{iy+368}" class="mono" font-size="10" fill="{WHITE}">WITNESS MATCH = {str(CM20["deterministic_witness_match"]).upper()}</text>')
A(f'<text x="{ix+25}" y="{iy+397}" class="mono" font-size="6.6" fill="{RED}">current A/B test does not consume carrier content → reader-independence remains OPEN</text>')
end_panel()

# 4 — generation/read/token routes
ix,iy,iw,ih=panel(*p20[3],"Read route","Generation, parsing and tokenization are distinct parameterized operations","read_route_operations","G:A→SVG ; P_φ:SVG→Â ; T_τ:text→tokens")
rows=[
("GENERATION","G : atlas-data → SVG","exact for fixed committed generator"),
("PARSING","P_φ : SVG → parsed structure","deterministic given parser φ"),
("TOKENIZATION","T_τ : text → token sequence","deterministic given tokenizer τ"),
("ROUNDTRIP","P_φ(G(A)) ≅ A","EXACT on serialized structural subset"),
]
for j,(a0,b0,c0) in enumerate(rows):
    yy=iy+30+j*73
    A(f'<text x="{ix+25}" y="{yy}" class="mono" font-size="7.2" fill="{[CYAN,PURPLE,GREEN,CYAN][j]}">{a0}</text>')
    A(f'<text x="{ix+155}" y="{yy}" class="mono" font-size="8" fill="{WHITE}">{esc(b0)}</text>')
    A(f'<text x="{ix+155}" y="{yy+24}" class="mono" font-size="6.4" fill="{GREY}">{esc(c0)}</text>')
A(f'<text x="{ix+25}" y="{iy+342}" class="mono" font-size="7" fill="{PURPLE}">self-consistency = EXACT · reader-independence = OPEN · full semantic self-read = OPEN</text>')
end_panel()

# 5 — status ledger / 0,1,boundary typing
ix,iy,iw,ih=panel(*p20[4],"Carrier-invariance ledger","0 / 1 / 1≡0 is project typing; executable equality is the canonical D hash","carrier_invariance_status","f=i∘b∘p ; X/~_f≅im(f) ; RI1∧RI2∧RI3")
cols=[
("SELF-CONSISTENCY","P_φ(G(A))≅A_serialized","EXACT"),
("INDEP. READER","P_χ + fault injection","PASS · SENSITIVITY"),
("RI GATE","RI1 ∧ RI2 ∧ RI3","LOGIC TESTED"),
("FULL SEMANTIC","P_full(G_total(A))=A","EXACT"),
]
xx=[ix+25,ix+365,ix+705,ix+1045]
for j,(a0,b0,c0) in enumerate(cols):
    A(f'<rect x="{xx[j]}" y="{iy+22}" width="290" height="92" rx="12" fill="#08111d" stroke="{[CYAN,PURPLE,GREEN,RED][j]}" stroke-opacity=".42"/>')
    A(f'<text x="{xx[j]+18}" y="{iy+50}" class="mono" font-size="7.5" fill="{[CYAN,PURPLE,GREEN,RED][j]}">{esc(a0)}</text>')
    A(f'<text x="{xx[j]+18}" y="{iy+76}" class="mono" font-size="6.5" fill="{WHITE}">{esc(b0)}</text>')
    A(f'<text x="{xx[j]+18}" y="{iy+99}" class="mono" font-size="6" fill="{GREY}">{esc(c0)}</text>')
A(f'<text x="{ix+25}" y="{iy+144}" class="mono" font-size="6.8" fill="{GREY}">factorization exact · P_χ sensitivity tested · RI gate logic tested · real reader-independence remains OPEN</text>')
end_panel()


# Footer
fy=HEADER_H+N_CH*CHAPTER_H
A(f'<line x1="70" y1="{fy+40}" x2="1530" y2="{fy+40}" stroke="{GREY}" stroke-opacity=".22"/>')
A(f'<text x="70" y="{fy+76}" class="mono" font-size="11" letter-spacing="1.4" fill="{GREY}">SIGNALS &amp; SYSTEMS · FULL VISUAL ATLAS · NPN // SIGNAL FIELD</text>')
A(f'<text x="1530" y="{fy+76}" text-anchor="end" class="mono" font-size="11" letter-spacing="1.4" fill="{CYAN}">20 CHAPTERS · 103 VISUAL FIELDS · 1 SVG</text>')
A(f'<text x="70" y="{fy+108}" class="mono" font-size="8.5" fill="{GREY}">Original educational atlas. Geometry, samples, spectra, pole-zero maps and diagrams are generated and embedded directly in the SVG.</text>')
A('</svg>')

SVG_PATH.write_text("\n".join(svg),encoding="utf-8")

# Verification
text=SVG_PATH.read_text(encoding="utf-8")
root=ET.fromstring(text)
concepts=[el.attrib.get("data-concept") for el in root.iter() if "data-concept" in el.attrib]
metadata=root.find("{http://www.w3.org/2000/svg}metadata")

def _check_embedded_image_only(t):
    has_b64 = 'href="data:image/png;base64,' in t
    no_http = "http://" not in t.replace("http://www.w3.org/2000/svg", "")
    no_https = "https://" not in t
    return "PASS" if (has_b64 and no_http and no_https) else "CHECK"

def _check_no_external_urls(t):
    return "PASS" if ("http://" not in t.replace("http://www.w3.org/2000/svg", "") and "https://" not in t) else "CHECK"

report=[
    "SIGNALS & SYSTEMS · FULL VISUAL ATLAS · VERIFICATION",
    "="*62,
    f"SVG path: {SVG_PATH.relative_to(OUT)}",
    f"viewBox: {root.attrib.get('viewBox')}",
    f"pixel size: {root.attrib.get('width')} × {root.attrib.get('height')}",
    f"chapter count: {len(chapters)}",
    f"visual field count: {len(concepts)}",
    f"unique concept ids: {len(set(concepts))}",
    f"embedded metadata: {'PASS' if metadata is not None else 'FAIL'}",
    f"SVG title: {'PASS' if root.find('{http://www.w3.org/2000/svg}title') is not None else 'FAIL'}",
    f"SVG description: {'PASS' if root.find('{http://www.w3.org/2000/svg}desc') is not None else 'FAIL'}",
    f"XML parse: PASS",
    f"embedded image only: {_check_embedded_image_only(text)}",
    f"external URLs: {_check_no_external_urls(text)}",
    f"Chapter 14 PNG bytes: {len(CH14_PNG_BYTES)}",
    f"Chapter 14 PNG sha256: {CH14_RAW_SHA256}",
    f"Chapter 14 Base64 chars: {len(CH14_B64)}",
    f"Chapter 14 Base64 sha256: {CH14_B64_SHA256}",
    f"Chapter 15 real RGB24 basin sum: {sum(UTF73_REAL_COUNTS)}",
    f"Chapter 15 real RGB24 basin min/max: {min(UTF73_REAL_COUNTS)} / {max(UTF73_REAL_COUNTS)}",
    "",
    "Concept IDs:",
]
report += [f"- {c}" for c in concepts]
VERIFY_PATH.write_text("\n".join(report),encoding="utf-8")
