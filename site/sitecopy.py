"""Namaste Bead Shop (namastebeadshop.com): malas, prayer beads and meditation tools. All copy is written for this site only."""
import re, collections
from copybase import E, stone_color, intent_color, kinds_phrase, kind_one, plist, tradition, hood_list, HOODS as HOOD_DATA

SEED = re.compile(r'rudraksh|sandalwood|\bwood|rosewood|tulsi|bodhi|lotus seed|raktu|bone|palo santo', re.I)
PRAYER = re.compile(r'\bmala\b|karma|buddha|\bom\b|chakra|prayer|tassel|guru|mantra|lotus|ganesh|meditat|tibet', re.I)
AISLES = {
 'm108':  ('108-Bead Malas', '108 Malas', '108-bead-malas', 'Full japa malas: 108 beads, a guru bead and usually a tassel, in stone, seed and wood.', '#e8a317'),
 'wrist': ('Wrist Malas & Prayer Bracelets', 'Wrist Malas', 'wrist-malas', '27- and 54-bead wrist malas, karma bead and chakra bracelets for everyday wear.', '#b8862b'),
 'seed':  ('Rudraksha, Sandalwood & Wood', 'Seed & Wood', 'rudraksha-sandalwood-wood', 'Rudraksha seeds, sandalwood, tulsi, bone and other natural materials.', '#7a4a2b'),
 'tools': ('Meditation Tools', 'Tools', 'meditation-tools', 'Singing bowls, bells, tingsha, dorje and chakra tuning forks.', '#4f7894'),
}
def assign(x):
    t = x['title']; b = x['base']
    if b == 'meditation': return 'tools'
    if b == 'mala' or (b in ('necklace',) and re.search(r'\bmala\b', t, re.I)):
        return 'm108' if re.search(r'108', t) and not re.search(r'wrist|bracelet', t, re.I) else ('seed' if SEED.search(t) and not x['stones'][:1] in ([],) and x['stones'][0] in ('rudraksha', 'sandalwood', 'wood') else 'wrist')
    if b in ('beaded', 'bracelet'):
        if SEED.search(t): return 'seed'
        if PRAYER.search(t): return 'wrist'
    return None
LABELS = {'stone': 'Bead', 'metal': 'Strung on'}
PRICE_BANDS = [('0-15', 'Under $15'), ('0-30', 'Under $30'), ('30-60', '$30 to $60'), ('60-99999', '$60 and up')]
BRAND_BANDS = [('Under $20', 0, 20), ('$20 to $50', 20, 50), ('$50 and up', 50, 1e9)]
STONE_MIN = 3; INTENT_MIN = 3; NAV_INTENTS = True

