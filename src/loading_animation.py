# Loading animation for the Gradio app: look only, no app logic.
# While a draft loads, a hand-drawn rider cycles across the Draft box in 6 seconds,
# then keeps pedalling at the finish flag until the text arrives.
# The bike and rider follow the Product dropdown:
#   road = man in a navy blazer, gravel = woman in a teal blazer,
#   mountain = woman with dark skin in a burgundy blazer.
# Everything is inline SVG inside CSS: no image files, no new packages,
# no font downloads, nothing is sent to Python.

import math
from urllib.parse import quote

RIDE_SECONDS = 6       # time to ride from start to finish flag
N_FRAMES = 24          # leg poses per crank turn
CRANK_DUR = 0.9        # seconds per crank turn
WHEEL_DUR = 0.55       # seconds per wheel turn

INK = '#1E293B'        # sketch line colour

# Bike geometry per product (viewBox 0 0 240 210, bike rides to the right)
BIKES = {
    'road': dict(R=40, tyre=4.5, tube=5, color='#DC2626', st_top=(94, 107),
                 ht_top=(166, 102), ht_bot=(171, 118), bar='drop',
                 shoulder=(127, 51), hands=(185, 93)),
    'gravel': dict(R=40, tyre=7, tube=5.5, color='#B7791F', st_top=(95, 109),
                   ht_top=(165, 99), ht_bot=(170, 117), bar='drop',
                   shoulder=(125, 49), hands=(184, 91), frame_bag=True),
    'mountain': dict(R=41, tyre=8, tube=6.5, color='#059669', st_top=(99, 121),
                     ht_top=(164, 98), ht_bot=(169, 116), bar='flat',
                     shoulder=(122, 47), hands=(177, 84), knobby=True, suspension=True),
}

# Rider per product: same outfit level, helmet, size and pose for everyone
RIDERS = {
    'road': dict(skin='#F3D5BC', skin_shade='#E2B48F', hair='#6B5344', hair_style='short',
                 blazer='#7E8FC1', blazer_far='#5F6FA3', neckwear='tie', neck_color='#F07A92',
                 shoe='#B08068', glasses=True, earring=False),
    'gravel': dict(skin='#E7C2A6', skin_shade='#CF9E7C', hair='#B5653A', hair_style='ponytail',
                   blazer='#7FB3AE', blazer_far='#5E948F', neckwear='scarf', neck_color='#F7C463',
                   shoe='#475569', glasses=False, earring=True),
    'mountain': dict(skin='#7A4B32', skin_shade='#5E3622', hair='#2B2220', hair_style='puff',
                     blazer='#CE8296', blazer_far='#AF6478', neckwear='scarf', neck_color='#7DD3FC',
                     shoe='#475569', glasses=False, earring=True),
}

RA, FA, BB = (58, 160), (184, 160), (112, 166)   # rear axle, front axle, bottom bracket
HIP, SADDLE_Y, CRANK = (92, 89), 92, 17
THIGH, SHIN, UPPER_ARM, FOREARM = 48, 50, 37, 37
HELMET = '#93B4F5'
TROUSERS, TROUSERS_FAR = '#9CA3AF', '#6B7280'


def _tint(hex_color, amount=0.45):
    # Mix a colour with white for the light colour wash
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    r, g, b = (round(c + (255 - c) * amount) for c in (r, g, b))
    return f'#{r:02X}{g:02X}{b:02X}'


def _p(pt):
    return f'{pt[0]:.1f},{pt[1]:.1f}'


def _ik(a, b, l1, l2):
    # Middle joint (knee or elbow) between a and b; picks the forward/lower side
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = min(math.hypot(dx, dy), l1 + l2 - 0.01)
    t = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(l1 * l1 - t * t, 0))
    ux, uy = dx / d, dy / d
    px, py = a[0] + ux * t, a[1] + uy * t
    c1, c2 = (px - uy * h, py + ux * h), (px + uy * h, py - ux * h)
    return c1 if c1[0] > c2[0] else c2


