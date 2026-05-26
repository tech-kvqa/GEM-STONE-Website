"""
Run: python seed.py
Seeds the database with categories, products, and a demo admin user.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.user import User, Category, Product, ProductImage
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ── Admin user ────────────────────────────────────────────────────────────────
if not db.query(User).filter(User.email == "admin@crystalluxe.com").first():
    admin = User(
        full_name="Crystal Luxe Admin",
        email="admin@crystalluxe.com",
        hashed_password=get_password_hash("Admin@123"),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    print("✓ Admin user created: admin@crystalluxe.com / Admin@123")

# ── Categories ────────────────────────────────────────────────────────────────
categories_data = [
    {
        "name": "Quartz Crystals",
        "slug": "quartz",
        "description": "The master healers — pure, powerful, and endlessly versatile.",
        "story": "Born deep within the earth's crust over millions of years, Quartz is the most abundant crystal on our planet, yet its power is anything but ordinary. Revered by ancient civilisations from the Egyptians to the Japanese — who called it *suisho*, meaning 'perfect jewel' — Quartz is the ultimate amplifier of intention. At Crystal Luxe, our Quartz collection is hand-sourced from the ancient riverbeds of the Himalayas and the mines of Madagascar, each piece carrying the memory of the earth itself. Hold one in your palm and feel the ancient world speak.",
        # "image_url": "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=800",
        "image_url": "/static/images/categories/Quartz.png",
        # "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1600",
        "banner_url": "/static/images/banners/Quartz.png",
        "sort_order": 1
    },
    {
        "name": "Amethyst",
        "slug": "amethyst",
        "description": "The stone of spiritual wisdom and inner calm.",
        "story": "The Greeks believed Amethyst could prevent intoxication — its very name derives from *amethystos*, 'not drunk'. But its true intoxication is of a higher kind: the quiet, violet-hued serenity that settles over you when you hold a genuine Amethyst. Our collection is sourced from the deep violet mines of Uruguay and the pale lilac deposits of Zambia — each stone a universe of colour, from the palest lavender to the deepest royal purple. This is the stone of writers, meditators, and dreamers — those who seek clarity in the space between thoughts.",
        # "image_url": "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=800",
        # "banner_url": "https://images.unsplash.com/photo-1615486511484-92e172cc4d0f?w=1600",
        "image_url": "/static/images/categories/Amethyst_1.jpeg",
        "banner_url": "/static/images/banners/Amethyst.png",
        "sort_order": 2
    },
    {
        "name": "Rose Quartz",
        "slug": "rose-quartz",
        "description": "The eternal stone of love, compassion, and tender grace.",
        "story": "Long before Valentine's Day existed, Rose Quartz was already humanity's love letter to itself. Ancient Romans carved it into seals. Egyptians fashioned it into amulets to prevent ageing. Today, we know it simply as the stone of the heart — a gentle, rose-pink crystal that holds space for self-love, romantic love, and the love that dissolves grief. Each piece in our Rose Quartz collection is chosen for its depth of colour and the softness of its energy — rough clusters still dusty from Madagascan soil, polished spheres that catch light like a winter sunrise.",
        # "image_url": "https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=800",
        "image_url": "/static/images/categories/Rose_Quartz.png",
        # "banner_url": "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=1600",
        "banner_url": "/static/images/banners/Rose_Quartz.png",
        "sort_order": 3
    },
    {
        "name": "Black Tourmaline",
        "slug": "black-tourmaline",
        "description": "The ultimate protector — a shield of dark, grounded energy.",
        "story": "In a world of noise, Black Tourmaline is silence. It is the crystal that shamans carried into battle, that miners tucked into their pockets before descending into the earth, that energy workers place at the four corners of a room to seal it from negativity. Scientifically, Black Tourmaline is pyroelectric — it generates an electric charge when heated — and this quality hints at its true nature: it is a crystal that actively *works*, continuously transmuting negative energy into neutral, protective light. Our pieces are sourced from the ancient mines of Brazil, where the largest and most powerful deposits on earth still yield their dark treasure.",
        # "image_url": "https://images.unsplash.com/photo-1573408301185-9519f94ae39c?w=800",
        # "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1600",
        "image_url": "/static/images/categories/Black_Tourmaline.png",
        "banner_url": "/static/images/banners/Black_Tourmaline.png",
        "sort_order": 4
    },
    {
        "name": "Citrine",
        "slug": "citrine",
        "description": "The merchant's stone — abundance, optimism, and solar radiance.",
        "story": "Called the 'Merchant's Stone' and the 'Sun Stone', Citrine carries the warmth of the sun within its golden depths. Unlike most crystals, it does not hold negative energy — it transmutes, dissipates, and grounds it. Medieval merchants kept Citrine in their coin purses, and it remains today the crystal most associated with prosperity, success, and the quiet confidence of someone who knows their worth. Our Citrine collection spans the full solar spectrum — from pale champagne to deep amber, from natural Congolese rough to the finest faceted points — each one a bottled sunrise.",
        # "image_url": "https://images.unsplash.com/photo-1597149693980-d91f62c8f8c4?w=800",
        # "banner_url": "https://images.unsplash.com/photo-1597149693980-d91f62c8f8c4?w=1600",
        "image_url": "/static/images/categories/Citrine.png",
        "banner_url": "/static/images/banners/Citrine.png",
        "sort_order": 5
    },
    {
        "name": "Labradorite",
        "slug": "labradorite",
        "description": "The stone of magic, transformation, and hidden light.",
        "story": "Inuit legend says the Northern Lights were once trapped inside rocks along the Labrador coast — until a warrior struck the rocks with his spear and freed them into the sky. Some lights remained, and those became Labradorite. It is easy to believe this story when you hold a piece: grey and unassuming from most angles, then suddenly — flash — a wing of peacock blue, a wash of copper gold, a blaze of violet green. This phenomenon, called *labradorescence*, makes each piece a living, moving artwork. It is the crystal of transformation, of magic made visible, of the extraordinary hidden within the ordinary.",
        # "image_url": "https://images.unsplash.com/photo-1535412833400-40b4f58cbf04?w=800",
        # "banner_url": "https://images.unsplash.com/photo-1535412833400-40b4f58cbf04?w=1600",
        "image_url": "/static/images/categories/Labradorite.jpeg",
        "banner_url": "/static/images/banners/Labradorite.png",
        "sort_order": 6
    },
    {
        "name": "Selenite",
        "slug": "selenite",
        "description": "Liquid moonlight in solid form — the purest cleansing crystal.",
        "story": "Named after Selene, the Greek goddess of the moon, Selenite is perhaps the most ethereal crystal in existence — translucent as frosted glass, soft as chalk, glowing from within as though it has captured moonlight and held it fast. It is one of only a handful of crystals that never needs cleansing, because it *is* cleansing — place other crystals upon a Selenite plate and watch them reset overnight, their energy restored as if by morning rain. Our Selenite collection is sourced from the great caves of Morocco, where deposits formed over millions of years in ancient seabeds, each piece carrying the slow patience of deep geological time.",
        # "image_url": "https://images.unsplash.com/photo-1551361415-69c87624334f?w=800",
        # "banner_url": "https://images.unsplash.com/photo-1551361415-69c87624334f?w=1600",
        "image_url": "/static/images/categories/Selenite.png",
        "banner_url": "/static/images/banners/Selenite.png",
        "sort_order": 7
    },
    {
        "name": "Lapis Lazuli",
        "slug": "lapis-lazuli",
        "description": "The royal stone of truth, wisdom, and celestial vision.",
        "story": "For over 6,000 years, Lapis Lazuli has been the stone of kings and philosophers. Ground into powder, it became *ultramarine* — the most precious and expensive pigment in the world, used to paint the robes of the Virgin Mary and the ceiling of the Sistine Chapel. Worn by Cleopatra as eyeshadow. Buried with Tutankhamun. Placed upon the breastplates of Hebrew high priests. Its deep midnight blue, spangled with gold pyrite like a star map of the ancient sky, has fascinated humanity across every civilisation and era. This is the stone of the seekers — those who pursue truth above all else.",
        # "image_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800",
        # "banner_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1600",
        "image_url": "/static/images/categories/Lapis_lazuli.png",
        "banner_url": "/static/images/banners/Lapis_lazuli.png",
        "sort_order": 8
    },
    {
        "name": "Jewellery Designs",
        "slug": "jewellery",
        "description": "Luxury wearable crystal energy.",
        "story": "Elegant handcrafted crystal jewellery infused with healing stones.",
        "image_url": "/static/images/categories/jewellery.png",
        "banner_url": "/static/images/banners/jewellery.png",
        "sort_order": 9
    },
    {
        "name": "Crystal Designs",
        "slug": "crystal-designs",
        "description": "Premium sacred crystal decor.",
        "story": "Artistic crystal structures designed for healing spaces.",
        "image_url": "/static/images/categories/crystal_designs.png",
        "banner_url": "/static/images/banners/crystal_designs.png",
        "sort_order": 10
    },
    # {
    #     "name": "Lab Diamonds",
    #     "slug": "lab-diamonds",
    #     "description": "Ethical brilliance and timeless luxury.",
    #     "story": "Modern precision-crafted diamonds with conscious origins.",
    #     "image_url": "/static/images/categories/lab_diamonds.png",
    #     "banner_url": "/static/images/banners/lab_diamonds.png",
    #     "sort_order": 11
    # },
]

cat_map = {}
for cd in categories_data:
    existing = db.query(Category).filter(Category.slug == cd["slug"]).first()
    if not existing:
        cat = Category(**cd)
        db.add(cat)
        db.flush()
        cat_map[cd["slug"]] = cat.id
        print(f"  ✓ Category: {cd['name']}")
    else:
        cat_map[cd["slug"]] = existing.id
db.commit()

# ── Products ──────────────────────────────────────────────────────────────────
products_data = [
    # QUARTZ
    {
        "name": "Himalayan Clear Quartz Point",
        "slug": "himalayan-clear-quartz-point",
        "sku": "CL-QTZ-001",
        "category_slug": "quartz",
        "description": "A pristine, naturally terminated Clear Quartz point sourced from the high-altitude mines of Himachal Pradesh. Each piece is unique, with natural inclusions and internal rainbows.",
        "story": "This crystal emerged from the same mountains that inspired mankind's oldest spiritual traditions. Its clarity is not emptiness — it is infinite potential, awaiting your intention.",
        "healing_props": "Amplifies energy and intention. Enhances clarity of thought. Aids meditation and spiritual growth. Boosts the immune system. Master healer.",
        "chakra": "Crown, All Chakras",
        "zodiac": "All Signs",
        "origin": "Himachal Pradesh, India",
        "weight_grams": 85.0,
        "dimensions": "8-10 cm height",
        "price": 1850.00,
        "compare_price": 2400.00,
        "stock_qty": 24,
        "is_featured": True,
        "is_bestseller": True,
        "images": [
            # "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=600",
            # "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600",
            # "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=600"
            "/static/images/products/Quartz/Quartz_1.png",
            # "/static/images/products/Quartz/Quartz_2.png",
        ]
    },
    {
        "name": "Smoky Quartz Tower",
        "slug": "smoky-quartz-tower",
        "sku": "CL-QTZ-002",
        "category_slug": "quartz",
        "description": "A deeply grounding Smoky Quartz tower with rich, translucent brown-grey colouring. Hand-polished to a high shine, it stands as a powerful centrepiece.",
        "story": "Smoky Quartz is Quartz that has spent eons near natural radiation sources — the earth itself has transformed it into something deeper, darker, and more grounding than its clear cousin.",
        "healing_props": "Grounding and protection. Transmutes negative energy. Relieves stress, fear, and anxiety. Enhances concentration. Excellent for EMF protection.",
        "chakra": "Root, Solar Plexus",
        "zodiac": "Scorpio, Sagittarius, Capricorn",
        "origin": "Brazil",
        "weight_grams": 320.0,
        "dimensions": "12-14 cm height",
        "price": 3200.00,
        "compare_price": 4000.00,
        "stock_qty": 12,
        "is_new_arrival": True,
        "images": [
            # "https://images.unsplash.com/photo-1516796181074-bf453fbfa3e6?w=600",
            # "https://images.unsplash.com/photo-1573408301185-9519f94ae39c?w=600",
            # "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600"
            "/static/images/products/Quartz/Quartz_2.png",
        ]
    },
    {
        "name": "Rose Quartz Sphere",
        "slug": "rose-quartz-sphere",
        "sku": "CL-RQ-001",
        "category_slug": "rose-quartz",
        "description": "A perfectly polished Rose Quartz sphere of exceptional colour depth. The sphere shape allows energy to radiate in all directions, filling your space with gentle, loving vibration.",
        "story": "The Sphere is the perfect form — no beginning, no end, infinite in all directions. A Rose Quartz sphere does not merely sit in a room; it gently, ceaselessly, loves it.",
        "healing_props": "Unconditional love. Emotional healing. Self-acceptance. Attracts romantic love. Heals the heart chakra. Reduces anxiety and emotional tension.",
        "chakra": "Heart",
        "zodiac": "Taurus, Libra",
        "origin": "Madagascar",
        "weight_grams": 280.0,
        "dimensions": "6 cm diameter",
        "price": 2650.00,
        "compare_price": 3200.00,
        "stock_qty": 18,
        "is_featured": True,
        "is_bestseller": True,
        "images": [
            # "https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=600",
            # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600",
            # "https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=600"
            "/static/images/products/Rose_Quartz/Rose_quartz_1.jpeg",
            "/static/images/products/Rose_Quartz/Rose_quartz_2.jpeg",
        ]
    },
    {
        "name": "Raw Rose Quartz Cluster",
        "slug": "raw-rose-quartz-cluster",
        "sku": "CL-RQ-002",
        "category_slug": "rose-quartz",
        "description": "A raw, unpolished Rose Quartz cluster with natural matrix. The rough surface catches light differently at each angle, revealing pale pink depths and natural crystal formations.",
        "story": "In its raw form, Rose Quartz speaks most honestly — unpolished, imperfect, and utterly beautiful. A reminder that love does not require perfection.",
        "healing_props": "Gentle, diffused loving energy. Excellent for bedroom spaces. Supports emotional healing during grief. Encourages self-love rituals.",
        "chakra": "Heart",
        "zodiac": "Taurus, Libra, Scorpio",
        "origin": "Madagascar",
        "weight_grams": 450.0,
        "dimensions": "10-12 cm",
        "price": 1950.00,
        "compare_price": None,
        "stock_qty": 9,
        "is_new_arrival": True,
        "images": [
            # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600",
            # "https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=600",
            # "https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=600"
            "/static/images/products/Rose_Quartz/Rose_quartz_2.jpeg",
        ]
    },
    {
        "name": "Deep Uruguayan Amethyst Cluster",
        "slug": "deep-uruguayan-amethyst-cluster",
        "sku": "CL-AMT-001",
        "category_slug": "amethyst",
        "description": "A museum-quality Amethyst cluster from the deep purple mines of Uruguay. The crystals are densely packed, deeply saturated in colour, and display exceptional clarity.",
        "story": "Uruguayan Amethyst is the rarest and most coveted — its purple so deep it borders on black in low light, revealing its true violet only when sunlight passes through. This is not decoration. This is art.",
        "healing_props": "Calms the mind and aids sleep. Enhances intuition and psychic abilities. Protects against psychic attack. Ideal for meditation spaces.",
        "chakra": "Third Eye, Crown",
        "zodiac": "Virgo, Sagittarius, Capricorn, Aquarius, Pisces",
        "origin": "Uruguay",
        "weight_grams": 680.0,
        "dimensions": "15-18 cm",
        "price": 5800.00,
        "compare_price": 7200.00,
        "stock_qty": 6,
        "is_featured": True,
        "images": [
            # "https://images.unsplash.com/photo-1615486511484-92e172cc4d0f?w=600",
            # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600",
            # "https://images.unsplash.com/photo-1516796181074-bf453fbfa3e6?w=600"
            "/static/images/products/Amethyst/Amethyst_1.png",
        ]
    },
    {
        "name": "Amethyst Palm Stone",
        "slug": "amethyst-palm-stone",
        "sku": "CL-AMT-002",
        "category_slug": "amethyst",
        "description": "A smoothly polished Amethyst palm stone, shaped to rest perfectly in the hand during meditation. Medium purple with natural banding and internal clarity.",
        "story": "Designed to be held. The palm stone has been used in healing traditions for centuries — its weight in your hand, its smooth coolness, are themselves a form of meditation.",
        "healing_props": "Stress relief. Meditation aid. Sleep support. Emotional balance. Ideal for anxiety and overthinking.",
        "chakra": "Third Eye, Crown",
        "zodiac": "Aquarius, Pisces",
        "origin": "Zambia",
        "weight_grams": 95.0,
        "dimensions": "6 x 4 cm",
        "price": 780.00,
        "compare_price": 950.00,
        "stock_qty": 35,
        "is_bestseller": True,
        "images": [
            # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600",
            # "https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=600",
            # "https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=600"
            "/static/images/products/Amethyst/Amethyst_2.png"
        ]
    },
    {
        "name": "Black Tourmaline Standing Piece",
        "slug": "black-tourmaline-standing",
        "sku": "CL-BT-001",
        "category_slug": "black-tourmaline",
        "description": "A naturally striated Black Tourmaline standing piece with a flat base. The parallel vertical lines are the crystal's signature — channels through which energy flows and transmutes.",
        "story": "You place a Black Tourmaline at your door not because you fear what comes in, but because you value what you have built inside. It is the guardian stone.",
        "healing_props": "Psychic protection. EMF shielding. Grounding. Removes negative energy from environments. Reduces anxiety and fear. Excellent near electronics.",
        "chakra": "Root",
        "zodiac": "Capricorn, Scorpio",
        "origin": "Brazil",
        "weight_grams": 240.0,
        "dimensions": "10-12 cm height",
        "price": 2100.00,
        "compare_price": 2800.00,
        "stock_qty": 15,
        "is_featured": True,
        "is_bestseller": True,
        "images": [
            # "https://images.unsplash.com/photo-1573408301185-9519f94ae39c?w=600",
            # "https://images.unsplash.com/photo-1516796181074-bf453fbfa3e6?w=600",
            # "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=600"
            "/static/images/products/Black_Tourmaline/Black_Tourmaline_1.png"

        ]
    },
    {
        "name": "Natural Citrine Point",
        "slug": "natural-citrine-point",
        "sku": "CL-CIT-001",
        "category_slug": "citrine",
        "description": "A natural (not heat-treated) Citrine point from the Congo. Pale yellow to honey-gold, these are rarer and more powerful than the heat-treated variety. Each piece is a genuine sun-coloured miracle.",
        "story": "True natural Citrine is rare. Most 'Citrine' on the market is Amethyst baked until golden. Ours is the real thing — formed naturally, carrying genuine solar energy.",
        "healing_props": "Abundance and manifestation. Creativity and motivation. Dispels negativity. Boosts self-confidence. Activates the solar plexus. The stone of joy.",
        "chakra": "Solar Plexus, Sacral",
        "zodiac": "Aries, Gemini, Leo, Libra",
        "origin": "Democratic Republic of Congo",
        "weight_grams": 75.0,
        "dimensions": "7-9 cm height",
        "price": 2400.00,
        "compare_price": 3000.00,
        "stock_qty": 20,
        "is_featured": True,
        "is_new_arrival": True,
        "images": [
            # "https://images.unsplash.com/photo-1597149693980-d91f62c8f8c4?w=600",
            # "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=600",
            # "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=600"
            "/static/images/products/Citrine/Citrine_1.png"
        ]
    },
    {
        "name": "Labradorite Freeform",
        "slug": "labradorite-freeform",
        "sku": "CL-LAB-001",
        "category_slug": "labradorite",
        "description": "A stunning Labradorite freeform with exceptional labradorescence — flashing blue, gold, and green across its surface as it catches the light. Each piece is a unique work of natural art.",
        "story": "Every angle tells a different story. This is the nature of Labradorite, and the nature of magic — it reveals itself only to those willing to look from new perspectives.",
        "healing_props": "Awakens psychic abilities. Strengthens intuition. Transformation and change. Protects the aura. Stimulates imagination. Excellent for shadow work.",
        "chakra": "Throat, Third Eye, Crown",
        "zodiac": "Leo, Scorpio, Sagittarius",
        "origin": "Madagascar",
        "weight_grams": 310.0,
        "dimensions": "8-10 cm",
        "price": 3500.00,
        "compare_price": 4200.00,
        "stock_qty": 11,
        "is_featured": True,
        "is_bestseller": True,
        "images": [
            # "https://images.unsplash.com/photo-1535412833400-40b4f58cbf04?w=600",
            # "https://images.unsplash.com/photo-1516796181074-bf453fbfa3e6?w=600",
            # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600"
            "/static/images/products/Labradorite/Labradorite_sphere_1.png",
            "/static/images/products/Labradorite/Labradorite_sphere_2.png"
        ]
    },
    {
        "name": "Selenite Charging Plate",
        "slug": "selenite-charging-plate",
        "sku": "CL-SEL-001",
        "category_slug": "selenite",
        "description": "A beautifully smooth, oval Selenite charging plate for cleansing and recharging your crystal collection overnight. Translucent white with natural striations.",
        "story": "Leave your crystals here overnight and return to find them reset, cleansed, and ready — as if the moon itself passed over them while you slept.",
        "healing_props": "Cleanses other crystals. Purifies environments. Connects to higher consciousness. Aids mental clarity. Promotes peaceful sleep. Never needs cleansing.",
        "chakra": "Crown, Third Eye",
        "zodiac": "Taurus, Cancer",
        "origin": "Morocco",
        "weight_grams": 450.0,
        "dimensions": "20 x 10 cm",
        "price": 1650.00,
        "compare_price": 2000.00,
        "stock_qty": 22,
        "is_bestseller": True,
        "images": [
            # "https://images.unsplash.com/photo-1551361415-69c87624334f?w=600",
            # "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=600",
            # "https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=600"
            "/static/images/products/Selenite/Selenite_1.png"
        ]
    },
    {
        "name": "Lapis Lazuli Sphere",
        "slug": "lapis-lazuli-sphere",
        "sku": "CL-LAP-001",
        "category_slug": "lapis-lazuli",
        "description": "A richly coloured Lapis Lazuli sphere with deep blue colouring and visible gold pyrite inclusions — the night sky made stone. Polished to a high mirror shine.",
        "story": "This is the stone that painted the Sistine Chapel. The stone Cleopatra wore as eyeshadow. When you hold this sphere, you hold 6,000 years of human wisdom.",
        "healing_props": "Truth and self-expression. Enhances wisdom and intellectual ability. Activates the higher mind. Aids communication. Reveals inner truth.",
        "chakra": "Third Eye, Throat",
        "zodiac": "Sagittarius, Aquarius",
        "origin": "Afghanistan",
        "weight_grams": 390.0,
        "dimensions": "7 cm diameter",
        "price": 4800.00,
        "compare_price": 6000.00,
        "stock_qty": 7,
        "is_featured": True,
        "images": [
            # "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600",
            # "https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=600",
            # "https://images.unsplash.com/photo-1573408301185-9519f94ae39c?w=600"
            "/static/images/products/Lapis_lazuli/Lapis_lazuli_1.png"
        ]
    },
    {
        "name": "Crystal Starter Set",
        "slug": "crystal-starter-set",
        "sku": "CL-SET-001",
        "category_slug": "quartz",
        "description": "The perfect introduction to the world of crystals — seven carefully chosen stones representing seven intentions: love, protection, clarity, abundance, peace, truth, and grounding.",
        "story": "Every journey begins with a single stone. This set is the beginning of yours — curated by our crystal experts to cover every dimension of wellbeing.",
        "healing_props": "Comprehensive energy support. Includes: Clear Quartz, Rose Quartz, Amethyst, Black Tourmaline, Citrine, Selenite, and Labradorite. Complete chakra coverage.",
        "chakra": "All Chakras",
        "zodiac": "All Signs",
        "origin": "Multiple Origins",
        "weight_grams": 350.0,
        "dimensions": "Wooden Gift Box",
        "price": 4999.00,
        "compare_price": 6500.00,
        "stock_qty": 30,
        "is_featured": True,
        "is_bestseller": True,
        "is_new_arrival": True,
        "images": [
            "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=600",
            "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600"
        ]
    },
    {
        "name": "Jewellery Designs",
        "slug": "jewellery",
        "sku": "CL-JEL-001",
        "category_slug": "jewellery",
        "description": "Luxury wearable crystal energy.",
        "story": "Elegant handcrafted crystal jewellery infused with healing stones.",
        "healing_props": "Comprehensive energy support. Includes: Clear Quartz, Rose Quartz, Amethyst, Black Tourmaline, Citrine, Selenite, and Labradorite. Complete chakra coverage.",
        "chakra": "All Chakras",
        "zodiac": "All Signs",
        "origin": "Multiple Origins",
        "weight_grams": 350.0,
        "dimensions": "Wooden Gift Box",
        "price": 4999.00,
        "compare_price": 6500.00,
        "stock_qty": 30,
        "is_featured": True,
        "is_bestseller": True,
        "is_new_arrival": True,
        "images": [
            # "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=600",
            # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600"
            "/static/images/products/jewllery/bracelets.png"
        ]
    }
]

for pd in products_data:
    existing = db.query(Product).filter(Product.slug == pd["slug"]).first()
    if not existing:
        images = pd.pop("images", [])
        cat_slug = pd.pop("category_slug")
        cat_id = cat_map.get(cat_slug)
        if not cat_id:
            continue
        product = Product(category_id=cat_id, **pd)
        db.add(product)
        db.flush()
        for i, url in enumerate(images):
            img = ProductImage(
                product_id=product.id,
                url=url,
                is_primary=(i == 0),
                sort_order=i
            )
            db.add(img)
        print(f"  ✓ Product: {product.name}")

db.commit()
db.close()
print("\n✅ Database seeded successfully!")