VISIT_EYEBROW = 'Hold a mala before you choose'
def STORE_DESC(S): return f'Mala and meditation shop by Union Square in Manhattan: about {S.ABOUT_N:,} 108-bead malas, wrist malas, rudraksha and sandalwood beads, singing bowls and bells.'
REVIEW_TITLE = 'Found your mala here?'
REVIEW_TEXT = 'A short Google review helps others looking for malas and prayer beads near Union Square.'
LOGO_SVG = '<svg viewBox="0 0 40 40"><g fill="#e8a317"><circle cx="20" cy="6" r="2.8"/><circle cx="28" cy="9.4" r="2.8"/><circle cx="31.4" cy="17" r="2.8"/><circle cx="28.6" cy="25" r="2.8"/><circle cx="11.4" cy="25" r="2.8"/><circle cx="8.6" cy="17" r="2.8"/><circle cx="12" cy="9.4" r="2.8"/></g><circle cx="20" cy="29" r="3.2" fill="currentColor"/><path d="M20 32v7" stroke="#e8a317" stroke-width="2.4"/></svg>'
WORDMARK = 'Namaste <b>Bead Shop</b>'
BAR_TEXT = 'Malas & prayer beads at 2 West 14th Street'
SEARCH_PLACEHOLDER = 'Search malas, rudraksha, sandalwood, singing bowls'
QUIZ = {
 'slug': 'mala-finder', 'nav': 'Mala finder', 'cta': 'Find my mala',
 'title': 'Mala Finder: Choose a Mala or Prayer Bracelet', 'desc': 'Three questions to choose a mala, wrist mala or meditation tool from what is in stock at 2 West 14th Street.',
 'h1': 'Mala finder', 'lead': 'Tell us how you will use it and we will show in-stock malas. The quiz runs in your browser and saves nothing.', 'submit': 'Show malas',
 'questions': [
  {'q': 'How will you use it?', 'options': [{'label': 'Counting mantras or breaths (full 108)', 'filter': {'aisle': ['m108']}}, {'label': 'Wearing every day on the wrist', 'filter': {'aisle': ['wrist', 'seed']}}, {'label': 'Sound for my practice', 'filter': {'aisle': ['tools']}}]},
  {'q': 'Which material calls to you?', 'options': [{'label': 'Stone', 'filter': {'nq': 'rudraksh|sandalwood|wood|tulsi|bone|brass|bell|bowl|fork'}}, {'label': 'Seed or wood', 'filter': {'stone': ['rudraksha', 'sandalwood', 'wood']}}, {'label': 'No preference', 'filter': {}}]},
  {'q': 'Budget?', 'options': [{'label': 'Under $20', 'filter': {'maxp': 20}}, {'label': 'Under $50', 'filter': {'maxp': 50}}, {'label': 'Any', 'filter': {}}]},
 ]}
def FOOTER_EXPLORE(S):
    return [('How to use a mala', '/guide/how-to-use-a-mala/'), ('Why 108 beads?', '/guide/why-108-beads/'), ('Choosing a mala', '/guide/choosing-a-mala/'), ('Mala care', '/guide/mala-care/'),
            ('Mala finder', '/mala-finder/'), ('Malas by stone', '/stones/'), ('Meditation shop in Manhattan', '/meditation-shop-manhattan/')]
FOOT_BLURB = 'Malas, prayer beads and the bells and bowls that go with them, a few minutes from Union Square.'
HERO_BASES = ('mala', 'beaded')
def HERO(S):
    return {'eyebrow': 'Malas &middot; Prayer beads &middot; Meditation &middot; 2 West 14th Street',
            'h1': 'One hundred and eight beads, <em>one breath at a time.</em>',
            'lede': f'{S.cat_count["m108"]} full 108-bead malas, {S.cat_count["wrist"] + S.cat_count["seed"]} wrist malas and prayer bracelets in stone, rudraksha and sandalwood, and {S.cat_count["tools"]} singing bowls, bells and tuning forks. Open daily from 11 AM near Union Square.' + (f' Reserve online; {S.READY.lower()}.' if S.PICKUP_ON else ''),
            'shop_cta': 'Shop malas'}
def _how(S):
    return '''<section class="wrap"><div class="sechead"><h2>New to malas?</h2><a href="/guide/how-to-use-a-mala/">Full guide &rarr;</a></div><ol class="steps" style="color:var(--ink)">
<li><b>Hold it in your right hand</b><span>Drape the mala over your middle finger, with the guru bead (the larger bead by the tassel) at the start.</span></li>
<li><b>Move one bead per repetition</b><span>Use your thumb to draw each bead toward you as you say a mantra, an affirmation or take a breath.</span></li>
<li><b>Stop at the guru bead</b><span>In many traditions you do not cross it; turn the mala around to begin another round.</span></li></ol></section>'''
def _near(S): return f'<section class="wrap"><div class="sechead"><h2>Coming to the shop from</h2></div>{hood_list(S, "/near/")}</section>'
def _whys(S):
    return [(f'{S.cat_count["m108"]} full malas', '108 beads plus a guru bead, in stone, rudraksha, wood and bone.'),
            ('Wrist malas', '27- and 54-bead strands and stretch prayer bracelets.'),
            (('Reserve, then collect', f'Pickup at checkout; orders are {S.READY.lower()}.') if S.PICKUP_ON else ('', '')),
            ('Sound tools too', 'Singing bowls, tingsha, bells and tuning forks for your practice.'),
            ('Hold before you choose', 'Weight and feel matter with a mala; come try a few.'),
            ('Open every day', 'From 11 AM, near Union Square.')]
