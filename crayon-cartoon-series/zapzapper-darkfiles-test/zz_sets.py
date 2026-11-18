"""Sets and props (world coordinates, 1280x720 logical canvas; ground line y~560). Flat palette, ~3-4 px black outlines like the series."""
from cc_kit import INK

def ol(w=3.4): return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'

def basement():
    o = []
    # back wall + ceiling + floor
    o.append('<rect x="-700" y="-300" width="3300" height="860" fill="#283246"/>')
    # brick courses (subtle)
    for y in range(120, 540, 36):
        o.append(f'<path d="M-700 {y} H2600" stroke="#232c3e" stroke-width="2.2"/>')
    for r, y in enumerate(range(120, 520, 36)):
        for x in range(-700 + (r % 2) * 38, 2600, 76):
            o.append(f'<path d="M{x} {y} v36" stroke="#232c3e" stroke-width="2.2"/>')
    o.append('<rect x="-700" y="-300" width="3300" height="420" fill="#1e2635"/>')                   # darker upper wall
    o.append(f'<path d="M-700 120 H2600" stroke="{INK}" stroke-width="4"/>')
    o.append('<rect x="-700" y="556" width="3300" height="400" fill="#1a2030"/>')
    o.append(f'<path d="M-700 556 H2600" stroke="{INK}" stroke-width="4"/>')
    for x in range(-640, 2600, 150):                                                                 # floor planks (perspective lines)
        o.append(f'<path d="M{x} 556 L{x * 1.35 - 230:.0f} 900" stroke="#232b3d" stroke-width="3"/>')
    for y in (600, 660, 730, 820): o.append(f'<path d="M-700 {y} H2600" stroke="#202839" stroke-width="2.4"/>')
    # ceiling beams + pipes
    o.append(f'<rect x="-700" y="-20" width="3300" height="46" fill="#3b2f2a" stroke="{INK}" stroke-width="3.4"/>')
    for bx in range(-500, 2600, 420): o.append(f'<rect x="{bx}" y="26" width="26" height="94" fill="#34292a" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<rect x="-700" y="58" width="3300" height="15" fill="#59657a" stroke="{INK}" stroke-width="3"/><rect x="-700" y="86" width="3300" height="12" fill="#6b4a3c" stroke="{INK}" stroke-width="3"/>')
    for px in range(-380, 2600, 310): o.append(f'<rect x="{px}" y="52" width="14" height="52" fill="#4a566a" stroke="{INK}" stroke-width="3"/>')
    # barred window with a cold light patch
    o.append(f'<rect x="250" y="150" width="120" height="62" fill="#7893b8" stroke="{INK}" stroke-width="4"/>')
    for bx in (280, 310, 340): o.append(f'<path d="M{bx} 150 V212" stroke="{INK}" stroke-width="4"/>')
    o.append('<path d="M250 212 L370 212 L470 556 L180 556 Z" fill="#7893b8" opacity=".10"/>')
    # stairs at the left (to the dark upstairs)
    for i in range(9):
        o.append(f'<path d="M{-520 + i * 40} {556 - i * 40} h40 v40 h-40 z" fill="{"#3a2f2c" if i % 2 else "#33292a"}" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<path d="M-520 556 L-160 196 L-160 156 L-520 516 Z" fill="#2e2523" stroke="{INK}" stroke-width="3"/>')
    o.append('<path d="M-160 196 L-520 556" stroke="#4f3d36" stroke-width="7"/>')
    # support pillar
    o.append(f'<rect x="690" y="26" width="64" height="530" fill="#454e60" stroke="{INK}" stroke-width="4"/><path d="M690 120 H754 M690 300 H754" stroke="#39414f" stroke-width="3"/>')
    # crates, barrels, boxes, bucket, bicycle-less clutter (left and right of the action)
    def crate(x, y, w, h, c='#6b4c33'):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{INK}" stroke-width="3.4"/>'
                f'<path d="M{x} {y + h / 2} H{x + w} M{x + w * .5} {y} V{y + h}" stroke="{INK}" stroke-width="2.4"/>')
    o.append(crate(420, 470, 86, 86) + crate(430, 392, 66, 78, '#7a573a') + crate(520, 500, 60, 56, '#5a402c'))
    o.append(f'<ellipse cx="610" cy="520" rx="34" ry="40" fill="#5a6a54" stroke="{INK}" stroke-width="3.4"/><path d="M576 505 H644 M576 535 H644" stroke="{INK}" stroke-width="2.6"/>')
    o.append(f'<path d="M120 556 L132 500 H178 L190 556 Z" fill="#6d747e" stroke="{INK}" stroke-width="3.4"/><path d="M132 500 Q155 478 178 500" fill="none" stroke="{INK}" stroke-width="3"/>')
    o.append(crate(1600, 480, 90, 76) + crate(1620, 404, 60, 76, '#7a573a') + crate(1710, 500, 70, 56, '#5a402c'))
    o.append(f'<rect x="1790" y="440" width="150" height="14" fill="#5a402c" stroke="{INK}" stroke-width="3.4"/><path d="M1800 454 V556 M1930 454 V556" stroke="{INK}" stroke-width="7"/><rect x="1810" y="408" width="40" height="32" fill="#8d8f94" stroke="{INK}" stroke-width="3"/>')
    # hanging cables, dead bulb, cobwebs
    o.append(f'<path d="M520 98 Q540 160 600 168 M900 98 Q930 150 880 190" fill="none" stroke="{INK}" stroke-width="3.4"/>')
    o.append(f'<path d="M1010 98 V182" stroke="{INK}" stroke-width="3"/><circle cx="1010" cy="196" r="13" fill="#3a3b3f" stroke="{INK}" stroke-width="3"/>')
    o.append('<path d="M-700 120 q40 20 20 60 M-700 120 q80 10 70 70" fill="none" stroke="#5e6a80" stroke-width="2" opacity=".8"/>')
    o.append('<path d="M1300 120 q-30 30 -20 70 M1300 120 q-60 14 -64 60 M1300 120 q-8 44 24 62" fill="none" stroke="#5e6a80" stroke-width="2" opacity=".8"/>')
    # door frame (door itself is animated in JS); hole behind the door
    o.append(f'<rect x="1072" y="326" width="146" height="236" fill="#3a2b24" stroke="{INK}" stroke-width="4"/>')
    o.append('<rect x="1085" y="340" width="120" height="215" fill="#0a0c12"/>')
    return ''.join(o)