class Sketch:
    # Collects SVG pieces in the sketch look: ink outline plus light colour wash

    def __init__(self):
        self.out = []

    def add(self, svg):
        self.out.append(svg)

    def tube(self, d, wash, width, values=None, dur=CRANK_DUR):
        # Thick line with an ink outline: frame tubes, legs, arms, shoes
        anim = (f'<animate attributeName="d" values="{values}" dur="{dur}s" repeatCount="indefinite"/>'
                if values else '')
        for colour, w in ((INK, width + 2.6), (wash, max(width - 0.6, 0.8))):
            self.add(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{w:.1f}" '
                     f'stroke-linecap="round" stroke-linejoin="round">{anim}</path>')

    def line(self, d, width=1.5):
        # Thin ink line: spokes, chain, bars
        self.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{width}" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')

    def shape(self, d, wash, inner=''):
        # Closed shape with wash fill and ink outline: blazer, hair, helmet
        self.add(f'<path d="{d}" fill="{wash}" stroke="{INK}" stroke-width="1.7" '
                 f'stroke-linejoin="round">{inner}</path>')

    def circle(self, c, r, wash, width=1.6):
        self.add(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}" fill="{wash}" '
                 f'stroke="{INK}" stroke-width="{width}"/>')


def _wheel(s, c, bike):
    # Tyre, rim and spinning spokes
    R, tyre = bike['R'], bike['tyre']
    spin = (f'<animateTransform attributeName="transform" type="rotate" from="0 {c[0]} {c[1]}" '
            f'to="360 {c[0]} {c[1]}" dur="{WHEEL_DUR}s" repeatCount="indefinite"/>')
    s.add(f'<circle cx="{c[0]}" cy="{c[1]}" r="{R}" fill="none" stroke="{INK}" stroke-width="{tyre * 0.55 + 1.2:.1f}"/>')
    s.add(f'<circle cx="{c[0]}" cy="{c[1]}" r="{R - tyre / 2 - 2.6:.1f}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.add(f'<g>{spin}')
    if bike.get('knobby'):
        s.add(f'<circle cx="{c[0]}" cy="{c[1]}" r="{R + tyre / 2 + 1:.1f}" fill="none" stroke="{INK}" '
              f'stroke-width="3" stroke-dasharray="3 3.6"/>')
    for i in range(8):
        a = math.pi * i / 4
        s.line(f'M{c[0]},{c[1]} L{c[0] + (R - 4) * math.cos(a):.1f},{c[1] + (R - 4) * math.sin(a):.1f}', 1.2)
    s.add('</g>')
    s.circle(c, 3.2, '#CBD5E1')


def _leg_frames(phase):
    # Thigh + shin and shoe paths for every frame of one crank turn
    legs, shoes = [], []
    for i in range(N_FRAMES + 1):
        th = phase + 2 * math.pi * i / N_FRAMES
        pedal = (BB[0] + CRANK * math.cos(th), BB[1] + CRANK * math.sin(th))
        knee = _ik(HIP, pedal, THIGH, SHIN)
        legs.append(f'M{_p(HIP)} L{_p(knee)} L{_p(pedal)}')
        shoes.append(f'M{pedal[0] - 6:.1f},{pedal[1] - 1:.1f} L{pedal[0] + 9:.1f},{pedal[1] + 1:.1f}')
    return ';'.join(legs), ';'.join(shoes), legs[0], shoes[0]


def _bike(s, bike):
    # Frame, fork, saddle, bars and chainring
    col = _tint(bike['color'])
    st_top, ht_top, ht_bot, tw = bike['st_top'], bike['ht_top'], bike['ht_bot'], bike['tube']
    s.line(f'M{BB[0]},{BB[1] - 10} L{RA[0]},{RA[1] - 4} M{BB[0]},{BB[1] + 10} L{RA[0]},{RA[1] + 4}', 1)
    clamp = (st_top[0] - 0.292 * (st_top[1] - SADDLE_Y - 3) / 0.956, SADDLE_Y + 3)
    s.line(f'M{_p(st_top)} L{_p(clamp)}', 2.2)
    x = clamp[0]
    s.shape(f'M{x - 12:.1f},{SADDLE_Y - 1} Q{x:.1f},{SADDLE_Y + 3} {x + 12:.1f},{SADDLE_Y} '
            f'L{x + 12:.1f},{SADDLE_Y + 3} Q{x:.1f},{SADDLE_Y + 6} {x - 12:.1f},{SADDLE_Y + 3} Z', '#94A3B8')
    if bike.get('frame_bag'):
        s.shape(f'M{st_top[0] + 6},{st_top[1] + 5} L{ht_bot[0] - 10},{ht_top[1] + 7} '
                f'L{ht_bot[0] - 14},{ht_bot[1] + 2} L{BB[0] + 8},{BB[1] - 26} Z', '#A1A1AA')
    s.tube(f'M{_p(RA)} L{_p(BB)}', col, tw * 0.75)                          # chainstay
    s.tube(f'M{_p(RA)} L{st_top[0] + 1},{st_top[1] + 3}', col, tw * 0.7)     # seatstay
    s.tube(f'M{_p(BB)} L{_p(st_top)}', col, tw)                             # seat tube
    s.tube(f'M{_p(st_top)} L{_p(ht_top)}', col, tw)                         # top tube
    s.tube(f'M{_p(BB)} L{_p(ht_bot)}', col, tw + 1)                         # down tube
    s.tube(f'M{_p(ht_top)} L{_p(ht_bot)}', col, tw + 2)                     # head tube
    if bike.get('suspension'):
        mid = (ht_bot[0] + (FA[0] - ht_bot[0]) * 0.55, ht_bot[1] + (FA[1] - ht_bot[1]) * 0.55)
        s.tube(f'M{_p(ht_bot)} L{_p(mid)}', '#E2E8F0', 4.2)
        s.tube(f'M{mid[0] - 0.5:.1f},{mid[1] - 3:.1f} L{_p(FA)}', '#94A3B8', 6)
    else:
        s.tube(f'M{_p(ht_bot)} Q{ht_bot[0] + 6},{(ht_bot[1] + FA[1]) / 2} {_p(FA)}', col, tw * 0.8)
    s.add(f'<circle cx="{BB[0]}" cy="{BB[1]}" r="10" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    sx, sy = ht_top[0] + 11, ht_top[1] - 3                                  # stem end
    s.line(f'M{ht_top[0]},{ht_top[1]} L{ht_top[0] - 0.5},{ht_top[1] - 4} L{sx},{sy}', 2.4)
    if bike['bar'] == 'drop':
        s.line(f'M{sx},{sy} L{sx + 6},{sy} C{sx + 13},{sy} {sx + 14},{sy + 9} {sx + 11},{sy + 14} '
               f'C{sx + 9},{sy + 18} {sx + 4},{sy + 19} {sx},{sy + 18}', 2.4)
        s.line(f'M{sx + 5},{sy - 2.5} L{sx + 10},{sy - 1}', 3.2)
    else:
        s.line(f'M{sx},{sy} L{sx + 2},{sy - 8}', 2.4)
        s.line(f'M{sx + 2},{sy - 8} L{sx - 7},{sy - 10}', 3.5)


def _head(s, rider, hx, hy):
    # Hair, head, helmet and face; the same face for every rider
    q = 16 / 13
    style = rider['hair_style']
    if style == 'ponytail':
        bx, by = hx - 12 * q, hy - 2 * q
        p1 = (f'M{bx:.1f},{by - 3:.1f} C{bx - 8:.1f},{by - 8:.1f} {bx - 18:.1f},{by - 4:.1f} {bx - 27:.1f},{by + 2:.1f} '
              f'C{bx - 19:.1f},{by + 7:.1f} {bx - 9:.1f},{by + 9:.1f} {bx + 1:.1f},{by + 5:.1f} Z')
        p2 = (f'M{bx:.1f},{by - 3:.1f} C{bx - 8:.1f},{by - 5:.1f} {bx - 18:.1f},{by - 9:.1f} {bx - 27:.1f},{by - 4:.1f} '
              f'C{bx - 19:.1f},{by + 4:.1f} {bx - 9:.1f},{by + 8:.1f} {bx + 1:.1f},{by + 5:.1f} Z')
        swing = f'<animate attributeName="d" values="{p1};{p2};{p1}" dur="0.5s" repeatCount="indefinite"/>'
        s.shape(p1, rider['hair'], inner=swing)
    if style == 'puff':
        cx, cy = hx - 14 * q, hy - 1 * q
        for ox, oy, r in ((-4, -4, 6.5), (-6, 3, 6.5), (1, 5, 6), (2, -5, 6), (-1, 0, 7)):
            s.circle((cx + ox * q, cy + oy * q), r * q, rider['hair'], 1.4)
    s.circle((hx, hy), 16, rider['skin'])
    # hair at the nape, under the helmet
    nape = 9.5 if style != 'short' else 9
    s.shape(f'M{hx - 13 * q:.1f},{hy - 1 * q:.1f} Q{hx - 14.5 * q:.1f},{hy + 8 * q:.1f} {hx - 8 * q:.1f},{hy + nape * q:.1f} '
            f'Q{hx - 10 * q:.1f},{hy + 2 * q:.1f} {hx - 5 * q:.1f},{hy - 3 * q:.1f} Z', rider['hair'])
    if style == 'puff':
        for ox, oy in ((-3, 3), (-1, 6)):
            s.circle((hx + ox * q - 6, hy + oy * q - 3), 2.2 * q, rider['hair'], 1.1)
    s.add(f'<circle cx="{hx - 4 * q:.1f}" cy="{hy + 2 * q:.1f}" r="{2.6 * q:.1f}" fill="{rider["skin_shade"]}" '
          f'stroke="{INK}" stroke-width="1.2"/>')                          # ear
    if rider['earring']:
        s.add(f'<circle cx="{hx - 4 * q:.1f}" cy="{hy + 5.4 * q:.1f}" r="1.6" fill="#FACC15" stroke="{INK}" stroke-width=".8"/>')
    s.shape(f'M{hx - 16 * q:.1f},{hy - 1 * q:.1f} C{hx - 16 * q:.1f},{hy - 18 * q:.1f} {hx + 10 * q:.1f},{hy - 22 * q:.1f} '
            f'{hx + 16 * q:.1f},{hy - 5 * q:.1f} L{hx + 18 * q:.1f},{hy - 3 * q:.1f} L{hx + 9 * q:.1f},{hy - 3 * q:.1f} '
            f'Q{hx:.1f},{hy - 7 * q:.1f} {hx - 16 * q:.1f},{hy - 1 * q:.1f} Z', HELMET)
    # eye with a white so it reads on every skin tone, smile, nose
    ex, ey = hx + 6.5 * q, hy + 1 * q
    s.add(f'<ellipse cx="{ex + 0.4:.1f}" cy="{ey:.1f}" rx="2.6" ry="2.2" fill="#FFFFFF"/>')
    s.add(f'<circle cx="{ex + 0.9:.1f}" cy="{ey:.1f}" r="1.5" fill="{INK}"/>')
    if rider['glasses']:
        s.add(f'<path d="M{ex - 3.4 * q:.1f},{ey:.1f} L{hx - 2.5 * q:.1f},{ey - 0.5:.1f}" stroke="{INK}" stroke-width="1.3" fill="none"/>')
        s.add(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{3.4 * q:.1f}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    else:
        s.line(f'M{ex + 1.5:.1f},{ey - 2.4:.1f} L{ex + 3.6:.1f},{ey - 3.8:.1f}', 1.1)   # lashes
    s.add(f'<path d="M{hx + 7.5 * q:.1f},{hy + 7.5 * q:.1f} Q{hx + 10.5 * q:.1f},{hy + 9.5 * q:.1f} {hx + 12.5 * q:.1f},{hy + 6 * q:.1f}" '
          f'fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')
    s.add(f'<path d="M{hx + 12.6 * q:.1f},{hy + 0.5 * q:.1f} Q{hx + 15.6 * q:.1f},{hy + 3 * q:.1f} {hx + 12.4 * q:.1f},{hy + 4 * q:.1f}" '
          f'fill="none" stroke="{INK}" stroke-width="1.2"/>')


def _neckwear(s, rider, x, y):
    # Tie or silk scarf, flying back over the shoulder
    w = 1.0 if rider['neckwear'] == 'tie' else 1.6
    t1 = (f'M{x:.1f},{y - 1.5 * w:.1f} C{x - 10:.1f},{y - 7:.1f} {x - 20:.1f},{y - 1:.1f} {x - 34:.1f},{y - 10:.1f} '
          f'L{x - 41:.1f},{y - 4:.1f} L{x - 33:.1f},{y:.1f} C{x - 16:.1f},{y + 4 * w:.1f} {x - 8:.1f},{y + 1:.1f} {x:.1f},{y + 1.5 * w:.1f} Z')
    t2 = (f'M{x:.1f},{y - 1.5 * w:.1f} C{x - 10:.1f},{y - 1:.1f} {x - 20:.1f},{y - 11:.1f} {x - 34:.1f},{y - 6:.1f} '
          f'L{x - 40:.1f},{y + 1:.1f} L{x - 33:.1f},{y + 2:.1f} C{x - 16:.1f},{y - 3 * w:.1f} {x - 8:.1f},{y + 4:.1f} {x:.1f},{y + 1.5 * w:.1f} Z')
    flap = f'<animate attributeName="d" values="{t1};{t2};{t1}" dur="0.4s" repeatCount="indefinite"/>'
    s.shape(t1, rider['neck_color'], inner=flap)
    if rider['neckwear'] == 'tie':
        s.shape(f'M{x - 2:.1f},{y - 2.5:.1f} L{x + 2.5:.1f},{y - 2:.1f} L{x + 2:.1f},{y + 2.5:.1f} L{x - 2.5:.1f},{y + 2:.1f} Z',
                rider['neck_color'])
    else:
        s.circle((x, y), 3.2, rider['neck_color'], 1.4)


def rider_svg(product):
    # Full animated SVG of the rider on the bike for one product
    bike, rider = BIKES[product], RIDERS[product]
    s = Sketch()
    s.add('<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -1.2;0 0" '
          'dur="0.45s" repeatCount="indefinite"/>')
    for y, x, length, delay in ((120, 4, 22, 0), (142, 0, 30, 0.2), (98, 10, 16, 0.4)):
        s.add(f'<path d="M{x},{y} h{length}" stroke="{INK}" stroke-width="1.4" stroke-linecap="round" opacity="0">'
              f'<animate attributeName="opacity" values="0;.9;0" dur="0.9s" begin="{delay}s" repeatCount="indefinite"/></path>')
    _wheel(s, RA, bike)
    _wheel(s, FA, bike)

    # far leg and far crank, behind the frame
    spin = (f'<animateTransform attributeName="transform" type="rotate" from="0 {BB[0]} {BB[1]}" '
            f'to="360 {BB[0]} {BB[1]}" dur="{CRANK_DUR}s" repeatCount="indefinite"/>')
    s.add(f'<g>{spin}')
    s.line(f'M{_p(BB)} L{BB[0]},{BB[1] - CRANK}', 2.4)
    s.add('</g>')
    legs, shoes, leg0, shoe0 = _leg_frames(math.pi * 1.5)
    s.tube(leg0, TROUSERS_FAR, 10.5, legs)
    s.tube(shoe0, _tint(rider['shoe'], 0.2), 6, shoes)

    _bike(s, bike)
    s.add(f'<g>{spin}')
    s.line(f'M{_p(BB)} L{BB[0]},{BB[1] + CRANK}', 2.8)
    s.add('</g>')
    s.circle(BB, 3, '#CBD5E1')

    # torso direction and helpers
    S, H = bike['shoulder'], HIP
    length = math.hypot(S[0] - H[0], S[1] - H[1])
    ux, uy = (S[0] - H[0]) / length, (S[1] - H[1]) / length
    fx, fy = (-uy, ux) if ux > 0 else (uy, -ux)                          # chest side

    def off(pt, along, front):
        return (pt[0] + ux * along + fx * front, pt[1] + uy * along + fy * front)

    hands = bike['hands']
    far_sh, far_hand = (S[0] - 3, S[1] + 1), (hands[0] - 3, hands[1] + 1)
    s.tube(f'M{_p(far_sh)} L{_p(_ik(far_sh, far_hand, UPPER_ARM, FOREARM))} L{_p(far_hand)}', rider['blazer_far'], 8)
    s.circle((hands[0] - 2, hands[1] + 1), 4, rider['skin_shade'])

    legs, shoes, leg0, shoe0 = _leg_frames(math.pi / 2)
    s.tube(leg0, TROUSERS, 11, legs)
    s.tube(shoe0, rider['shoe'], 6.5, shoes)

    # blazer with tails over the saddle, shirt front, lapel, buttons
    tf, tb = off(H, -9, 7), off(H, -14, -6)
    torso = (f'M{_p(tf)} L{_p(tb)} C{_p(off(H, 0, -12))} {_p(off(S, -14, -12))} {_p(off(S, -2, -10))} '
             f'Q{_p(off(S, 7, -10))} {_p(off(S, 8, -1))} Q{_p(off(S, 9, 9))} {_p(off(S, 1, 10))} '
             f'L{_p(off(H, 8, 11))} Q{_p(off(H, -4, 13))} {_p(tf)} Z')
    s.shape(torso, rider['blazer'])
    s.shape(f'M{_p(off(S, 6, 4))} L{_p(off(S, 3, 10))} L{_p(off(S, -17, 10.5))} Z', '#FFFFFF')
    s.line(f'M{_p(off(S, 5, 2.5))} L{_p(off(S, -18, 9))}', 1.3)
    for a in (-24, -32):
        b = off(S, a, 9.5)
        s.add(f'<circle cx="{b[0]:.1f}" cy="{b[1]:.1f}" r="1.1" fill="{INK}"/>')

    # near arm, in front of the body
    elbow = _ik(S, hands, UPPER_ARM, FOREARM)
    s.tube(f'M{_p(S)} L{_p(elbow)} L{_p(hands)}', rider['blazer'], 9)
    cuff = (hands[0] - (hands[0] - elbow[0]) * 0.17, hands[1] - (hands[1] - elbow[1]) * 0.17)
    s.circle(cuff, 3.6, '#FFFFFF')
    s.circle(hands, 4.4, rider['skin'])
    # neck and head, drawn last so the face is never hidden
    hx, hy = S[0] + ux * 18 + 5, S[1] + uy * 18 - 8
    s.tube(f'M{_p(off(S, 3, 2))} L{hx - 3:.1f},{hy + 10:.1f}', rider['skin'], 8)
    _head(s, rider, hx, hy)
    nx, ny = off(S, 8, 8)
    _neckwear(s, rider, nx, ny)

    s.add('</g>')

    rough = ('<defs><filter id="rough" x="-5%" y="-5%" width="110%" height="110%">'
             '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/>'
             '<feDisplacementMap in="SourceGraphic" scale="2.2" xChannelSelector="R" yChannelSelector="G"/>'
             '</filter></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 210">{rough}'
            f'<g filter="url(#rough)">{"".join(s.out)}</g></svg>')


def _url(svg):
    # SVG text as a CSS data URL
    return 'url("data:image/svg+xml,' + quote(svg, safe=" /=:;,.-_()'") + '")'


HILLS = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 120" preserveAspectRatio="none">'
         '<path d="M0,72 C80,32 150,42 230,67 C310,92 380,22 470,37 C530,47 570,62 600,60" fill="none" stroke="#94A3B8" stroke-width="1.6" stroke-linecap="round"/>'
         '<path d="M0,97 C90,72 170,82 260,94 C360,107 430,72 520,80 C560,84 585,92 600,94" fill="none" stroke="#64748B" stroke-width="1.8" stroke-linecap="round"/>'
         '<path d="M40,100 l8,-8 M60,98 l8,-8 M80,96 l8,-8 M300,100 l8,-8 M320,102 l8,-8 M480,86 l8,-8 M500,85 l8,-8" stroke="#94A3B8" stroke-width="1.2"/></svg>')
FLAG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 70">'
        '<path d="M5.5,4 L6,69" stroke="#1E293B" stroke-width="2.2" stroke-linecap="round"/>'
        '<path d="M7,6 C15,3 22,9 37,6 L37,26 C22,29 15,23 7,26 Z" fill="none" stroke="#1E293B" stroke-width="1.6"/>'
        '<path d="M7,6h7.5v5h-7.5zM22,7h7.5v5h-7.5zM14.5,11h7.5v5h-7.5zM29.5,11h7.5v5h-7.5zM7,16h7.5v5h-7.5zM22,16h7.5v5h-7.5zM14.5,21h7.5v5h-7.5z" fill="#1E293B" opacity=".75"/></svg>')
SUN = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80">'
       '<circle cx="40" cy="40" r="16" fill="#FDE68A" fill-opacity=".6" stroke="#1E293B" stroke-width="1.6"/>'
       '<path d="M40,12v8M40,60v8M12,40h8M60,40h8M20,20l6,6M54,54l6,6M60,20l-6,6M26,54l-6,6" stroke="#1E293B" stroke-width="1.6" stroke-linecap="round"/></svg>')