def _m108(S): return S.by_rank([x for x in S.leaders if x['aisle'] == 'm108'])[:8]
def _wrist(S): return S.by_rank([x for x in S.leaders if x['aisle'] in ('wrist', 'seed') and not x['noimg']])[:8]
def _tools(S): return S.by_rank([x for x in S.leaders if x['aisle'] == 'tools' and not x['noimg']])[:4]
HOME_SECTIONS = [
 {'type': 'grid', 'title': '108-bead malas', 'select': _m108, 'href': '/shop/108-bead-malas/', 'link': 'All 108 malas'},
 {'type': 'html', 'html': _how},
 {'type': 'visit'},
 {'type': 'grid', 'title': 'Wrist malas & prayer bracelets', 'select': _wrist, 'href': '/shop/wrist-malas/', 'link': 'All wrist malas'},
 {'type': 'collections', 'title': 'By material', 'items': [
   {'title': 'Rudraksha', 'blurb': 'The seed of the rudraksha tree.', 'href': '/stones/rudraksha/', 'filter': {'stone': ['rudraksha']}},
   {'title': 'Sandalwood & wood', 'blurb': 'Warm, light and fragrant.', 'href': '/stones/wood/', 'filter': {'stone': ['wood', 'sandalwood']}},
   {'title': 'Stone malas', 'blurb': 'Tiger\'s eye, rose quartz, obsidian.', 'href': '/stone-malas/', 'filter': {'base': ['mala'], 'nq': 'rudraksh|sandalwood|wood|tulsi|bone'}},
   {'title': 'Chakra beads', 'blurb': 'Seven colors, seven stones.', 'href': '/intentions/chakra/', 'filter': {'intent': ['chakra']}}]},
 {'type': 'grid', 'title': 'Bowls, bells & forks', 'select': _tools, 'href': '/shop/meditation-tools/', 'link': 'All tools'},
 {'type': 'whys', 'title': 'Why shop malas here', 'items': _whys},
 {'type': 'quiz', 'title': 'Which mala is right for you?', 'text': 'Three questions about how you will use it.'},
 {'type': 'brands', 'title': 'Makers', 'n': 8},
 {'type': 'html', 'html': _near},
 {'type': 'review'},
 {'type': 'band', 'title': 'Reserve your mala', 'text': lambda S: 'Every mala online is a live listing. Reserve and collect on 14th Street, or ship it from New York City.',
  'steps': lambda S: [('Choose', 'Filter by bead, material and price.'), ('Pick Pickup', f'Secure Shopify checkout. {S.READY or "Usually ready the same day"}.'), ('Collect', S.STORE_ADDR + '.')]},
]
def HOME_TITLE(S): return 'Namaste Bead Shop | Malas, Prayer Beads & Meditation near Union Square NYC'
def HOME_DESC(S): return f'108-bead malas, wrist malas, rudraksha and sandalwood prayer beads, singing bowls and bells at {S.STORE_ADDR}, by Union Square. Mala guides, pickup or ship.'
def SHOP_TITLE(S): return 'Shop Malas & Prayer Beads Online | Namaste Bead Shop NYC'
def SHOP_DESC(S): return f'{S.N:,} malas, prayer bracelets and meditation tools from {S.money(S.MIN_PRICE)}. Pick up at 2 West 14th Street, Manhattan, or ship.'
SHOP_H1 = 'Malas, prayer beads & tools'
def SHOP_SUB(S): return f'{S.N:,} pieces. Filter by bead, price, style and maker.'
def AISLE_TITLE(S, k): return f'{AISLES[k][0]} in NYC | Namaste Bead Shop'
def AISLE_DESC(S, k): return f'{AISLES[k][3]} {S.cat_count[k]} at 2 West 14th Street by Union Square.'
def LANDINGS(S):
    return [{'path': '/stone-malas/', 'title': 'Gemstone Malas: Tiger Eye, Rose Quartz & More | Namaste Bead Shop', 'desc': 'Natural stone malas with guru bead and tassel at 2 West 14th Street, Manhattan.', 'h1': 'Stone malas', 'sub': 'Malas strung in natural stone.', 'filter': {'base': ['mala'], 'nq': 'rudraksh|sandalwood|wood|tulsi|bone'}},
            {'path': '/singing-bowls/', 'title': 'Singing Bowls in NYC near Union Square | Namaste Bead Shop', 'desc': 'Brass singing bowls and strikers at 2 West 14th Street.', 'h1': 'Singing bowls', 'sub': 'Brass bowls for sound practice.', 'filter': {'aisle': ['tools'], 'q': 'bowl'}},
            {'path': '/tingsha-bells/', 'title': 'Tingsha, Bells & Dorje | Namaste Bead Shop NYC', 'desc': 'Tibetan tingsha cymbals, hand bells and dorje at 2 West 14th Street.', 'h1': 'Tingsha, bells & dorje', 'sub': 'Bells and ritual tools.', 'filter': {'aisle': ['tools'], 'q': 'bell|tingsha|dorje|vajra'}},
            {'path': '/chakra-tuning-forks/', 'title': 'Chakra Tuning Forks | Namaste Bead Shop NYC', 'desc': 'Weighted chakra tuning forks at 2 West 14th Street near Union Square.', 'h1': 'Chakra tuning forks', 'sub': 'A fork for each of the seven chakras.', 'filter': {'aisle': ['tools'], 'q': 'fork'}}]