def shelf():
    """Origin = left-bottom corner on the floor plate. 190 wide x 270 tall; bolt plates at both feet."""
    o = []
    o.append(f'<rect x="10" y="-268" width="170" height="268" fill="#3b2f25" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<rect x="0" y="-270" width="12" height="270" fill="#5b4631" stroke="{INK}" stroke-width="3.4"/><rect x="178" y="-270" width="12" height="270" fill="#5b4631" stroke="{INK}" stroke-width="3.4"/>')
    for i, y in enumerate((-270, -200, -130, -60)):
        o.append(f'<rect x="0" y="{y}" width="190" height="12" fill="#6e5639" stroke="{INK}" stroke-width="3.4"/>')
    items = [(-200, 'jar', 22, '#6c8a6c'), (-200, 'box', 62, '#8a7a55'), (-200, 'jar', 124, '#8a5f5f'), (-200, 'box', 150, '#55677f'),
             (-130, 'box', 18, '#7b6b4a'), (-130, 'jar', 92, '#6c8a6c'), (-130, 'box', 126, '#6a5a7a'),
             (-60, 'box', 20, '#55677f'), (-60, 'box', 80, '#8a7a55'), (-60, 'jar', 148, '#8a5f5f'),
             (-270, 'box', 40, '#7b6b4a'), (-270, 'jar', 118, '#6c8a6c')]
    for y, k, x, c in items:
        if k == 'jar': o.append(f'<rect x="{x}" y="{y - 36}" width="22" height="36" rx="5" fill="{c}" stroke="{INK}" stroke-width="3"/><rect x="{x + 3}" y="{y - 42}" width="16" height="7" fill="#444" stroke="{INK}" stroke-width="2.4"/>')
        else: o.append(f'<rect x="{x}" y="{y - 40}" width="40" height="40" fill="{c}" stroke="{INK}" stroke-width="3"/><path d="M{x} {y - 26} H{x + 40}" stroke="{INK}" stroke-width="2"/>')
    # feet plates
    o.append(f'<path d="M-8 0 H34 L40 12 H-14 Z" fill="#59616e" stroke="{INK}" stroke-width="3"/><path d="M156 0 H198 L204 12 H150 Z" fill="#59616e" stroke="{INK}" stroke-width="3"/>')
    return ''.join(o)


