"""Simple line-art analogy scenes (viewBox 420x290) using the deck's analogy animation classes."""

def _w(inner, label):
    return f'<svg viewBox="0 0 420 290" class="viz">{inner}<text x="210" y="280" class="viz-lbl" text-anchor="middle">{label}</text></svg>'

R = 'stroke="var(--rose)" stroke-width="2.5" fill="none"'
W = 'stroke="var(--w6)" stroke-width="2" fill="none"'
WF = 'stroke="var(--w5)" stroke-width="1.6" fill="rgba(255,255,255,.03)"'
RF = 'stroke="var(--rose)" stroke-width="2.2" fill="rgba(200,50,74,.08)"'


def person(x, y, s=1.0, cls=""):
    return (f'<g class="{cls}" transform="translate({x},{y}) scale({s})"><circle cx="0" cy="-46" r="16" {W}></circle>'
            f'<path d="M-28 20 q0 -40 28 -40 q28 0 28 40" {W}></path></g>')


def doc(x, y, w=70, h=90, lines=4, cls="", red=False):
    ls = "".join(f'<line x1="{x+12}" y1="{y+20+i*14}" x2="{x+w-12-(i%2)*14}" y2="{y+20+i*14}" stroke="var(--w4)" stroke-width="2"></line>' for i in range(lines))
    return f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" {RF if red else WF}></rect>{ls}</g>'