def stone_tile(S, k): return f'{S.stone_any[k]} strands'
def STONE_PAGE(S, k, xs):
    n = S.STONE_NAME[k]; tr = tradition(S, k)
    note = {'rudraksha': 'Rudraksha beads are the dried seeds of the Elaeocarpus tree, long used for malas in Hindu and Buddhist practice.',
            'sandalwood': 'Sandalwood beads are light and keep a soft scent; they are a common choice for wrist malas.',
            'wood': 'Wood, seed and bone beads are light in the hand and warm to the touch.'}.get(k, '')
    return {'title': f'{n} Malas & Prayer Beads | Namaste Bead Shop NYC', 'desc': f'{len(xs)} {n.lower()} malas and prayer bracelets at 2 West 14th Street near Union Square.',
            'h1': f'{n} malas & prayer beads', 'sub': f'{len(xs)} pieces',
            'intro': (f'<p class="intro">{E(note)}</p>' if note else '') + (f'<p class="note-belief">In crystal tradition {E(n.lower())} is linked with {plist(tr)}. We share it as belief.</p>' if tr else ''),
            'faq': [(f'Do you have {n.lower()} 108-bead malas?', f'{sum(1 for x in xs if x["aisle"] == "m108")} right now; the rest are wrist malas and bracelets.')]}
def intent_tile(S, k): return f'{S.intent_count[k]} pieces'
def INTENT_PAGE(S, k, xs):
    n = S.INTENT_NAME[k]
    return {'title': f'Malas & Prayer Beads for {n} | Namaste Bead Shop', 'desc': f'{len(xs)} malas and prayer bracelets chosen for {n.lower()}, at 2 West 14th Street.', 'h1': f'Malas for {n.lower()}', 'sub': f'{len(xs)} pieces',
            'intro': '<p class="note-belief">Many people pick mala beads for the intention tradition gives them. The practice is what you bring to it; we make no claims for the beads themselves.</p>', 'faq': []}