def bolt():
    """Hex bolt, origin at the base of the shank; head at the top (y<0)."""
    return (f'<rect x="-3" y="-6" width="6" height="12" fill="#8c929c" stroke="{INK}" stroke-width="2"/><path d="M-3 -2 h6 M-3 2 h6" stroke="{INK}" stroke-width="1.2"/>'
            f'<path d="M-8 -6 L-6 -13 H6 L8 -6 Z" fill="#a5abb5" stroke="{INK}" stroke-width="2.6"/>')


def wrench():
    """Ratchet wrench; origin at the socket centre, handle pointing +x."""
    return (f'<rect x="4" y="-4" width="48" height="8" rx="3" fill="#7b838f" stroke="{INK}" stroke-width="2.6"/>'
            f'<circle cx="0" cy="0" r="10" fill="#9aa1ac" stroke="{INK}" stroke-width="3"/><circle cx="0" cy="0" r="4" fill="#3a3d44"/>'
            f'<rect x="30" y="-5" width="22" height="10" rx="4" fill="#b45a2f" stroke="{INK}" stroke-width="2.4"/>')


def flashlight():
    """Origin at the grip, beam direction +x."""
    return (f'<rect x="-8" y="-5.5" width="26" height="11" rx="3" fill="#3a3f4a" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M18 -5.5 L30 -9.5 V9.5 L18 5.5 Z" fill="#59616e" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M30 -8 V8" stroke="#fff3c2" stroke-width="3.4"/>')


def recorder():
    """Small digital audio recorder, origin at the centre of the body (36 x 70). Screen and button states are driven from JS."""
    return (f'<rect x="-18" y="-35" width="36" height="70" rx="7" fill="#3c4048" stroke="{INK}" stroke-width="3.4"/>'
            f'<rect x="-12" y="-29" width="24" height="9" rx="4" fill="#23262c" stroke="{INK}" stroke-width="2"/>'      # mic grille
            f'<path d="M-9 -26 h18" stroke="#6a707b" stroke-width="1.4" stroke-dasharray="2 2"/>'
            f'<rect x="-13" y="-16" width="26" height="19" rx="3" fill="#0d1a13" stroke="{INK}" stroke-width="2.4"/>')


def interior():
    """Hidden room, x ~ 3250..4230 (right edge = the doorway wall)."""
    o = []
    o.append('<rect x="3100" y="-300" width="1300" height="860" fill="#2d2a34"/>')
    for y in range(140, 540, 40): o.append(f'<path d="M3100 {y} H4400" stroke="#26232c" stroke-width="2"/>')
    o.append('<rect x="3100" y="-300" width="1300" height="440" fill="#201e27"/>')
    o.append(f'<path d="M3100 140 H4400" stroke="{INK}" stroke-width="4"/>')
    o.append('<rect x="3100" y="556" width="1300" height="400" fill="#1b1a22"/>')
    o.append(f'<path d="M3100 556 H4400" stroke="{INK}" stroke-width="4"/>')
    for x in range(3140, 4400, 130): o.append(f'<path d="M{x} 556 L{x * 1.3 - 1160:.0f} 900" stroke="#242330" stroke-width="3"/>')
    o.append(f'<rect x="3100" y="-20" width="1300" height="44" fill="#352c2a" stroke="{INK}" stroke-width="3.4"/>')
    o.append(f'<rect x="3150" y="24" width="14" height="70" fill="#3a3b3f" stroke="{INK}" stroke-width="3"/><path d="M3640 24 V110" stroke="{INK}" stroke-width="3"/><circle cx="3640" cy="124" r="12" fill="#3a3b3f" stroke="{INK}" stroke-width="3"/>')
    # the doorway wall on the right with the open blue door seen edge-on
    o.append(f'<rect x="4208" y="-300" width="260" height="860" fill="#26232c" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<rect x="4208" y="326" width="16" height="236" fill="#3a2b24" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<path d="M4208 340 L4190 350 V548 L4208 556 Z" fill="#2a63b8" stroke="{INK}" stroke-width="3.4"/>')
    return ''.join(o)