SCENES = {
 "intern": lambda: _w(person(150, 190) + f'<path d="M210 70 h150 a12 12 0 0 1 12 12 v54 a12 12 0 0 1 -12 12 h-110 l-22 20 v-20 h-18 a12 12 0 0 1 -12 -12 v-54 a12 12 0 0 1 12 -12z" {RF}></path>'
                       '<text x="285" y="104" text-anchor="middle" style="font:700 15px var(--mono);fill:var(--w8)">Q3 return: 4.1%</text>'
                       '<text x="285" y="128" text-anchor="middle" class="vp" style="font:700 22px var(--mono);fill:var(--rose)">source?</text>', "fast, fluent — and sometimes guessing"),
 "pass": lambda: _w(''.join(f'<rect x="{60+i*80}" y="70" width="58" height="120" rx="5" {RF if i<2 else WF}></rect><circle cx="{106+i*80}" cy="132" r="4" fill="{"var(--rose)" if i<2 else "var(--w4)"}"></circle>' for i in range(4))
                      + '<rect x="160" y="210" width="100" height="44" rx="8" stroke="var(--rose)" stroke-width="2" fill="rgba(200,50,74,.12)" class="vg"></rect><text x="210" y="237" text-anchor="middle" style="font:700 12px var(--mono);fill:var(--rose-lt)">YOUR PASS</text>', "it opens only your doors"),
 "lift": lambda: _w('<rect x="110" y="40" width="200" height="200" rx="8" ' + WF + '></rect>' + person(170, 200, .9) + person(250, 200, .9)
                      + '<path d="M300 120 q18 20 0 40" class="vp" ' + R + '></path><path d="M318 108 q30 32 0 64" class="vp2" ' + R + '></path>', "who else can hear this?"),
 "brief": lambda: _w('<rect x="120" y="30" width="180" height="220" rx="10" ' + WF + '></rect>' + ''.join(
                      f'<text x="145" y="{80+i*44}" style="font:700 18px var(--mono);fill:var(--rose)" class="vp{"" if i==0 else i+1}">{k}</text><line x1="175" y1="{74+i*44}" x2="{280-(i%2)*30}" y2="{74+i*44}" stroke="var(--w4)" stroke-width="2"></line>' for i, k in enumerate("CTFT")), "who · what · how · in what voice"),
 "tailor": lambda: _w('<path d="M150 60 l30 -20 h60 l30 20 l40 40 l-30 30 l-20 -20 v130 h-100 v-130 l-20 20 l-30 -30z" ' + WF + '></path>'
                       '<line x1="120" y1="200" x2="300" y2="200" stroke="var(--rose)" stroke-width="3" stroke-dasharray="6 6" class="vdash"></line>', "first fitting → adjust → adjust"),
 "folder": lambda: _w(''.join(f'<path d="M{60+i*110} 110 h40 l10 12 h50 v80 h-100z" {RF if i==2 else WF}></path>' for i in range(3))
                       + '<path d="M325 70 l-20 30" ' + R + '></path><path d="M300 95 l5 5 l10 -6" ' + R + '></path><text x="270" y="232" text-anchor="middle" style="font:700 11px var(--mono);fill:var(--rose-lt)">30 SEP</text><text x="110" y="232" text-anchor="middle" style="font:700 11px var(--mono);fill:var(--w4)">JUNE</text>', "point at the right file"),
 "onepager": lambda: _w(doc(60, 60, 60, 80) + doc(75, 75, 60, 80) + doc(90, 90, 60, 80) + '<path d="M180 140 h50" ' + R + ' class="vdash" stroke-dasharray="6 5"></path><path d="M222 132 l10 8 l-10 8" ' + R + '></path>'
                         + doc(260, 70, 90, 120, 5, "vsc", True), "the whole file, on one page"),
 "orderpad": lambda: _w('<rect x="130" y="30" width="160" height="220" rx="8" ' + WF + '></rect>' + ''.join(
                         f'<rect x="150" y="{62+i*42}" width="16" height="16" rx="3" stroke="var(--rose)" stroke-width="2" fill="none"></rect><path d="M153 {70+i*42} l4 4 l7 -9" stroke="var(--rose)" stroke-width="2.4" fill="none" class="vp{"" if i==0 else min(i+1,5)}"></path><line x1="178" y1="{70+i*42}" x2="270" y2="{70+i*42}" stroke="var(--w4)" stroke-width="2"></line>' for i in range(4)), "who · what · when · special requests"),
 "door": lambda: _w('<rect x="150" y="40" width="120" height="200" rx="4" ' + WF + '></rect><path d="M150 40 l60 18 v200 l-60 -18z" ' + RF + '></path><circle cx="198" cy="150" r="4" fill="var(--rose)"></circle>', "a short reply buys you time"),
 "mise": lambda: _w(''.join(f'<path d="M{50+i*85} 150 q38 50 76 0" {RF if i<3 else WF}></path><line x1="{48+i*85}" y1="150" x2="{128+i*85}" y2="150" stroke="var(--w5)" stroke-width="2"></line>' for i in range(4))
                     + ''.join(f'<circle cx="{88+i*85}" cy="138" r="7" fill="var(--rose)" class="vp{"" if i==0 else i+1}"></circle>' for i in range(3)), "prepared before you cook"),
 "scan": lambda: _w(''.join(f'<rect x="80" y="{50+i*34}" width="260" height="24" rx="4" {RF if i==3 else WF}></rect>' for i in range(5)) + '<g class="vscan"><circle cx="170" cy="130" r="34" ' + R + '></circle><line x1="194" y1="154" x2="222" y2="182" ' + R + '></line></g>', "trust — then check what changed"),
 "xray": lambda: _w(''.join(f'<rect x="{70+i*75}" y="{230-hh}" width="50" height="{hh}" rx="5" {RF if i==0 else WF}></rect>' for i, hh in enumerate([160, 90, 50, 45])), "the shape, not the rows"),
 "limit": lambda: _w('<circle cx="140" cy="130" r="70" stroke="var(--rose)" stroke-width="10" fill="rgba(255,255,255,.03)"></circle><text x="140" y="146" text-anchor="middle" style="font:800 46px var(--mf);fill:var(--w)">55</text>'
                      '<rect x="250" y="80" width="110" height="100" rx="10" ' + WF + '></rect><text x="305" y="138" text-anchor="middle" style="font:800 26px var(--mono);fill:var(--rose)" class="vp">10%</text>', "a range, and a weight limit"),
 "movers": lambda: _w(''.join(f'<path d="M{80+i*90} {150 if up else 110} l20 {-30 if up else 30} l20 {30 if up else -30}z" fill="{"rgba(200,50,74,.18)" if up else "rgba(255,255,255,.05)"}" stroke="{"var(--rose)" if up else "var(--w5)"}" stroke-width="2" class="vp{i+1 if i else ""}"></path>' for i, up in enumerate([1, 1, 0, 0])), "who moved the number?"),
 "letter": lambda: _w(doc(70, 60, 110, 150, 7) + '<rect x="270" y="140" width="80" height="100" rx="6" ' + WF + '></rect>' + person(310, 120, .8) + '<path d="M350 70 q20 20 0 40" class="vp" ' + R + '></path>', "read alone — or presented live"),
 "headline": lambda: _w('<rect x="90" y="40" width="240" height="200" rx="8" ' + WF + '></rect><rect x="110" y="60" width="200" height="34" rx="4" fill="rgba(200,50,74,.25)" stroke="var(--rose)" stroke-width="2" class="vg"></rect>' + ''.join(f'<line x1="110" y1="{120+i*20}" x2="{310-(i%3)*30}" y2="{120+i*20}" stroke="var(--w4)" stroke-width="2"></line>' for i, _ in enumerate(range(5))), "the most important fact first"),
 "sign": lambda: _w('<rect x="120" y="50" width="180" height="110" rx="10" fill="rgba(200,50,74,.12)" stroke="var(--rose)" stroke-width="2.5"></rect><text x="210" y="115" text-anchor="middle" style="font:800 22px var(--mf);fill:var(--w)">EXIT 3 →</text><line x1="210" y1="160" x2="210" y2="250" stroke="var(--w5)" stroke-width="4"></line>', "one sign, one message"),
 "sketch": lambda: _w('<rect x="80" y="40" width="260" height="200" rx="6" fill="rgba(61,123,224,.04)" stroke="var(--w4)" stroke-width="1.5"></rect>' + ''.join(f'<line x1="{80+i*26}" y1="40" x2="{80+i*26}" y2="240" stroke="rgba(255,255,255,.05)"></line>' for i in range(11))
                       + '<path d="M130 200 v-90 l80 -50 l80 50 v90z" ' + R + ' stroke-dasharray="7 6" class="vdash"></path>', "outline first, then build"),
 "checklist": lambda: _w('<rect x="130" y="30" width="160" height="220" rx="10" ' + WF + '></rect>' + ''.join(
                          f'<circle cx="160" cy="{72+i*46}" r="11" stroke="var(--rose)" stroke-width="2" fill="rgba(200,50,74,.1)"></circle><path d="M154 {72+i*46} l4 4 l8 -9" stroke="var(--rose)" stroke-width="2.4" fill="none" class="vp{"" if i==0 else i+1}"></path><text x="182" y="{77+i*46}" style="font:700 13px var(--mono);fill:var(--w7)">{t}</text>' for i, t in enumerate(["ACCURACY", "CONFIDENTIAL", "TONE", "COMPLETE"])), "every flight — every send"),
 "greet": lambda: _w(person(140, 190) + person(290, 190) + '<rect x="70" y="50" width="120" height="44" rx="10" ' + WF + '></rect><rect x="230" y="50" width="120" height="44" rx="10" ' + RF + '></rect><text x="130" y="77" text-anchor="middle" style="font:600 12px var(--mf);fill:var(--w7)">formal</text><text x="290" y="77" text-anchor="middle" style="font:600 12px var(--mf);fill:var(--rose-lt)">formal</text>', "match the voice you were given"),
 "jobdesc": lambda: _w(doc(90, 40, 140, 200, 9) + person(320, 200, .9) + '<path d="M240 140 h40" ' + R + ' stroke-dasharray="6 5" class="vdash"></path>', "the role, the rules, the files"),
}


def scene(k):
    return SCENES[k]()