def STONES_HUB(S): return {'title': 'Malas by Bead & Material | Namaste Bead Shop', 'desc': 'Malas and prayer beads by stone, seed and wood.', 'h1': 'By bead', 'lead': 'Stone, rudraksha, sandalwood, wood and bone.'}
def INTENTS_HUB(S): return {'title': 'Malas by Intention | Namaste Bead Shop', 'desc': 'Malas grouped by the intention tradition gives each bead.', 'h1': 'By intention', 'lead': 'Set an intention, then choose the beads tradition pairs with it.'}
def brand_intro(S, k, st): return f'<p>{st["n"]} {E(S.BRAND_NAME[k])} piece{"s" if st["n"] != 1 else ""} for practice: {kinds_phrase(S.kinds_of(st["xs"]))}, from {S.money(st["min"])}.</p>'
def brand_faq(S, k, st): return [(f'Where can I find {S.BRAND_NAME[k]} near Union Square?', f'At {S.STORE_ADDR}; {st["n"]} pieces today.')]
def BRAND_H1(S, k): return f'{S.BRAND_NAME[k]} at Namaste Bead Shop'
def BRAND_TITLE(S, k, st): return f'{S.BRAND_NAME[k]} Malas & Prayer Beads | Namaste Bead Shop'
def BRAND_DESC(S, k, st): return f'{st["n"]} {S.BRAND_NAME[k]} pieces from {S.money(st["min"])} at 2 West 14th Street.'
def BRANDS_TITLE(S): return 'Mala & Meditation Brands | Namaste Bead Shop'
def BRANDS_DESC(S): return 'Named makers of malas and prayer beads at Namaste Bead Shop.'
BRANDS_H1 = 'Makers'
def BRANDS_LEAD(S, n): return f'{n} named makers. Many malas are made by independent stringers and sit under <a href="/shop/">the shop</a>.'
PAIR = {'mala': ['meditation'], 'beaded': ['mala'], 'meditation': ['mala'], 'necklace': ['beaded'], 'bracelet': ['mala']}
REL_BRAND = 'More from {brand}'
REL_SCENT = 'More {scent} beads'
REL_PAIR = 'For your practice'
REL_MORE = 'More {aisle}'
def describe(S, x):
    t = x['title']; a = x['aisle']; s = []
    if a == 'tools':
        s.append(f"{E(t)} is a sound tool for meditation and ritual.")
        s.append('Strike or circle gently; each piece of handmade metal has its own tone, and sizes are given in the title.')
    else:
        n = re.search(r'\b(108|54|27|21|18)\b', t)
        s.append(f"{E(t)}" + (f" has {n.group(1)} beads" if n else ' is a strand of prayer beads') + (f" of about {x['mm']:g} mm" if x['mm'] else '') + '.')
        if a == 'm108': s.append('A full mala is used to count 108 repetitions of a mantra, affirmation or breath; the guru bead marks the start and end of a round.')
        else: s.append('Wrist malas and prayer bracelets keep a shorter count and are easy to wear between sessions.')
        if x['stones'] and x['stones'][0] not in S.NON_STONE and tradition(S, x['stones'][0]): s.append(f"Tradition pairs {E(S.STONE_NAME[x['stones'][0]].lower())} with {plist(tradition(S, x['stones'][0]))}, offered here as lore.")
    s.append('Natural materials vary from photo to piece. Collect it at 2 West 14th Street by Union Square or ship from NYC; checkout runs on Shopify through namastebookshop.com.')
    return s