def loading_css(default_product):
    # CSS for Gradio's loading overlay; default_product is the Product dropdown's start value
    draft = '#draft-box [data-testid="status-tracker"]:not(.hide)'
    mini = '.ih-quality [data-testid="status-tracker"]:not(.hide)'
    quiet = ('#feedback-box [data-testid="status-tracker"]:not(.hide), '
             '.ih-status [data-testid="status-tracker"]:not(.hide)')
    ease = 'cubic-bezier(.25,.6,.35,1)'
    css = f"""
/* ---- Loading animation (look only, see loading_animation.py) ---- */
{draft} {{
  background: {_url(SUN)} right 18% top 14px / 64px 64px no-repeat,
              {_url(FLAG)} right 14px bottom 30px / 34px 60px no-repeat,
              linear-gradient(#94A3B8, #94A3B8) left 0 bottom 22px / 100% 2px no-repeat,
              linear-gradient(#EFE9DC, #EFE9DC) left 0 bottom 0 / 100% 46px no-repeat,
              {_url(HILLS)} left 0 bottom 44px / 100% 110px no-repeat,
              #FBF8F1 !important;
  opacity: 1 !important; border-radius: inherit; overflow: hidden;
}}
{draft} svg, {draft} .eta-bar {{ display: none !important; }}
{draft} .progress-text {{
  top: 12px; right: 14px; bottom: auto; background: rgba(255,255,255,.8); color: #475569;
  border-radius: 999px; padding: 2px 10px; font-size: 12px;
}}
{draft} .margin::before {{
  content: "Your draft is on its way…"; position: absolute; left: 20px; top: 46px; color: {INK};
  font: 600 21px 'Segoe Print', 'Bradley Hand', 'Chalkboard SE', 'Comic Sans MS', cursive;
}}
{draft}::before {{
  content: ""; position: absolute; left: 0; bottom: 21px; height: 4px;
  background: repeating-linear-gradient(90deg, {INK} 0 10px, transparent 10px 16px);
  animation: ih-trail {RIDE_SECONDS}s {ease} forwards;
}}
{draft}::after {{
  content: ""; position: absolute; bottom: 10px; width: 216px; height: 189px;
  background: var(--ih-rider) center / contain no-repeat;
  animation: ih-ride {RIDE_SECONDS}s {ease} forwards;
}}
@keyframes ih-ride {{ from {{ left: -40px; }} to {{ left: max(10px, calc(100% - 270px)); }} }}
@keyframes ih-trail {{ from {{ width: 0; }} to {{ width: max(0px, calc(100% - 150px)); }} }}

/* Quality box: white, same rider, small */
.ih-quality:has([data-testid="status-tracker"]:not(.hide)) {{ min-height: 74px; }}
{mini} {{ inset: 0 !important; height: auto !important; background: #FFFFFF !important;
  opacity: 1 !important; border-radius: inherit; overflow: hidden; }}
{mini} svg, {mini} .progress-text {{ display: none !important; }}
{mini}::after {{
  content: ""; position: absolute; bottom: 4px; width: 74px; height: 65px;
  background: var(--ih-rider) center / contain no-repeat;
  animation: ih-ride-mini {RIDE_SECONDS}s {ease} forwards;
}}
@keyframes ih-ride-mini {{ from {{ left: -20px; }} to {{ left: max(4px, calc(100% - 96px)); }} }}

/* Feedback and status boxes: no logo, plain white */
{quiet} {{ background: #FFFFFF !important; opacity: 1 !important; }}
{quiet} svg, {quiet} .progress-text {{ display: none !important; }}

/* Phones: smaller rider */
@media (max-width: 640px) {{ {draft}::after {{ width: 150px; height: 131px; }} }}
"""
    # Which rider: follows body[data-product]; the dropdown's start value is the fallback
    css += f"body {{ --ih-rider: {_url(rider_svg(default_product))}; }}\n"
    for product in BIKES:
        css += f'body[data-product="{product}"] {{ --ih-rider: {_url(rider_svg(product))}; }}\n'
    return css


# Runs in the browser only: stores the selected product on the page for the CSS above
PRODUCT_JS = "(product) => { document.body.dataset.product = product; return []; }"


if __name__ == '__main__':
    # Card check: every rider is valid SVG and the CSS has a rule per product
    import xml.etree.ElementTree as ET
    for name in BIKES:
        ET.fromstring(rider_svg(name))
        print(f'PASS rider_svg({name!r}) is valid SVG')
    css = loading_css('gravel')
    missing = [p for p in BIKES if f'body[data-product="{p}"]' not in css]
    print('PASS CSS has a rider for every product' if not missing else f'FAIL missing: {missing}')
    print(f'CSS size: {len(css) // 1024} KB')