def interior_objects():
    """Individually revealed objects: returns dict name -> svg."""
    d = {}
    # storage boxes (stack) x 3290..3420
    box = lambda x, y, w, h, c: (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{INK}" stroke-width="3.4"/>'
                                 f'<path d="M{x} {y + 14} H{x + w} M{x + w / 2 - 8} {y} v14 h16 v-14" stroke="{INK}" stroke-width="2.2" fill="#c9b98f"/>')
    d['boxes'] = box(3290, 470, 100, 86, '#8c7a58') + box(3310, 392, 76, 78, '#7d6c4c') + box(3396, 496, 66, 60, '#6f6049') + \
        f'<path d="M3300 520 H3380" stroke="#5a4c36" stroke-width="2.4"/>'
    # old telephone equipment: wall switchboard panel with jacks, dials and patch cords x 3480..3630
    jacks = ''.join(f'<circle cx="{3498 + (i % 4) * 28}" cy="{352 + (i // 4) * 28}" r="7" fill="#15161a" stroke="{INK}" stroke-width="2.4"/>' for i in range(12))
    d['phone_gear'] = (f'<rect x="3480" y="324" width="160" height="150" rx="6" fill="#4b4f45" stroke="{INK}" stroke-width="4"/>'
                       f'<rect x="3490" y="334" width="140" height="94" fill="#3a3d36" stroke="{INK}" stroke-width="2.4"/>{jacks}'
                       f'<circle cx="3520" cy="452" r="12" fill="#b59a5a" stroke="{INK}" stroke-width="3"/><circle cx="3562" cy="452" r="12" fill="#b59a5a" stroke="{INK}" stroke-width="3"/>'
                       f'<rect x="3590" y="440" width="34" height="22" fill="#7a2f2f" stroke="{INK}" stroke-width="2.6"/>'
                       f'<path d="M3498 380 Q3480 430 3520 470 M3554 380 Q3600 440 3580 500" fill="none" stroke="#c4402f" stroke-width="4"/>'
                       f'<path d="M3526 408 Q3548 470 3600 480" fill="none" stroke="#2f7ac4" stroke-width="4"/>')
    # wooden desk x 3650..3890, top y=470
    d['desk'] = (f'<rect x="3650" y="470" width="240" height="18" fill="#7b5636" stroke="{INK}" stroke-width="3.6"/>'
                 f'<rect x="3660" y="488" width="86" height="72" fill="#664629" stroke="{INK}" stroke-width="3.4"/><rect x="3790" y="488" width="86" height="72" fill="#664629" stroke="{INK}" stroke-width="3.4"/>'
                 f'<path d="M3668 508 H3738 M3668 530 H3738 M3798 508 H3868 M3798 530 H3868" stroke="{INK}" stroke-width="2.4"/><circle cx="3703" cy="519" r="3" fill="#c9b36a"/><circle cx="3833" cy="519" r="3" fill="#c9b36a"/>'
                 f'<rect x="3750" y="488" width="36" height="72" fill="#1f1a18" opacity=".5"/>')
    # rotary phone base + handset on its cable, on the desk top
    d['handset'] = (f'<rect x="3690" y="440" width="64" height="30" rx="8" fill="#23262c" stroke="{INK}" stroke-width="3.4"/>'
                    f'<circle cx="3722" cy="446" r="9" fill="#9a9ca4" stroke="{INK}" stroke-width="2.4"/>'
                    f'<path d="M3722 440 Q3700 420 3676 432 Q3660 440 3668 456 Q3680 468 3700 462" fill="none" stroke="#1a1b1f" stroke-width="5" stroke-linecap="round"/>'
                    f'<path d="M3668 448 Q3650 470 3660 470 H3700" fill="none" stroke="{INK}" stroke-width="2.4" opacity="0"/>'
                    f'<path d="M3694 438 C3704 424 3742 424 3752 438 L3748 444 C3738 436 3708 436 3698 444 Z" fill="#2a2d34" stroke="{INK}" stroke-width="3"/>'
                    f'<path d="M3752 440 Q3790 470 3770 470" fill="none" stroke="#1a1b1f" stroke-width="3.4" stroke-linecap="round"/>')
    return d