def PRODUCT_DESC(S, x, v0): return f"{x['title']}, {S.money(v0['price'])}. Malas and prayer beads at 2 West 14th Street, NYC" + (', ready for pickup in about 2 hours.' if x['pickup'] else '.')
def ABOUT_DESC(S): return 'About Namaste Bead Shop, the mala and meditation shop at 2 West 14th Street by Union Square. A brand of Wealth Edge Ventures Inc.'
ABOUT_H1 = 'About Namaste Bead Shop'
def ABOUT(S):
    return f'''<p class="lead">Namaste Bead Shop is our corner for practice at {S.STORE_ADDR}: full malas, wrist malas, prayer bracelets and the bowls and bells that go with them.</p>
<p>We keep it focused so it is easier to choose: 108-bead malas in one aisle, wrist malas in another, seed and wood in their own, and sound tools last.{" Reserve online and choose Pickup at checkout." if S.PICKUP_ON else ""}</p>
<h2>Visit</h2><p>{S.STORE_ADDR}. Call <a href="tel:{S.TEL}">{S.PHONE}</a>.</p>{S.hours_html()}{S.visit_buttons()}
<h2>Who we are</h2><p>{S.LEGAL} Orders are processed on Shopify through <a href="{S.SHOP}" rel="noopener">namastebookshop.com</a>.</p>
<h2>A note on tradition</h2><p>Our guides describe how malas are commonly used in Hindu, Buddhist and yoga practice, and the meanings traditions give to stones. We share them respectfully and for interest; they are not medical advice.</p>'''
VISIT_TITLE = 'Visit Our Mala Shop near Union Square'
def VISIT_DESC(S): return f'Hours, directions and pickup for Namaste Bead Shop at {S.STORE_ADDR}.'
def VISIT_LEAD(S): return f'Come hold a few malas at {S.STORE_ADDR}, a few minutes west of Union Square.'
def FAQ_DESC(S): return 'Mala questions: how to use a mala, why 108 beads, wrist vs full malas, care, pickup and shipping.'
FAQ_H1 = 'Mala questions'
def FAQ(S):
    return [('What is a mala?', 'A strand of beads used to keep count during mantra or breath meditation, found in Hindu, Buddhist and yoga traditions.'),
            ('Why 108 beads?', 'Traditions give 108 many meanings; see <a href="/guide/why-108-beads/">why 108 beads</a>. Wrist malas use 27 or 54, fractions of 108.'),
            ('How do I use one?', 'Move one bead per repetition with your thumb, starting beside the guru bead. Full steps in <a href="/guide/how-to-use-a-mala/">how to use a mala</a>.'),
            ('Stone or rudraksha?', 'Rudraksha and wood are light and traditional; stone is heavier and cool to the touch. See <a href="/guide/choosing-a-mala/">choosing a mala</a>.'),
            ('Can I wear a mala as a necklace?', 'Many people do. Some traditions keep a practice mala private; it is your choice.'),
            ('Can I reserve and pick up?', 'Yes.' + (f' Orders are {S.READY.lower()}.' if S.READY else '') + f' We are at {S.STORE_ADDR}.')]
def GUIDES(S):
    return [
     {'path': '/guide/how-to-use-a-mala/', 'title': 'How to Use a Mala: A Simple Step-by-Step Guide', 'desc': 'How to hold a mala, count 108 repetitions and use the guru bead, with tips for beginners.', 'h1': 'How to use a mala',
      'html': '''<p class="lead">A mala keeps count so your mind can rest on the practice.</p><ol><li>Sit comfortably and choose a mantra, affirmation or simply your breath.</li><li>Hold the mala in your right hand, draped over the middle or ring finger. Many traditions avoid using the index finger.</li><li>Start at the bead next to the guru bead. With your thumb, draw one bead toward you for each repetition.</li><li>Continue around the strand for 108 repetitions.</li><li>When you reach the guru bead, pause. To continue, turn the mala and go back the other way rather than crossing it.</li></ol><h2>Short on time?</h2><p>Use a 27-bead wrist mala and go around four times for 108.</p><p><a class="btn" href="/shop/108-bead-malas/">Shop 108-bead malas</a></p>'''},
     {'path': '/guide/why-108-beads/', 'title': 'Why Do Malas Have 108 Beads?', 'desc': 'The traditional meanings of 108 in Hindu, Buddhist and yoga practice, and why wrist malas have 27 or 54 beads.', 'h1': 'Why 108 beads?',
      'html': '''<p class="lead">108 is a sacred number in several traditions, and the explanations vary.</p><ul><li>In Hindu traditions it appears in counts of names of deities and in Vedic cosmology.</li><li>In some Buddhist schools it is linked with 108 earthly desires or afflictions.</li><li>In yoga, 108 sun salutations are sometimes practiced at seasonal changes.</li></ul><p>Whatever the reason, 108 is long enough to settle into a practice. Wrist malas use 27 or 54 beads so that four or two rounds make 108.</p>'''},
     {'path': '/guide/choosing-a-mala/', 'title': 'Choosing a Mala: Stone, Rudraksha, Sandalwood or Wood', 'desc': 'How mala materials feel and wear, and how to choose bead size and length.', 'h1': 'Choosing a mala',
      'html': '''<p class="lead">Pick by how it will feel in your hand for 108 counts.</p><ul><li><b>Rudraksha:</b> textured seeds, light and traditional.</li><li><b>Sandalwood and wood:</b> light, smooth and warm.</li><li><b>Stone:</b> heavier and cool; choose a stone whose tradition or color you like.</li><li><b>Bead size:</b> 8 mm is standard; 6 mm is light and compact; 10 mm feels substantial.</li></ul>'''},
     {'path': '/guide/mala-care/', 'title': 'How to Care for a Mala', 'desc': 'Keep knotted cords and natural beads in good shape.', 'h1': 'Mala care',
      'html': '''<p class="lead">Malas are strung on cord, often knotted between beads.</p><ul><li>Keep it dry; water weakens cord and can mark wood and seed.</li><li>Store it coiled loosely in a pouch.</li><li>Comb a tassel gently with your fingers if it tangles.</li><li>Have a well-used mala restrung when the cord frays.</li></ul>'''},
     {'path': '/meditation-shop-manhattan/', 'title': 'Mala & Meditation Shop in Manhattan near Union Square', 'store_ld': True, 'desc': f'Malas, prayer beads and singing bowls in Manhattan at {S.STORE_ADDR}, by Union Square.', 'h1': 'Malas and meditation in Manhattan',
      'html': f'<p class="lead">{S.N:,} malas, prayer bracelets and sound tools on 14th Street just west of Fifth Avenue.</p>{hood_list(S, "/near/")}{S.visit_block()}'},
    ]
HOOD_LINE = {'union-square': 'After a class near Union Square, the mala shelf is a short walk west.', 'east-village': 'From East Village studios, head west on 14th Street.', 'chelsea': 'From Chelsea, walk east along 14th.',
             'flatiron': 'From Flatiron yoga studios, walk down Fifth.', 'greenwich-village': 'From the Village, up Fifth Avenue.', 'midtown': 'From Midtown, a quick ride to 14th Street.'}
def HOODS(S):
    picks = S.by_rank([x for x in S.leaders if x['aisle'] in ('m108', 'wrist')])[:8]
    return [{'path': f'/near/{k}/', 'title': f'Malas & Prayer Beads near {n} | Namaste Bead Shop', 'h1': f'Malas near {n}', 'desc': f'108-bead malas, wrist malas and singing bowls near {n}, NYC, at {S.STORE_ADDR}.',
             'html': f'<p class="lead">{E(HOOD_LINE[k])}</p><h2>Route from {E(n)}</h2><p>{E(route)}</p><h2>Malas in stock</h2>{S.grid(picks)}{S.visit_block()}<h2>Other neighborhoods</h2>{hood_list(S, "/near/", k)}'}
            for k, n, route in HOOD_DATA]
NOT_FOUND = 'That mala is no longer on the shelf'
