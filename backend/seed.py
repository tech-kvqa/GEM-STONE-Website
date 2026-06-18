# """
# Run: python seed.py
# Seeds the database with categories, products, and a demo admin user.
# """
# import sys, os
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# from app.core.database import SessionLocal, engine, Base
# from app.models.user import User, Category, Product, ProductImage
# from app.core.security import get_password_hash

# Base.metadata.create_all(bind=engine)
# db = SessionLocal()

# # ── Admin user ────────────────────────────────────────────────────────────────
# if not db.query(User).filter(User.email == "admin@crystalluxe.com").first():
#     admin = User(
#         full_name="Crystal Luxe Admin",
#         email="admin@crystalluxe.com",
#         hashed_password=get_password_hash("Admin@123"),
#         is_admin=True
#     )
#     db.add(admin)
#     db.commit()
#     print("✓ Admin user created: admin@crystalluxe.com / Admin@123")

# # ── Categories ────────────────────────────────────────────────────────────────
# categories_data = [
#     {
#         "name": "Quartz Crystals",
#         "slug": "quartz",
#         "description": "The master healers — pure, powerful, and endlessly versatile.",
#         "story": "Born deep within the earth's crust over millions of years, Quartz is the most abundant crystal on our planet, yet its power is anything but ordinary. Revered by ancient civilisations from the Egyptians to the Japanese — who called it *suisho*, meaning 'perfect jewel' — Quartz is the ultimate amplifier of intention. At Crystal Luxe, our Quartz collection is hand-sourced from the ancient riverbeds of the Himalayas and the mines of Madagascar, each piece carrying the memory of the earth itself. Hold one in your palm and feel the ancient world speak.",
#         # "image_url": "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=800",
#         "image_url": "/static/images/categories/Quartz.png",
#         # "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1600",
#         "banner_url": "/static/images/banners/Quartz.png",
#         "sort_order": 1
#     },
#     {
#         "name": "Amethyst",
#         "slug": "amethyst",
#         "description": "The stone of spiritual wisdom and inner calm.",
#         "story": "The Greeks believed Amethyst could prevent intoxication — its very name derives from *amethystos*, 'not drunk'. But its true intoxication is of a higher kind: the quiet, violet-hued serenity that settles over you when you hold a genuine Amethyst. Our collection is sourced from the deep violet mines of Uruguay and the pale lilac deposits of Zambia — each stone a universe of colour, from the palest lavender to the deepest royal purple. This is the stone of writers, meditators, and dreamers — those who seek clarity in the space between thoughts.",
#         # "image_url": "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=800",
#         # "banner_url": "https://images.unsplash.com/photo-1615486511484-92e172cc4d0f?w=1600",
#         "image_url": "/static/images/categories/Amethyst_1.jpeg",
#         "banner_url": "/static/images/banners/Amethyst.png",
#         "sort_order": 2
#     },
#     {
#         "name": "Rose Quartz",
#         "slug": "rose-quartz",
#         "description": "The eternal stone of love, compassion, and tender grace.",
#         "story": "Long before Valentine's Day existed, Rose Quartz was already humanity's love letter to itself. Ancient Romans carved it into seals. Egyptians fashioned it into amulets to prevent ageing. Today, we know it simply as the stone of the heart — a gentle, rose-pink crystal that holds space for self-love, romantic love, and the love that dissolves grief. Each piece in our Rose Quartz collection is chosen for its depth of colour and the softness of its energy — rough clusters still dusty from Madagascan soil, polished spheres that catch light like a winter sunrise.",
#         # "image_url": "https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=800",
#         "image_url": "/static/images/categories/Rose_Quartz.png",
#         # "banner_url": "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=1600",
#         "banner_url": "/static/images/banners/Rose_Quartz.png",
#         "sort_order": 3
#     },
#     {
#         "name": "Black Tourmaline",
#         "slug": "black-tourmaline",
#         "description": "The ultimate protector — a shield of dark, grounded energy.",
#         "story": "In a world of noise, Black Tourmaline is silence. It is the crystal that shamans carried into battle, that miners tucked into their pockets before descending into the earth, that energy workers place at the four corners of a room to seal it from negativity. Scientifically, Black Tourmaline is pyroelectric — it generates an electric charge when heated — and this quality hints at its true nature: it is a crystal that actively *works*, continuously transmuting negative energy into neutral, protective light. Our pieces are sourced from the ancient mines of Brazil, where the largest and most powerful deposits on earth still yield their dark treasure.",
#         # "image_url": "https://images.unsplash.com/photo-1573408301185-9519f94ae39c?w=800",
#         # "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1600",
#         "image_url": "/static/images/categories/Black_Tourmaline.png",
#         "banner_url": "/static/images/banners/Black_Tourmaline.png",
#         "sort_order": 4
#     },
#     {
#         "name": "Citrine",
#         "slug": "citrine",
#         "description": "The merchant's stone — abundance, optimism, and solar radiance.",
#         "story": "Called the 'Merchant's Stone' and the 'Sun Stone', Citrine carries the warmth of the sun within its golden depths. Unlike most crystals, it does not hold negative energy — it transmutes, dissipates, and grounds it. Medieval merchants kept Citrine in their coin purses, and it remains today the crystal most associated with prosperity, success, and the quiet confidence of someone who knows their worth. Our Citrine collection spans the full solar spectrum — from pale champagne to deep amber, from natural Congolese rough to the finest faceted points — each one a bottled sunrise.",
#         # "image_url": "https://images.unsplash.com/photo-1597149693980-d91f62c8f8c4?w=800",
#         # "banner_url": "https://images.unsplash.com/photo-1597149693980-d91f62c8f8c4?w=1600",
#         "image_url": "/static/images/categories/Citrine.png",
#         "banner_url": "/static/images/banners/Citrine.png",
#         "sort_order": 5
#     },
#     {
#         "name": "Labradorite",
#         "slug": "labradorite",
#         "description": "The stone of magic, transformation, and hidden light.",
#         "story": "Inuit legend says the Northern Lights were once trapped inside rocks along the Labrador coast — until a warrior struck the rocks with his spear and freed them into the sky. Some lights remained, and those became Labradorite. It is easy to believe this story when you hold a piece: grey and unassuming from most angles, then suddenly — flash — a wing of peacock blue, a wash of copper gold, a blaze of violet green. This phenomenon, called *labradorescence*, makes each piece a living, moving artwork. It is the crystal of transformation, of magic made visible, of the extraordinary hidden within the ordinary.",
#         # "image_url": "https://images.unsplash.com/photo-1535412833400-40b4f58cbf04?w=800",
#         # "banner_url": "https://images.unsplash.com/photo-1535412833400-40b4f58cbf04?w=1600",
#         "image_url": "/static/images/categories/Labradorite.jpeg",
#         "banner_url": "/static/images/banners/Labradorite.png",
#         "sort_order": 6
#     },
#     {
#         "name": "Selenite",
#         "slug": "selenite",
#         "description": "Liquid moonlight in solid form — the purest cleansing crystal.",
#         "story": "Named after Selene, the Greek goddess of the moon, Selenite is perhaps the most ethereal crystal in existence — translucent as frosted glass, soft as chalk, glowing from within as though it has captured moonlight and held it fast. It is one of only a handful of crystals that never needs cleansing, because it *is* cleansing — place other crystals upon a Selenite plate and watch them reset overnight, their energy restored as if by morning rain. Our Selenite collection is sourced from the great caves of Morocco, where deposits formed over millions of years in ancient seabeds, each piece carrying the slow patience of deep geological time.",
#         # "image_url": "https://images.unsplash.com/photo-1551361415-69c87624334f?w=800",
#         # "banner_url": "https://images.unsplash.com/photo-1551361415-69c87624334f?w=1600",
#         "image_url": "/static/images/categories/Selenite.png",
#         "banner_url": "/static/images/banners/Selenite.png",
#         "sort_order": 7
#     },
#     {
#         "name": "Lapis Lazuli",
#         "slug": "lapis-lazuli",
#         "description": "The royal stone of truth, wisdom, and celestial vision.",
#         "story": "For over 6,000 years, Lapis Lazuli has been the stone of kings and philosophers. Ground into powder, it became *ultramarine* — the most precious and expensive pigment in the world, used to paint the robes of the Virgin Mary and the ceiling of the Sistine Chapel. Worn by Cleopatra as eyeshadow. Buried with Tutankhamun. Placed upon the breastplates of Hebrew high priests. Its deep midnight blue, spangled with gold pyrite like a star map of the ancient sky, has fascinated humanity across every civilisation and era. This is the stone of the seekers — those who pursue truth above all else.",
#         # "image_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800",
#         # "banner_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1600",
#         "image_url": "/static/images/categories/Lapis_lazuli.png",
#         "banner_url": "/static/images/banners/Lapis_lazuli.png",
#         "sort_order": 8
#     },
#     {
#         "name": "Jewellery Designs",
#         "slug": "jewellery",
#         "description": "Luxury wearable crystal energy.",
#         "story": "Elegant handcrafted crystal jewellery infused with healing stones.",
#         "image_url": "/static/images/categories/jewellery.png",
#         "banner_url": "/static/images/banners/jewellery.png",
#         "sort_order": 9
#     },
#     {
#         "name": "Crystal Designs",
#         "slug": "crystal-designs",
#         "description": "Premium sacred crystal decor.",
#         "story": "Artistic crystal structures designed for healing spaces.",
#         "image_url": "/static/images/categories/crystal_designs.png",
#         "banner_url": "/static/images/banners/crystal_designs.png",
#         "sort_order": 10
#     },
#     # {
#     #     "name": "Lab Diamonds",
#     #     "slug": "lab-diamonds",
#     #     "description": "Ethical brilliance and timeless luxury.",
#     #     "story": "Modern precision-crafted diamonds with conscious origins.",
#     #     "image_url": "/static/images/categories/lab_diamonds.png",
#     #     "banner_url": "/static/images/banners/lab_diamonds.png",
#     #     "sort_order": 11
#     # },
# ]

# cat_map = {}
# for cd in categories_data:
#     existing = db.query(Category).filter(Category.slug == cd["slug"]).first()
#     if not existing:
#         cat = Category(**cd)
#         db.add(cat)
#         db.flush()
#         cat_map[cd["slug"]] = cat.id
#         print(f"  ✓ Category: {cd['name']}")
#     else:
#         cat_map[cd["slug"]] = existing.id
# db.commit()

# # ── Products ──────────────────────────────────────────────────────────────────
# products_data = [
#     # QUARTZ
#     {
#         "name": "Himalayan Clear Quartz Point",
#         "slug": "himalayan-clear-quartz-point",
#         "sku": "CL-QTZ-001",
#         "category_slug": "quartz",
#         "description": "A pristine, naturally terminated Clear Quartz point sourced from the high-altitude mines of Himachal Pradesh. Each piece is unique, with natural inclusions and internal rainbows.",
#         "story": "This crystal emerged from the same mountains that inspired mankind's oldest spiritual traditions. Its clarity is not emptiness — it is infinite potential, awaiting your intention.",
#         "healing_props": "Amplifies energy and intention. Enhances clarity of thought. Aids meditation and spiritual growth. Boosts the immune system. Master healer.",
#         "chakra": "Crown, All Chakras",
#         "zodiac": "All Signs",
#         "origin": "Himachal Pradesh, India",
#         "weight_grams": 85.0,
#         "dimensions": "8-10 cm height",
#         "price": 1850.00,
#         "compare_price": 2400.00,
#         "stock_qty": 24,
#         "is_featured": True,
#         "is_bestseller": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=600",
#             # "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600",
#             # "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=600"
#             "/static/images/products/Quartz/Quartz_1.png",
#             # "/static/images/products/Quartz/Quartz_2.png",
#         ]
#     },
#     {
#         "name": "Smoky Quartz Tower",
#         "slug": "smoky-quartz-tower",
#         "sku": "CL-QTZ-002",
#         "category_slug": "quartz",
#         "description": "A deeply grounding Smoky Quartz tower with rich, translucent brown-grey colouring. Hand-polished to a high shine, it stands as a powerful centrepiece.",
#         "story": "Smoky Quartz is Quartz that has spent eons near natural radiation sources — the earth itself has transformed it into something deeper, darker, and more grounding than its clear cousin.",
#         "healing_props": "Grounding and protection. Transmutes negative energy. Relieves stress, fear, and anxiety. Enhances concentration. Excellent for EMF protection.",
#         "chakra": "Root, Solar Plexus",
#         "zodiac": "Scorpio, Sagittarius, Capricorn",
#         "origin": "Brazil",
#         "weight_grams": 320.0,
#         "dimensions": "12-14 cm height",
#         "price": 3200.00,
#         "compare_price": 4000.00,
#         "stock_qty": 12,
#         "is_new_arrival": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1516796181074-bf453fbfa3e6?w=600",
#             # "https://images.unsplash.com/photo-1573408301185-9519f94ae39c?w=600",
#             # "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600"
#             "/static/images/products/Quartz/Quartz_2.png",
#         ]
#     },
#     {
#         "name": "Rose Quartz Sphere",
#         "slug": "rose-quartz-sphere",
#         "sku": "CL-RQ-001",
#         "category_slug": "rose-quartz",
#         "description": "A perfectly polished Rose Quartz sphere of exceptional colour depth. The sphere shape allows energy to radiate in all directions, filling your space with gentle, loving vibration.",
#         "story": "The Sphere is the perfect form — no beginning, no end, infinite in all directions. A Rose Quartz sphere does not merely sit in a room; it gently, ceaselessly, loves it.",
#         "healing_props": "Unconditional love. Emotional healing. Self-acceptance. Attracts romantic love. Heals the heart chakra. Reduces anxiety and emotional tension.",
#         "chakra": "Heart",
#         "zodiac": "Taurus, Libra",
#         "origin": "Madagascar",
#         "weight_grams": 280.0,
#         "dimensions": "6 cm diameter",
#         "price": 2650.00,
#         "compare_price": 3200.00,
#         "stock_qty": 18,
#         "is_featured": True,
#         "is_bestseller": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=600",
#             # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600",
#             # "https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=600"
#             "/static/images/products/Rose_Quartz/Rose_quartz_1.jpeg",
#             "/static/images/products/Rose_Quartz/Rose_quartz_2.jpeg",
#         ]
#     },
#     {
#         "name": "Raw Rose Quartz Cluster",
#         "slug": "raw-rose-quartz-cluster",
#         "sku": "CL-RQ-002",
#         "category_slug": "rose-quartz",
#         "description": "A raw, unpolished Rose Quartz cluster with natural matrix. The rough surface catches light differently at each angle, revealing pale pink depths and natural crystal formations.",
#         "story": "In its raw form, Rose Quartz speaks most honestly — unpolished, imperfect, and utterly beautiful. A reminder that love does not require perfection.",
#         "healing_props": "Gentle, diffused loving energy. Excellent for bedroom spaces. Supports emotional healing during grief. Encourages self-love rituals.",
#         "chakra": "Heart",
#         "zodiac": "Taurus, Libra, Scorpio",
#         "origin": "Madagascar",
#         "weight_grams": 450.0,
#         "dimensions": "10-12 cm",
#         "price": 1950.00,
#         "compare_price": None,
#         "stock_qty": 9,
#         "is_new_arrival": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600",
#             # "https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=600",
#             # "https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=600"
#             "/static/images/products/Rose_Quartz/Rose_quartz_2.jpeg",
#         ]
#     },
#     {
#         "name": "Deep Uruguayan Amethyst Cluster",
#         "slug": "deep-uruguayan-amethyst-cluster",
#         "sku": "CL-AMT-001",
#         "category_slug": "amethyst",
#         "description": "A museum-quality Amethyst cluster from the deep purple mines of Uruguay. The crystals are densely packed, deeply saturated in colour, and display exceptional clarity.",
#         "story": "Uruguayan Amethyst is the rarest and most coveted — its purple so deep it borders on black in low light, revealing its true violet only when sunlight passes through. This is not decoration. This is art.",
#         "healing_props": "Calms the mind and aids sleep. Enhances intuition and psychic abilities. Protects against psychic attack. Ideal for meditation spaces.",
#         "chakra": "Third Eye, Crown",
#         "zodiac": "Virgo, Sagittarius, Capricorn, Aquarius, Pisces",
#         "origin": "Uruguay",
#         "weight_grams": 680.0,
#         "dimensions": "15-18 cm",
#         "price": 5800.00,
#         "compare_price": 7200.00,
#         "stock_qty": 6,
#         "is_featured": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1615486511484-92e172cc4d0f?w=600",
#             # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600",
#             # "https://images.unsplash.com/photo-1516796181074-bf453fbfa3e6?w=600"
#             "/static/images/products/Amethyst/Amethyst_1.png",
#         ]
#     },
#     {
#         "name": "Amethyst Palm Stone",
#         "slug": "amethyst-palm-stone",
#         "sku": "CL-AMT-002",
#         "category_slug": "amethyst",
#         "description": "A smoothly polished Amethyst palm stone, shaped to rest perfectly in the hand during meditation. Medium purple with natural banding and internal clarity.",
#         "story": "Designed to be held. The palm stone has been used in healing traditions for centuries — its weight in your hand, its smooth coolness, are themselves a form of meditation.",
#         "healing_props": "Stress relief. Meditation aid. Sleep support. Emotional balance. Ideal for anxiety and overthinking.",
#         "chakra": "Third Eye, Crown",
#         "zodiac": "Aquarius, Pisces",
#         "origin": "Zambia",
#         "weight_grams": 95.0,
#         "dimensions": "6 x 4 cm",
#         "price": 780.00,
#         "compare_price": 950.00,
#         "stock_qty": 35,
#         "is_bestseller": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600",
#             # "https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=600",
#             # "https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=600"
#             "/static/images/products/Amethyst/Amethyst_2.png"
#         ]
#     },
#     {
#         "name": "Black Tourmaline Standing Piece",
#         "slug": "black-tourmaline-standing",
#         "sku": "CL-BT-001",
#         "category_slug": "black-tourmaline",
#         "description": "A naturally striated Black Tourmaline standing piece with a flat base. The parallel vertical lines are the crystal's signature — channels through which energy flows and transmutes.",
#         "story": "You place a Black Tourmaline at your door not because you fear what comes in, but because you value what you have built inside. It is the guardian stone.",
#         "healing_props": "Psychic protection. EMF shielding. Grounding. Removes negative energy from environments. Reduces anxiety and fear. Excellent near electronics.",
#         "chakra": "Root",
#         "zodiac": "Capricorn, Scorpio",
#         "origin": "Brazil",
#         "weight_grams": 240.0,
#         "dimensions": "10-12 cm height",
#         "price": 2100.00,
#         "compare_price": 2800.00,
#         "stock_qty": 15,
#         "is_featured": True,
#         "is_bestseller": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1573408301185-9519f94ae39c?w=600",
#             # "https://images.unsplash.com/photo-1516796181074-bf453fbfa3e6?w=600",
#             # "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=600"
#             "/static/images/products/Black_Tourmaline/Black_Tourmaline_1.png"

#         ]
#     },
#     {
#         "name": "Natural Citrine Point",
#         "slug": "natural-citrine-point",
#         "sku": "CL-CIT-001",
#         "category_slug": "citrine",
#         "description": "A natural (not heat-treated) Citrine point from the Congo. Pale yellow to honey-gold, these are rarer and more powerful than the heat-treated variety. Each piece is a genuine sun-coloured miracle.",
#         "story": "True natural Citrine is rare. Most 'Citrine' on the market is Amethyst baked until golden. Ours is the real thing — formed naturally, carrying genuine solar energy.",
#         "healing_props": "Abundance and manifestation. Creativity and motivation. Dispels negativity. Boosts self-confidence. Activates the solar plexus. The stone of joy.",
#         "chakra": "Solar Plexus, Sacral",
#         "zodiac": "Aries, Gemini, Leo, Libra",
#         "origin": "Democratic Republic of Congo",
#         "weight_grams": 75.0,
#         "dimensions": "7-9 cm height",
#         "price": 2400.00,
#         "compare_price": 3000.00,
#         "stock_qty": 20,
#         "is_featured": True,
#         "is_new_arrival": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1597149693980-d91f62c8f8c4?w=600",
#             # "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=600",
#             # "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=600"
#             "/static/images/products/Citrine/Citrine_1.png"
#         ]
#     },
#     {
#         "name": "Labradorite Freeform",
#         "slug": "labradorite-freeform",
#         "sku": "CL-LAB-001",
#         "category_slug": "labradorite",
#         "description": "A stunning Labradorite freeform with exceptional labradorescence — flashing blue, gold, and green across its surface as it catches the light. Each piece is a unique work of natural art.",
#         "story": "Every angle tells a different story. This is the nature of Labradorite, and the nature of magic — it reveals itself only to those willing to look from new perspectives.",
#         "healing_props": "Awakens psychic abilities. Strengthens intuition. Transformation and change. Protects the aura. Stimulates imagination. Excellent for shadow work.",
#         "chakra": "Throat, Third Eye, Crown",
#         "zodiac": "Leo, Scorpio, Sagittarius",
#         "origin": "Madagascar",
#         "weight_grams": 310.0,
#         "dimensions": "8-10 cm",
#         "price": 3500.00,
#         "compare_price": 4200.00,
#         "stock_qty": 11,
#         "is_featured": True,
#         "is_bestseller": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1535412833400-40b4f58cbf04?w=600",
#             # "https://images.unsplash.com/photo-1516796181074-bf453fbfa3e6?w=600",
#             # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600"
#             "/static/images/products/Labradorite/Labradorite_sphere_1.png",
#             "/static/images/products/Labradorite/Labradorite_sphere_2.png"
#         ]
#     },
#     {
#         "name": "Selenite Charging Plate",
#         "slug": "selenite-charging-plate",
#         "sku": "CL-SEL-001",
#         "category_slug": "selenite",
#         "description": "A beautifully smooth, oval Selenite charging plate for cleansing and recharging your crystal collection overnight. Translucent white with natural striations.",
#         "story": "Leave your crystals here overnight and return to find them reset, cleansed, and ready — as if the moon itself passed over them while you slept.",
#         "healing_props": "Cleanses other crystals. Purifies environments. Connects to higher consciousness. Aids mental clarity. Promotes peaceful sleep. Never needs cleansing.",
#         "chakra": "Crown, Third Eye",
#         "zodiac": "Taurus, Cancer",
#         "origin": "Morocco",
#         "weight_grams": 450.0,
#         "dimensions": "20 x 10 cm",
#         "price": 1650.00,
#         "compare_price": 2000.00,
#         "stock_qty": 22,
#         "is_bestseller": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1551361415-69c87624334f?w=600",
#             # "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=600",
#             # "https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=600"
#             "/static/images/products/Selenite/Selenite_1.png"
#         ]
#     },
#     {
#         "name": "Lapis Lazuli Sphere",
#         "slug": "lapis-lazuli-sphere",
#         "sku": "CL-LAP-001",
#         "category_slug": "lapis-lazuli",
#         "description": "A richly coloured Lapis Lazuli sphere with deep blue colouring and visible gold pyrite inclusions — the night sky made stone. Polished to a high mirror shine.",
#         "story": "This is the stone that painted the Sistine Chapel. The stone Cleopatra wore as eyeshadow. When you hold this sphere, you hold 6,000 years of human wisdom.",
#         "healing_props": "Truth and self-expression. Enhances wisdom and intellectual ability. Activates the higher mind. Aids communication. Reveals inner truth.",
#         "chakra": "Third Eye, Throat",
#         "zodiac": "Sagittarius, Aquarius",
#         "origin": "Afghanistan",
#         "weight_grams": 390.0,
#         "dimensions": "7 cm diameter",
#         "price": 4800.00,
#         "compare_price": 6000.00,
#         "stock_qty": 7,
#         "is_featured": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600",
#             # "https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=600",
#             # "https://images.unsplash.com/photo-1573408301185-9519f94ae39c?w=600"
#             "/static/images/products/Lapis_lazuli/Lapis_lazuli_1.png"
#         ]
#     },
#     {
#         "name": "Crystal Starter Set",
#         "slug": "crystal-starter-set",
#         "sku": "CL-SET-001",
#         "category_slug": "quartz",
#         "description": "The perfect introduction to the world of crystals — seven carefully chosen stones representing seven intentions: love, protection, clarity, abundance, peace, truth, and grounding.",
#         "story": "Every journey begins with a single stone. This set is the beginning of yours — curated by our crystal experts to cover every dimension of wellbeing.",
#         "healing_props": "Comprehensive energy support. Includes: Clear Quartz, Rose Quartz, Amethyst, Black Tourmaline, Citrine, Selenite, and Labradorite. Complete chakra coverage.",
#         "chakra": "All Chakras",
#         "zodiac": "All Signs",
#         "origin": "Multiple Origins",
#         "weight_grams": 350.0,
#         "dimensions": "Wooden Gift Box",
#         "price": 4999.00,
#         "compare_price": 6500.00,
#         "stock_qty": 30,
#         "is_featured": True,
#         "is_bestseller": True,
#         "is_new_arrival": True,
#         "images": [
#             "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=600",
#             "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600"
#         ]
#     },
#     {
#         "name": "Jewellery Designs",
#         "slug": "jewellery",
#         "sku": "CL-JEL-001",
#         "category_slug": "jewellery",
#         "description": "Luxury wearable crystal energy.",
#         "story": "Elegant handcrafted crystal jewellery infused with healing stones.",
#         "healing_props": "Comprehensive energy support. Includes: Clear Quartz, Rose Quartz, Amethyst, Black Tourmaline, Citrine, Selenite, and Labradorite. Complete chakra coverage.",
#         "chakra": "All Chakras",
#         "zodiac": "All Signs",
#         "origin": "Multiple Origins",
#         "weight_grams": 350.0,
#         "dimensions": "Wooden Gift Box",
#         "price": 4999.00,
#         "compare_price": 6500.00,
#         "stock_qty": 30,
#         "is_featured": True,
#         "is_bestseller": True,
#         "is_new_arrival": True,
#         "images": [
#             # "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=600",
#             # "https://images.unsplash.com/photo-1567225557594-88d73398014a?w=600"
#             "/static/images/products/jewllery/bracelets.png"
#         ]
#     }
# ]

# for pd in products_data:
#     existing = db.query(Product).filter(Product.slug == pd["slug"]).first()
#     if not existing:
#         images = pd.pop("images", [])
#         cat_slug = pd.pop("category_slug")
#         cat_id = cat_map.get(cat_slug)
#         if not cat_id:
#             continue
#         product = Product(category_id=cat_id, **pd)
#         db.add(product)
#         db.flush()
#         for i, url in enumerate(images):
#             img = ProductImage(
#                 product_id=product.id,
#                 url=url,
#                 is_primary=(i == 0),
#                 sort_order=i
#             )
#             db.add(img)
#         print(f"  ✓ Product: {product.name}")

# db.commit()
# db.close()
# print("\n✅ Database seeded successfully!")


################################################################################################



################################################################################################



################################################################################################


"""
Glow With Ritz — Database Seed Script
Format mirrors the original project seed.py exactly.
All products are seeded once; after that, use the Admin Portal
to add / edit / delete products via full CRUD operations.

Run:
    cd backend
    rm -f *.db
    python seed.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.user import User, Category, Product, ProductImage
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ═══════════════════════════════════════════════════════════════════════════════
# USERS
# ═══════════════════════════════════════════════════════════════════════════════

if not db.query(User).filter(User.email == "admin@glowwithritz.com").first():
    db.add(User(
        full_name="Glow With Ritz Admin",
        email="admin@glowwithritz.com",
        hashed_password=get_password_hash("Admin@123"),
        is_admin=True
    ))
    db.commit()
    print("✓ Admin user created   : admin@glowwithritz.com / Admin@123")

if not db.query(User).filter(User.email == "demo@glowwithritz.com").first():
    db.add(User(
        full_name="Demo Customer",
        email="demo@glowwithritz.com",
        hashed_password=get_password_hash("Demo@123"),
        is_admin=False,
        phone="+91 98765 43210"
    ))
    db.commit()
    print("✓ Consumer user created: demo@glowwithritz.com / Demo@123")

# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORIES
# ═══════════════════════════════════════════════════════════════════════════════

categories_data = [
    {
        "name": "Quartz Crystals",
        "slug": "quartz",
        "description": "The master healers — pure, powerful, and endlessly versatile.",
        "story": "Born deep within the earth's crust over millions of years, Quartz is the most abundant crystal on our planet, yet its power is anything but ordinary. Revered by ancient civilisations from the Egyptians to the Japanese — who called it suisho, meaning 'perfect jewel' — Quartz is the ultimate amplifier of intention. Our collection is hand-sourced from the ancient riverbeds of the Himalayas and the mines of Madagascar, each piece carrying the memory of the earth itself.",
        "image_url": "/static/images/categories/Quartz.png",
        "banner_url": "/static/images/banners/Quartz.png",
        "sort_order": 1
    },
    {
        "name": "Amethyst",
        "slug": "amethyst",
        "description": "The stone of spiritual wisdom and inner calm.",
        "story": "The Greeks believed Amethyst could prevent intoxication — its very name derives from amethystos, 'not drunk'. But its true intoxication is of a higher kind: the quiet, violet-hued serenity that settles over you when you hold a genuine Amethyst. Our collection is sourced from the deep violet mines of Uruguay and the pale lilac deposits of Zambia.",
        "image_url": "/static/images/categories/Amethyst_1.jpeg",
        "banner_url": "/static/images/banners/Amethyst.png",
        "sort_order": 2
    },
    {
        "name": "Rose Quartz",
        "slug": "rose-quartz",
        "description": "The eternal stone of love, compassion, and tender grace.",
        "story": "Long before Valentine's Day existed, Rose Quartz was already humanity's love letter to itself. Ancient Romans carved it into seals. Egyptians fashioned it into amulets to prevent ageing. Today we know it simply as the stone of the heart — a gentle, rose-pink crystal that holds space for self-love, romantic love, and the love that dissolves grief.",
        "image_url": "/static/images/categories/Rose_Quartz.png",
        "banner_url": "/static/images/banners/Rose_Quartz.png",
        "sort_order": 3
    },
    {
        "name": "Black Tourmaline",
        "slug": "black-tourmaline",
        "description": "The ultimate protector — a shield of dark, grounded energy.",
        "story": "In a world of noise, Black Tourmaline is silence. It is the crystal that shamans carried into battle, that miners tucked into their pockets before descending into the earth. Scientifically pyroelectric — it generates an electric charge when heated — it actively transmutes negative energy into neutral, protective light.",
        "image_url": "/static/images/categories/Black_Tourmaline.png",
        "banner_url": "/static/images/banners/Black_Tourmaline.png",
        "sort_order": 4
    },
    {
        "name": "Citrine",
        "slug": "citrine",
        "description": "The merchant's stone — abundance, optimism, and solar radiance.",
        "story": "Called the Merchant's Stone and the Sun Stone, Citrine carries the warmth of the sun within its golden depths. Unlike most crystals it does not hold negative energy — it transmutes, dissipates, and grounds it. Medieval merchants kept Citrine in their coin purses. Our collection spans the full solar spectrum — from pale champagne to deep amber.",
        "image_url": "/static/images/categories/Citrine.png",
        "banner_url": "/static/images/banners/Citrine.png",
        "sort_order": 5
    },
    {
        "name": "Labradorite",
        "slug": "labradorite",
        "description": "The stone of magic, transformation, and hidden light.",
        "story": "Inuit legend says the Northern Lights were once trapped inside rocks along the Labrador coast — until a warrior struck the rocks with his spear and freed them into the sky. Some lights remained, and those became Labradorite. Grey and unassuming from most angles, then suddenly — flash — a wing of peacock blue, a wash of copper gold.",
        "image_url": "/static/images/categories/Labradorite.jpeg",
        "banner_url": "/static/images/banners/Labradorite.png",
        "sort_order": 6
    },
    {
        "name": "Selenite",
        "slug": "selenite",
        "description": "Liquid moonlight in solid form — the purest cleansing crystal.",
        "story": "Named after Selene, the Greek goddess of the moon, Selenite is perhaps the most ethereal crystal in existence — translucent as frosted glass, soft as chalk, glowing from within. It is one of only a handful of crystals that never needs cleansing, because it is cleansing — place other crystals upon a Selenite plate and watch them reset overnight.",
        "image_url": "/static/images/categories/Selenite.png",
        "banner_url": "/static/images/banners/Selenite.png",
        "sort_order": 7
    },
    {
        "name": "Lapis Lazuli",
        "slug": "lapis-lazuli",
        "description": "The royal stone of truth, wisdom, and celestial vision.",
        "story": "For over 6,000 years, Lapis Lazuli has been the stone of kings and philosophers. Ground into powder, it became ultramarine — the most precious pigment in the world, used to paint the robes of the Virgin Mary and the ceiling of the Sistine Chapel. Worn by Cleopatra as eyeshadow. Buried with Tutankhamun.",
        "image_url": "/static/images/categories/Lapis_lazuli.png",
        "banner_url": "/static/images/banners/Lapis_lazuli.png",
        "sort_order": 8
    },
    # ── Premium Collection — Jewellery sub-categories ──────────────────────────
    {
        "name": "Crystal Bracelets",
        "slug": "crystal-bracelets",
        "description": "Natural crystal bracelets for healing, wealth, protection and personal alignment.",
        "story": "Worn on the wrist, these crystal bracelets keep healing energy in constant contact with your pulse — your most intimate and continuous point of intention throughout the day.",
        "image_url": "/static/images/categories/jewellery.png",
        "banner_url": "/static/images/banners/jewellery.png",
        "sort_order": 9
    },
    {
        "name": "Anklets",
        "slug": "anklets",
        "description": "Elegant gemstone anklets — a graceful way to carry healing energy every step.",
        "story": "Anklets have been worn across cultures for centuries as symbols of feminine protection and beauty. Each step becomes an act of intention when your anklet carries healing crystals.",
        "image_url": "/static/images/categories/jewellery.png",
        "banner_url": "/static/images/banners/jewellery.png",
        "sort_order": 10
    },
    {
        "name": "Pendants & Malas",
        "slug": "pendants-malas",
        "description": "Crystal pendants, Karungali malas, and zodiac power combos.",
        "story": "Worn at the heart chakra, pendants carry intention and protection wherever you go. Our malas range from traditional 108-bead meditation tools to modern zodiac power combos.",
        "image_url": "/static/images/categories/jewellery.png",
        "banner_url": "/static/images/banners/jewellery.png",
        "sort_order": 11
    },
    {
        "name": "Rudraksha",
        "slug": "rudraksha",
        "description": "Authentic Rudraksha beads and malas — sacred seeds of Lord Shiva.",
        "story": "Rudraksha seeds have been worn in meditation and prayer for thousands of years across the Indian subcontinent. Each bead is a direct gift from Lord Shiva — a seed of divine consciousness that has taken physical form for the benefit of the wearer.",
        "image_url": "/static/images/categories/Quartz.png",
        "banner_url": "/static/images/banners/Quartz.png",
        "sort_order": 12
    },
    # ── Premium Collection — Crystal Designs sub-categories ────────────────────
    {
        "name": "Yantras & Frames",
        "slug": "yantras-frames",
        "description": "Sacred Yantras, crystal pyramids, and spiritual frames for wealth and success.",
        "story": "A Yantra is not decoration — it is a living geometric field of energy. When properly energised, it operates ceaselessly in the background, drawing abundance, protection, or divine blessings toward its owner.",
        "image_url": "/static/images/categories/crystal_designs.png",
        "banner_url": "/static/images/banners/crystal_designs.png",
        "sort_order": 13
    },
    {
        "name": "Crystal Designs",
        "slug": "crystal-designs",
        "description": "Crystal trees, dome pieces, and sacred crystal art for your home.",
        "story": "Crystal art forms radiate energy in all directions, filling your space with the continuous vibration of intention and beauty. Each piece is handcrafted and energetically verified.",
        "image_url": "/static/images/categories/crystal_designs.png",
        "banner_url": "/static/images/banners/crystal_designs.png",
        "sort_order": 14
    },
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

# ═══════════════════════════════════════════════════════════════════════════════
# PRODUCTS
#
# images[] rules:
#   images[0]   → is_primary = True  → shown as the card listing image
#   images[1..] → is_primary = False → shown as gallery thumbnails in product page
#
# After seeding, use the Admin Portal to:
#   • Add / remove images per product
#   • Change the primary image
#   • Edit any product field
#   • Create or delete products
# ═══════════════════════════════════════════════════════════════════════════════

products_data = [

    # ──────────────────────────────────────────────────────────────────────────
    # GWR SIGNATURE CRYSTALS  (images from /static/images/products/)
    # ──────────────────────────────────────────────────────────────────────────
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
            "/static/images/products/Quartz/Quartz_1.png",   # primary — card image
            "/static/images/products/Quartz/Quartz_2.png",   # gallery thumbnail 1
        ]
    },
    {
        "name": "Smoky Quartz Tower",
        "slug": "smoky-quartz-tower",
        "sku": "CL-QTZ-002",
        "category_slug": "quartz",
        "description": "A deeply grounding Smoky Quartz tower with rich, translucent brown-grey colouring. Hand-polished to a high shine, it stands as a powerful centrepiece for any space.",
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
            "/static/images/products/Quartz/Quartz_2.png",   # primary
            "/static/images/products/Quartz/Quartz_1.png",   # gallery thumbnail 1
        ]
    },
    {
        "name": "Rose Quartz Sphere",
        "slug": "rose-quartz-sphere",
        "sku": "CL-RQ-001",
        "category_slug": "rose-quartz",
        "description": "A perfectly polished Rose Quartz sphere of exceptional colour depth from Madagascar. The sphere shape radiates energy in all directions, filling your space with gentle, loving vibration.",
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
            "/static/images/products/Rose_Quartz/Rose_quartz_1.jpeg",  # primary
            "/static/images/products/Rose_Quartz/Rose_quartz_2.jpeg",  # gallery thumbnail 1
        ]
    },
    {
        "name": "Raw Rose Quartz Cluster",
        "slug": "raw-rose-quartz-cluster",
        "sku": "CL-RQ-002",
        "category_slug": "rose-quartz",
        "description": "A raw, unpolished Rose Quartz cluster with natural matrix from Madagascar. The rough surface catches light differently at each angle, revealing pale pink depths.",
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
            "/static/images/products/Rose_Quartz/Rose_quartz_2.jpeg",  # primary
            "/static/images/products/Rose_Quartz/Rose_quartz_1.jpeg",  # gallery thumbnail 1
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
            "/static/images/products/Amethyst/Amethyst_1.png",   # primary
            "/static/images/products/Amethyst/Amethyst_2.png",   # gallery thumbnail 1
        ]
    },
    {
        "name": "Amethyst Palm Stone",
        "slug": "amethyst-palm-stone",
        "sku": "CL-AMT-002",
        "category_slug": "amethyst",
        "description": "A smoothly polished Amethyst palm stone shaped to rest perfectly in the hand during meditation. Medium purple with natural banding and internal clarity.",
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
            "/static/images/products/Amethyst/Amethyst_2.png",   # primary
            "/static/images/products/Amethyst/Amethyst_1.png",   # gallery thumbnail 1
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
            "/static/images/products/Black_Tourmaline/Black_Tourmaline_1.png",   # primary
            "/static/images/products/Black_Tourmaline/Black_tourmaline_2.png",   # gallery thumbnail 1
        ]
    },
    {
        "name": "Natural Citrine Point",
        "slug": "natural-citrine-point",
        "sku": "CL-CIT-001",
        "category_slug": "citrine",
        "description": "A natural (not heat-treated) Citrine point from the Congo. Pale yellow to honey-gold, these are rarer and more powerful than the heat-treated variety.",
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
            "/static/images/products/Citrine/Citrine_1.png",   # primary
            "/static/images/products/Citrine/Citrine_2.png",   # gallery thumbnail 1
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
            "/static/images/products/Labradorite/Labradorite_sphere_1.png",   # primary
            "/static/images/products/Labradorite/Labradorite_sphere_2.png",   # gallery thumbnail 1
            "/static/images/products/Labradorite/Labradorite_heart_1.png",    # gallery thumbnail 2
            "/static/images/products/Labradorite/Labradorite_heart_2.png",    # gallery thumbnail 3
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
            "/static/images/products/Selenite/Selenite_1.png",   # primary
            "/static/images/products/Selenite/Selenite_2.png",   # gallery thumbnail 1
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
            "/static/images/products/Lapis_lazuli/Lapis_lazuli_1.png",   # primary
            "/static/images/products/Lapis_lazuli/Lapis_lazuli_2.png",   # gallery thumbnail 1
        ]
    },
    {
        "name": "Crystal Starter Set — 7 Stones",
        "slug": "crystal-starter-set",
        "sku": "CL-SET-001",
        "category_slug": "quartz",
        "description": "The perfect introduction to the world of crystals — seven carefully chosen stones representing seven intentions: love, protection, clarity, abundance, peace, truth, and grounding.",
        "story": "Every journey begins with a single stone. This set is the beginning of yours — curated by Ritz to cover every dimension of wellbeing, from the heart to the crown.",
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
            "/static/images/products/Quartz/Quartz_1.png",                  # primary
            "/static/images/products/Rose_Quartz/Rose_quartz_1.jpeg",        # gallery thumbnail 1
            "/static/images/products/Amethyst/Amethyst_1.png",               # gallery thumbnail 2
            "/static/images/products/Citrine/Citrine_1.png",                 # gallery thumbnail 3
        ]
    },


    # ──────────────────────────────────────────────────────────────────────────
    # GEMSFOREVER.IN PRODUCTS  (40 items with matching image folder names)
    # images[0] = primary card image | images[1+] = gallery thumbnails
    # Image path format: /static/images/products/<Exact Folder Name>/image1.png
    # ──────────────────────────────────────────────────────────────────────────
    {
        "name": "13 Mukhi Rudraksha Bead In 5 Mukhi Rudraksha Mala",
        "slug": "13-mukhi-rudraksha-bead-in-5-mukhi-mala",
        "sku": "GF-RDR-013",
        "category_slug": "rudraksha",
        "description": "The 13 Mukhi Rudraksha is blessed by Lord Indra and Kamadeva — the deity of love and attraction. Set within a 5 Mukhi mala for daily wear and enhanced protection.",
        "story": "The 13 Mukhi is among the rarest Rudrakshas — its wearer receives blessings of the Sapta Rishis. Each bead is individually certified and energised before dispatch.",
        "healing_props": "Attraction and charisma. Fulfils desires and wishes. Spiritual awakening. Balance and protection. Divine blessings of Lord Indra.",
        "chakra": "Crown, Throat",
        "zodiac": None,
        "origin": "Nepal/India",
        "weight_grams": None,
        "dimensions": "Standard mala length",
        "price": 24999.00,
        "compare_price": 49999.00,
        "stock_qty": 5,
        "is_featured": True,
        "is_bestseller": False,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/13 Mukhi Rudraksha Bead In 5 Mukhi Rudraksha Mala/image1.png",
        ]
    },
    {
        "name": "Authentic 7 Chakra Dome Tree",
        "slug": "authentic-7-chakra-dome-tree",
        "sku": "GF-CDN-007",
        "category_slug": "crystal-designs",
        "description": "A handcrafted 7 Chakra dome tree featuring crystal chips representing each chakra — Red Jasper, Carnelian, Citrine, Green Aventurine, Sodalite, Amethyst and Clear Quartz.",
        "story": "The dome tree combines sacred geometry with the healing energy of all seven chakra crystals. Place it in your living space to maintain energetic balance throughout your home.",
        "healing_props": "Balances and aligns all seven chakras. Promotes harmony and protection. Enhances positive energy flow throughout the home.",
        "chakra": "All Chakras",
        "zodiac": None,
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Approx. 18-22 cm height",
        "price": 999.00,
        "compare_price": 1999.00,
        "stock_qty": 20,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Authentic 7 Chakra Dome Tree _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Authentic Amazonite Bracelet",
        "slug": "authentic-amazonite-bracelet",
        "sku": "GF-BRC-AMZ",
        "category_slug": "crystal-bracelets",
        "description": "A natural Amazonite bead bracelet — the stone of courage and truth. Amazonite's beautiful teal-green colour brings calm, clarity and the courage to speak your truth.",
        "story": "Named after the Amazon River, this stone was carried by female warriors for courage. Today it empowers all who wear it to live authentically and communicate with confidence.",
        "healing_props": "Balance and protection. Calms anxiety and fear. Encourages truth and communication. Soothes emotional trauma. Promotes harmony in relationships.",
        "chakra": "Heart, Throat",
        "zodiac": "Virgo, Aquarius",
        "origin": "India",
        "weight_grams": 38.0,
        "dimensions": "Standard size, 8mm beads",
        "price": 699.00,
        "compare_price": 1399.00,
        "stock_qty": 35,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Authentic Amazonite Bracelet _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Authentic Evil Eye Dome Tree",
        "slug": "authentic-evil-eye-dome-tree",
        "sku": "GF-CDN-EVL",
        "category_slug": "crystal-designs",
        "description": "A handcrafted Evil Eye dome tree combining crystal chips with the powerful Evil Eye symbol — one of the most ancient symbols of protection across cultures.",
        "story": "The Evil Eye has been used as a protective talisman for over 3,000 years. This dome tree brings that ancient protective energy into your home in a beautiful, modern form.",
        "healing_props": "Powerful protection against negative energy and ill will. Deflects the evil eye. Promotes safety and positive energy in the home.",
        "chakra": "Root, Third Eye",
        "zodiac": None,
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Approx. 18-22 cm height",
        "price": 899.00,
        "compare_price": 1799.00,
        "stock_qty": 18,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Authentic Evil Eye Dome Tree _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Authentic Garnet Anklet Maha Lakshmi Siddhi",
        "slug": "authentic-garnet-anklet-maha-lakshmi-siddhi",
        "sku": "GF-ANK-GRN",
        "category_slug": "anklets",
        "description": "A deep red Garnet anklet energised with Maha Lakshmi Siddhi — combining Garnet's root chakra power with the divine abundance blessings of Goddess Lakshmi.",
        "story": "Garnet has been worn for protection and vitality for over 5,000 years. This anklet is elevated by the sacred Maha Lakshmi Siddhi energisation ritual for both protection and prosperity.",
        "healing_props": "Balance and protection. Maha Lakshmi blessings. Root chakra grounding. Passion and vitality. Attracts abundance and love.",
        "chakra": "Root",
        "zodiac": "Capricorn, Aquarius, Leo",
        "origin": "India",
        "weight_grams": 28.0,
        "dimensions": "Adjustable anklet",
        "price": 849.00,
        "compare_price": 1699.00,
        "stock_qty": 22,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Authentic Garnet Anklet Maha Lakshmi Siddhi _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Authentic Maha Lakshmi Kripa Combo With 7 Mukhi Rudraksha",
        "slug": "authentic-maha-lakshmi-kripa-combo-7-mukhi-rudraksha",
        "sku": "GF-CMB-MLK",
        "category_slug": "rudraksha",
        "description": "A powerful combo combining Maha Lakshmi blessings with the 7 Mukhi Rudraksha — ruled by Goddess Lakshmi herself — designed to attract wealth, success and divine grace.",
        "story": "The 7 Mukhi Rudraksha is directly associated with Goddess Lakshmi. Combined with Lakshmi Kripa sacred items, it creates an unparalleled wealth attraction and protection combo.",
        "healing_props": "Balance and protection. Maha Lakshmi blessings. Wealth and abundance. 7 Mukhi prosperity energy. Removes financial obstacles. Divine grace.",
        "chakra": "Crown, Solar Plexus",
        "zodiac": None,
        "origin": "Nepal/India",
        "weight_grams": None,
        "dimensions": "Combo set",
        "price": 1299.00,
        "compare_price": 2599.00,
        "stock_qty": 15,
        "is_featured": True,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Authentic Maha Lakshmi Kripa Combo With 7 Mukhi Rudraksha _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Authentic Triple Protection Bracelet 8mm",
        "slug": "authentic-triple-protection-bracelet-8mm",
        "sku": "GF-BRC-TPL",
        "category_slug": "crystal-bracelets",
        "description": "The ultimate protection bracelet combining Black Tourmaline, Obsidian and Hematite in 8mm beads — triple shielding against negativity, psychic attack and EMF radiation.",
        "story": "Three is the number of completion in crystal healing. This triple combination creates a complete energetic shield — transmuting (Black Tourmaline), grounding (Hematite) and sealing (Obsidian) simultaneously.",
        "healing_props": "Healing and clarity. Triple layer of protection. Shields against negative energy and psychic attack. EMF protection. Grounding and stabilising. Positive energy.",
        "chakra": "Root",
        "zodiac": "Scorpio, Capricorn, Aries",
        "origin": "India",
        "weight_grams": 45.0,
        "dimensions": "Standard size, 8mm beads",
        "price": 799.00,
        "compare_price": 1599.00,
        "stock_qty": 40,
        "is_featured": True,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Authentic Triple Protection Bracelet 8Mm For Protection Positive Energy _ Healing & Clarity/image1.png",
        ]
    },
    {
        "name": "Classic 14 Mukhi Rudraksha Bead In 5 Mukhi Rudraksha Mala",
        "slug": "classic-14-mukhi-rudraksha-bead-in-5-mukhi-mala",
        "sku": "GF-RDR-014",
        "category_slug": "rudraksha",
        "description": "The 14 Mukhi Rudraksha ruled by Lord Hanuman — bestowing fearlessness, strength and divine protection. Set within a 5 Mukhi mala. Certificate of authenticity included.",
        "story": "The 14 Mukhi is among the rarest of all Rudrakshas. Lord Hanuman's energy makes this bead especially powerful for courage and protection in all endeavours.",
        "healing_props": "Balance and protection. Fearlessness and inner strength. Divine protection of Lord Hanuman. Clarity of mind. Deep meditation support. Certified authentic.",
        "chakra": "Crown",
        "zodiac": None,
        "origin": "Nepal/India",
        "weight_grams": None,
        "dimensions": "Standard mala length",
        "price": 49999.00,
        "compare_price": 99999.00,
        "stock_qty": 5,
        "is_featured": True,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Classic 14 Mukhi Rudraksha Bead In 5 Mukhi Rudraksha Mala _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Classic Clear Quartz Tumble",
        "slug": "classic-clear-quartz-tumble",
        "sku": "GF-QTZ-TBL",
        "category_slug": "quartz",
        "description": "A beautifully polished Clear Quartz tumble stone — the master healer in its most portable form. Smooth, clear and unique with natural inclusions. Perfect for meditation or pocket carry.",
        "story": "Tumble stones are the most intimate way to work with crystals — small enough to carry in your pocket or hold during meditation. Clear Quartz amplifies every intention you bring to it.",
        "healing_props": "Healing and clarity. Amplifies energy and intention. Enhances clarity of thought. Master healer. Aids meditation. Boosts the immune system. Purifies energy.",
        "chakra": "Crown, All Chakras",
        "zodiac": "All Signs",
        "origin": "India",
        "weight_grams": 25.0,
        "dimensions": "Approx. 2-3 cm",
        "price": 299.00,
        "compare_price": 599.00,
        "stock_qty": 60,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Classic Clear Quartz Tumble _ Healing & Clarity/image1.png",
        ]
    },
    {
        "name": "Classic Nepal Origin 17 Mukhi Rudraksha 17mm to 22mm",
        "slug": "classic-nepal-origin-17-mukhi-rudraksha",
        "sku": "GF-RDR-017",
        "category_slug": "rudraksha",
        "description": "Nepal-origin 17 Mukhi Rudraksha (17-22mm) — one of the rarest and most powerful beads available. Ruled by Vishwakarma, the divine architect. Lab certified with authenticity certificate.",
        "story": "The 17 Mukhi is said to fulfil all material and spiritual desires simultaneously. Nepal-origin beads are considered superior due to the unique soil composition and altitude of the Himalayas.",
        "healing_props": "Balance and protection. Fulfils material and spiritual desires. Vishwakarma blessings for success in all work. Rare and powerful. Certificate of authenticity included.",
        "chakra": "Crown",
        "zodiac": None,
        "origin": "Nepal",
        "weight_grams": None,
        "dimensions": "17mm to 22mm bead size",
        "price": 89999.00,
        "compare_price": 179999.00,
        "stock_qty": 2,
        "is_featured": True,
        "is_bestseller": False,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Classic Nepal Origin 17 Mukhi Rudraksha 17Mm To 22Mm _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Divine Dhan Yog Bracelet With Zodiac Charm Pisces",
        "slug": "divine-dhan-yog-bracelet-zodiac-pisces",
        "sku": "GF-BRC-DYP",
        "category_slug": "crystal-bracelets",
        "description": "The Dhan Yog wealth bracelet paired with a Pisces zodiac charm — channelling both financial prosperity and the deep intuitive spiritual nature of the Pisces sign.",
        "story": "Dhan Yog is an auspicious planetary alignment for wealth in Vedic astrology. Paired with Pisces energy, this bracelet channels spiritual abundance and financial prosperity simultaneously.",
        "healing_props": "Wealth and success. Amplifies Pisces intuition and abundance. Financial manifestation. Spiritual depth. Activates solar plexus chakra.",
        "chakra": "Solar Plexus",
        "zodiac": "Pisces",
        "origin": "India",
        "weight_grams": 38.0,
        "dimensions": "Standard size",
        "price": 899.00,
        "compare_price": 1799.00,
        "stock_qty": 25,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Divine Dhan Yog Bracelet With Zodiac Charm Pisces _ Wealth & Success/image1.png",
        ]
    },
    {
        "name": "Divine Metal Rudraksha And Karungali Bracelet Black",
        "slug": "divine-metal-rudraksha-karungali-bracelet-black",
        "sku": "GF-BRC-MRK",
        "category_slug": "crystal-bracelets",
        "description": "A powerful black-toned bracelet combining Rudraksha beads and Karungali (Ebony wood) beads with metal accents — triple protection from three of India's most sacred protective materials.",
        "story": "Black is the colour of ultimate protection. This bracelet unites Rudraksha, Karungali and metal — three powerful protective traditions from different corners of Indian spirituality.",
        "healing_props": "Balance and protection. Triple-layer protection. Rudraksha's divine energy. Karungali's sacred protection. Grounding and stability. Shields from all negative energy.",
        "chakra": "Root, Crown",
        "zodiac": None,
        "origin": "South India",
        "weight_grams": 42.0,
        "dimensions": "Standard size",
        "price": 799.00,
        "compare_price": 1599.00,
        "stock_qty": 20,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Divine Metal Rudraksha And Karungali Bracelet Black _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Divine Nepal Origin 6 Mukhi Rudraksha Without Silver Capping",
        "slug": "divine-nepal-origin-6-mukhi-rudraksha",
        "sku": "GF-RDR-006N",
        "category_slug": "rudraksha",
        "description": "Nepal-origin 6 Mukhi Rudraksha (17-22mm) without silver capping — the pure natural bead in its most authentic form. Ruled by Lord Kartikeya, bestowing wisdom, willpower and learning.",
        "story": "Nepal-origin Rudrakshas are prized above all others for their size, clarity and energy. Without silver capping, this bead offers the most direct contact with its inherent spiritual energy.",
        "healing_props": "Balance and protection. Lord Kartikeya blessings. Wisdom and willpower. Enhances learning and focus. Emotional stability. Removes laziness and indecision.",
        "chakra": "Sacral, Solar Plexus",
        "zodiac": None,
        "origin": "Nepal",
        "weight_grams": None,
        "dimensions": "17mm to 22mm bead size",
        "price": 5999.00,
        "compare_price": 11999.00,
        "stock_qty": 8,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Divine Nepal Origin 6 Mukhi Rudraksha 17Mm To 22Mm Without Silver Capping _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Divine Pyrite Shree Yantra Frame Crystal Wall Art",
        "slug": "divine-pyrite-shree-yantra-frame-crystal-wall-art",
        "sku": "GF-YNT-SHR",
        "category_slug": "yantras-frames",
        "description": "A stunning Pyrite Shree Yantra as crystal wall art — combining the sacred geometry of the Shree Yantra with natural Pyrite's abundance energy for home, office and Vastu correction.",
        "story": "The Shree Yantra is the most powerful of all Yantras — the geometric representation of the Divine Mother herself. Mounted on Pyrite, it becomes a continuous generator of wealth and positive energy.",
        "healing_props": "Wealth and success. Shree Yantra's supreme abundance power. Pyrite amplification. Vastu correction. Positive spiritual energy. Home and office prosperity.",
        "chakra": "Solar Plexus, Crown",
        "zodiac": None,
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Wall art frame size",
        "price": 1499.00,
        "compare_price": 2999.00,
        "stock_qty": 12,
        "is_featured": True,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Divine Pyrite Shree Yantra Frame Crystal Wall Art For Wealth Positivity Spiritual Energy Vastu Pyrite Shree Yantra For Home Office _ Wealth & Success/image1.png",
        ]
    },
    {
        "name": "Divine Shree Yantra On Raw Pyrite Frame Maha Lakshmi Siddhi",
        "slug": "divine-shree-yantra-raw-pyrite-frame-maha-lakshmi-siddhi",
        "sku": "GF-YNT-SHP",
        "category_slug": "yantras-frames",
        "description": "The Shree Yantra on a raw natural Pyrite frame, Siddh with Maha Lakshmi mantras — the most powerful wealth attraction piece in our entire collection.",
        "story": "Shree Yantra + Pyrite + Maha Lakshmi Siddhi: each of these three elements is independently powerful. Together they create an extraordinary continuous field of abundance energy.",
        "healing_props": "Wealth and success. Supreme Maha Lakshmi blessings. Shree Yantra divine geometry. Raw Pyrite amplification. Ultimate wealth attraction. Siddh energised.",
        "chakra": "Solar Plexus, Crown",
        "zodiac": None,
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Standard frame on raw Pyrite",
        "price": 1299.00,
        "compare_price": 2599.00,
        "stock_qty": 10,
        "is_featured": True,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Divine Shree Yantra On Raw Pyrite Frame Maha Lakshmi Siddhi _ Wealth & Success/image1.png",
        ]
    },
    {
        "name": "Divine Surya's Blessing Combo (Pack of 2)",
        "slug": "divine-surya-blessing-combo-pack-of-2",
        "sku": "GF-CMB-SRY",
        "category_slug": "crystal-designs",
        "description": "A pack of 2 items channelling Lord Surya's blessings — bringing clarity, health, confidence and solar energy into your daily life. An ideal gift for new beginnings.",
        "story": "Lord Surya is the source of all life, health and vitality in Vedic tradition. This combo channels his golden solar blessings through carefully selected crystals and sacred items.",
        "healing_props": "Wealth and success. Surya blessings for health and vitality. Solar energy and confidence. Clarity and leadership. Removes obstacles. Pack of 2 items.",
        "chakra": "Solar Plexus",
        "zodiac": "Leo, Aries",
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Pack of 2",
        "price": 999.00,
        "compare_price": 1999.00,
        "stock_qty": 18,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Divine Surya S Blessing Combo _ Wealth & Success (Pack Of 2 )/image1.png",
        ]
    },
    {
        "name": "Divine Zodiac Bracelet Capricorn",
        "slug": "divine-zodiac-bracelet-capricorn",
        "sku": "GF-BRC-CAP",
        "category_slug": "crystal-bracelets",
        "description": "A curated crystal bracelet for Capricorn — featuring crystals that amplify the sign's natural ambition, discipline and drive for long-term success and achievement.",
        "story": "Capricorn is the most disciplined sign of the zodiac — patient, persistent and built for the summit. This bracelet supports every step of the Capricorn's climb toward their biggest goals.",
        "healing_props": "Personal alignment and strength. Amplifies Capricorn's discipline. Career success and ambition. Grounding and stability. Long-term achievement energy.",
        "chakra": "Root, Solar Plexus",
        "zodiac": "Capricorn",
        "origin": "India",
        "weight_grams": 38.0,
        "dimensions": "Standard size",
        "price": 799.00,
        "compare_price": 1599.00,
        "stock_qty": 28,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Divine Zodiac Bracelet Capricon _ Personal Alignment & Strength/image1.png",
        ]
    },
    {
        "name": "Elegant Amethyst Pyramid",
        "slug": "elegant-amethyst-pyramid",
        "sku": "GF-PYR-AMT",
        "category_slug": "crystal-designs",
        "description": "A beautifully crafted natural Amethyst pyramid — combining Amethyst's powerful healing energy with pyramid sacred geometry for enhanced meditation and space clearing.",
        "story": "The pyramid shape concentrates energy upward through its apex. An Amethyst pyramid doubly amplifies spiritual energy, making it ideal for meditation rooms and sleep spaces.",
        "healing_props": "Healing and clarity. Calms the mind and aids sleep. Enhances intuition and psychic ability. Pyramid geometry amplifies Amethyst's spiritual energy.",
        "chakra": "Third Eye, Crown",
        "zodiac": "Virgo, Aquarius, Pisces",
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Approx. 5-7 cm base",
        "price": 699.00,
        "compare_price": 1399.00,
        "stock_qty": 22,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Elegant Amethyst Pyramid _ Healing & Clarity/image1.png",
        ]
    },
    {
        "name": "Elegant Black Obsidian Evil Eye Bracelet With Free Raw Selenite Plate",
        "slug": "elegant-black-obsidian-evil-eye-bracelet-with-selenite-plate",
        "sku": "GF-BRC-BOE",
        "category_slug": "crystal-bracelets",
        "description": "A Black Obsidian bracelet with Evil Eye charm — double protection combining volcanic glass energy with the ancient Evil Eye symbol. Comes with a complimentary raw Selenite plate.",
        "story": "Black Obsidian is volcanic glass formed when lava meets water in an instant. The Evil Eye symbol adds a second layer of protection against ill will, creating a complete shield.",
        "healing_props": "Balance and protection. Black Obsidian psychic shielding. Evil Eye protection. Cuts energetic cords. Free Selenite plate for crystal cleansing included.",
        "chakra": "Root",
        "zodiac": "Scorpio, Sagittarius",
        "origin": "India",
        "weight_grams": 42.0,
        "dimensions": "Standard size + Selenite plate",
        "price": 849.00,
        "compare_price": 1699.00,
        "stock_qty": 30,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Elegant Black Obsidian Evil Eye Bracelet With Free Raw Selenite Plate _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Elegant Garnet Anklet With Free Raw Selenite Plate",
        "slug": "elegant-garnet-anklet-with-free-raw-selenite-plate",
        "sku": "GF-ANK-GRS",
        "category_slug": "anklets",
        "description": "A deep red Garnet anklet with a complimentary raw Moroccan Selenite plate — grounding passion energy paired with lunar cleansing power in one beautiful set.",
        "story": "Garnet has been worn as jewellery for over five thousand years. Roman soldiers wore it for protection. Victorian ladies wore it for love. The Selenite plate keeps it continuously charged.",
        "healing_props": "Healing and clarity. Passion and vitality. Root chakra grounding. Protective energy. Free Selenite plate cleanses and recharges the anklet continuously.",
        "chakra": "Root",
        "zodiac": "Capricorn, Aquarius, Leo",
        "origin": "India",
        "weight_grams": 30.0,
        "dimensions": "Adjustable anklet + Selenite plate",
        "price": 999.00,
        "compare_price": 1999.00,
        "stock_qty": 25,
        "is_featured": True,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Elegant Garnet Anklet With Free Raw Selenite Plate _ Healing & Clarity/image1.png",
        ]
    },
    {
        "name": "Elegant Zodiac Bracelet Libra",
        "slug": "elegant-zodiac-bracelet-libra",
        "sku": "GF-BRC-LBR",
        "category_slug": "crystal-bracelets",
        "description": "A curated crystal bracelet for Libra — supporting the sign's natural gifts for harmony, balance, beauty and refined decision-making.",
        "story": "Libra is the sign of balance, beauty and justice. This bracelet honours all those qualities, supporting the Libran soul in its eternal quest for equilibrium and elegance.",
        "healing_props": "Personal alignment and strength. Amplifies Libra's natural harmony. Balanced decision-making. Beauty and grace. Heart and throat chakra activation.",
        "chakra": "Heart, Throat",
        "zodiac": "Libra",
        "origin": "India",
        "weight_grams": 38.0,
        "dimensions": "Standard size",
        "price": 799.00,
        "compare_price": 1599.00,
        "stock_qty": 30,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Elegant Zodiac Bracelet Libra _ Personal Alignment & Strength/image1.png",
        ]
    },
    {
        "name": "Exquisite 2026 Good Health Combo (Pack of 2)",
        "slug": "exquisite-2026-good-health-combo-pack-of-2",
        "sku": "GF-CMB-GH2",
        "category_slug": "crystal-designs",
        "description": "A specially curated 2026 Good Health combo — two items selected to support physical wellbeing, immunity and vitality as you enter the new year with renewed energy.",
        "story": "Health is the foundation of every other aspiration. This combo was curated with a single intention — to support your physical body and vitality throughout 2026 and beyond.",
        "healing_props": "Balance and protection. Physical health and immunity. Vitality and energy. New year wellness intention. Pack of 2 — ideal as a health gift for a loved one.",
        "chakra": "Heart, Solar Plexus",
        "zodiac": "All Signs",
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Pack of 2",
        "price": 999.00,
        "compare_price": 1999.00,
        "stock_qty": 20,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Exquisite 2026 Good Health Combo _ Balance & Protection (Pack Of 2 )/image1.png",
        ]
    },
    {
        "name": "Exquisite 7 Chakra Conical Pyramid",
        "slug": "exquisite-7-chakra-conical-pyramid",
        "sku": "GF-PYR-7CK",
        "category_slug": "crystal-designs",
        "description": "A 7 Chakra conical pyramid with all seven chakra crystal chips arranged in a spiral — combining the upward-spiralling energy of the conical form with complete chakra alignment.",
        "story": "The conical form creates a spiralling energy field, distributing balanced energy evenly throughout your space. Combined with all seven chakra crystals, this piece creates complete energetic harmony.",
        "healing_props": "Healing and clarity. Balances and aligns all seven chakras. Conical sacred geometry. Continuous energy circulation. Excellent for meditation rooms and living spaces.",
        "chakra": "All Chakras",
        "zodiac": "All Signs",
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Approx. 8-10 cm height",
        "price": 799.00,
        "compare_price": 1599.00,
        "stock_qty": 18,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Exquisite 7 Chakra Conical Pyramid _ Healing & Clarity/image1.png",
        ]
    },
    {
        "name": "Exquisite Black Obsidian Pyramid",
        "slug": "exquisite-black-obsidian-pyramid",
        "sku": "GF-PYR-BOB",
        "category_slug": "crystal-designs",
        "description": "A striking Black Obsidian pyramid — the most powerful protective crystal in pyramid form, creating a concentrated beam of protective energy for space clearing and psychic protection.",
        "story": "Black Obsidian is volcanic glass formed in fire. The pyramid focuses its formidable energy upward, creating a powerful beam that can cleanse an entire room of negative energy.",
        "healing_props": "Healing and clarity. Powerful psychic protection. Space clearing and purification. Cuts energetic cords. Reveals truth. Pyramid geometry amplifies Obsidian's power.",
        "chakra": "Root",
        "zodiac": "Scorpio, Sagittarius, Capricorn",
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Approx. 5-7 cm base",
        "price": 699.00,
        "compare_price": 1399.00,
        "stock_qty": 20,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Exquisite Black Obsidian Pyramid _ Healing & Clarity/image1.png",
        ]
    },
    {
        "name": "Exquisite Citrine Pyramid With Free Vyapar Vridhi Yantra 6x6 Inch Maha Lakshmi Siddhi",
        "slug": "exquisite-citrine-pyramid-vyapar-vridhi-yantra-6x6-maha-lakshmi-siddhi",
        "sku": "GF-YNT-CPV",
        "category_slug": "yantras-frames",
        "description": "A natural Citrine pyramid paired with a free Vyapar Vridhi Yantra (6x6 inch) — both Maha Lakshmi Siddhi energised. The ultimate combo for business owners seeking prosperity.",
        "story": "Citrine's solar abundance energy combined with the Vyapar Vridhi Yantra's geometric precision creates an unmatched business prosperity tool. Both Maha Lakshmi Siddhi energised.",
        "healing_props": "Balance and protection. Citrine abundance energy. Vyapar Vridhi business growth. Maha Lakshmi Siddhi blessings. Free 6x6 Yantra. Excellent for shops and offices.",
        "chakra": "Solar Plexus",
        "zodiac": None,
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Pyramid + free 6x6 inch Yantra",
        "price": 1110.00,
        "compare_price": 2229.00,
        "stock_qty": 12,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Exquisite Citrine Pyramid With Free Vyapppar Vridhi Yantra 6 6 Inch Maha Lakshmi Siddhi _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Handcrafted Ghar Samriddhi Combo (Pack of 2)",
        "slug": "handcrafted-ghar-samriddhi-combo-pack-of-2",
        "sku": "GF-CMB-GSC",
        "category_slug": "yantras-frames",
        "description": "The Ghar Samriddhi (Home Prosperity) combo — a pack of 2 sacred items energised to bring wealth, harmony and abundance into your home and family life.",
        "story": "Ghar Samriddhi means the prosperity of the entire household — not just financial wealth but harmony, health and happiness for every family member. The perfect housewarming gift.",
        "healing_props": "Wealth and success. Home prosperity and harmony. Family wellbeing. Abundance attraction. Vastu-friendly. Pack of 2 — ideal housewarming gift.",
        "chakra": "Solar Plexus, Heart",
        "zodiac": None,
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Pack of 2",
        "price": 1099.00,
        "compare_price": 2199.00,
        "stock_qty": 15,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Handcrafted Ghar Samriddhi Combo _ Wealth & Success (Pack Of 2 )/image1.png",
        ]
    },
    {
        "name": "Handcrafted Pyrite Anklet With Free Black Tourmaline Anklet With Evil Eye Charm Maha Lakshmi Siddhi (Pack of 2)",
        "slug": "handcrafted-pyrite-anklet-black-tourmaline-evil-eye-maha-lakshmi-siddhi-pack-2",
        "sku": "GF-ANK-PBT",
        "category_slug": "anklets",
        "description": "Pack of 2 — a Pyrite wealth anklet plus a free Black Tourmaline anklet with Evil Eye charm. Both Maha Lakshmi Siddhi energised for maximum abundance and protection.",
        "story": "Wealth and protection are the two most fundamental needs. This pack addresses both simultaneously — Pyrite for abundance and Black Tourmaline with Evil Eye for complete protection.",
        "healing_props": "Wealth and success. Pyrite wealth attraction. Black Tourmaline protection. Evil Eye shield. Maha Lakshmi Siddhi blessings. Pack of 2 anklets.",
        "chakra": "Root, Solar Plexus",
        "zodiac": None,
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Pack of 2 anklets",
        "price": 1299.00,
        "compare_price": 2599.00,
        "stock_qty": 15,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Handcrafted Pyrite Anklet With Free Black Tourmaline Anklet With Evil Eye Charm Maha Lakshmi Siddhi _ Wealth & Success (Pack Of 2 )/image1.png",
        ]
    },
    {
        "name": "Powerful Aquarius Zodiac Amethyst Lapis Lazuli Bracelet Poornima Energized",
        "slug": "powerful-aquarius-zodiac-amethyst-lapis-lazuli-bracelet-poornima-energized",
        "sku": "GF-BRC-AQL",
        "category_slug": "crystal-bracelets",
        "description": "A Poornima (full moon) energised bracelet combining Amethyst and Lapis Lazuli for the visionary Aquarius — supporting spiritual insight, truth and higher consciousness.",
        "story": "Amethyst and Lapis Lazuli together support Aquarius's visionary nature with clarity, intuition and the courage to speak truth to power. Poornima charging amplifies this energy.",
        "healing_props": "Personal alignment and strength. Aquarius intuition amplification. Amethyst spiritual clarity. Lapis Lazuli truth and wisdom. Poornima charged for enhanced manifestation.",
        "chakra": "Third Eye, Throat",
        "zodiac": "Aquarius",
        "origin": "India",
        "weight_grams": 40.0,
        "dimensions": "Standard size",
        "price": 910.00,
        "compare_price": 1829.00,
        "stock_qty": 20,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Powerful Aquarius Zodiac Amethyst Lapis Lazuli Bracelet Poornima Energized _ Personal Alignment & Strength/image1.png",
        ]
    },
    {
        "name": "Sacred Aries Courage Vitality Power Combo",
        "slug": "sacred-aries-courage-vitality-power-combo",
        "sku": "GF-CMB-ARS",
        "category_slug": "crystal-bracelets",
        "description": "A curated crystal power combo for Aries — combining stones that amplify the sign's natural courage, vitality and pioneering spirit for those born under the first sign of the zodiac.",
        "story": "Aries is the first sign — the pioneer, the warrior, the one who leads where others hesitate. This combo channels that innate Aries fire into unstoppable courage and vitality.",
        "healing_props": "Balance and protection. Aries courage and vitality. Pioneer energy and leadership. Physical strength and endurance. Root and sacral chakra activation.",
        "chakra": "Root, Sacral",
        "zodiac": "Aries",
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Combo set",
        "price": 1199.00,
        "compare_price": 2399.00,
        "stock_qty": 18,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Sacred Aries Courage Vitality Power Combo _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Sacred Divya Raksha Rudraksha Karungali Mala Silver Capped 108 Bead Meditation Necklace",
        "slug": "sacred-divya-raksha-rudraksha-karungali-mala-silver-capped-108-bead",
        "sku": "GF-RDR-DRK",
        "category_slug": "rudraksha",
        "description": "A 108-bead Divya Raksha (Divine Protection) meditation necklace combining Rudraksha and Karungali beads with silver capping — the ultimate daily wear and meditation mala.",
        "story": "108 is the most sacred number in Hinduism. This mala carries that cosmic significance in every rotation, combining Rudraksha, Karungali and silver for complete divine protection.",
        "healing_props": "Balance and protection. Complete divine protection. Rudraksha Lord Shiva blessings. Karungali sacred protection. Silver for purity. Traditional 108-bead meditation tool.",
        "chakra": "Crown, Root",
        "zodiac": None,
        "origin": "South India/Nepal",
        "weight_grams": None,
        "dimensions": "108 beads, standard mala",
        "price": 1299.00,
        "compare_price": 2599.00,
        "stock_qty": 12,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Sacred Divya Raksha Rudraksha Karungali Mala Silver Capped 108 Bead Meditation Necklace _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Sacred Garnet Anklet With Free Black Tourmaline Anklet With Evil Eye Charm",
        "slug": "sacred-garnet-anklet-free-black-tourmaline-anklet-evil-eye-charm",
        "sku": "GF-ANK-GBT",
        "category_slug": "anklets",
        "description": "Pack of 2 — a Garnet anklet for vitality and passion plus a free Black Tourmaline anklet with Evil Eye charm for complete protection. Walk through life energised and shielded.",
        "story": "This pack pairs Garnet's life-giving energy with Black Tourmaline's protective shield and the ancient Evil Eye charm — ensuring you walk both energised and fully protected.",
        "healing_props": "Balance and protection. Garnet vitality and passion. Black Tourmaline protection. Evil Eye shield. Pack of 2 — excellent value for complete crystal ankle care.",
        "chakra": "Root",
        "zodiac": None,
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Pack of 2 anklets",
        "price": 1099.00,
        "compare_price": 2199.00,
        "stock_qty": 20,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Sacred Garnet Anklet With Free Black Tourmaline Anklet With Evil Eye Charm _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Sacred Zodiac Bracelet Taurus",
        "slug": "sacred-zodiac-bracelet-taurus",
        "sku": "GF-BRC-TAU",
        "category_slug": "crystal-bracelets",
        "description": "A curated crystal bracelet for Taurus — featuring crystals that support the sign's natural gifts for sensuality, patience, determination and earthly abundance.",
        "story": "Taurus is the most grounded of all signs — deeply connected to the physical world, pleasure, beauty and the fruits of patient effort. This bracelet honours and amplifies all of those qualities.",
        "healing_props": "Personal alignment and strength. Taurus grounding and stability. Patience and determination. Sensuality and beauty. Earth energy and material abundance.",
        "chakra": "Root, Heart",
        "zodiac": "Taurus",
        "origin": "India",
        "weight_grams": 38.0,
        "dimensions": "Standard size",
        "price": 799.00,
        "compare_price": 1599.00,
        "stock_qty": 28,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Sacred Zodiac Bracelet Taurus _ Personal Alignment & Strength/image1.png",
        ]
    },
    {
        "name": "Timeless 5 Mukhi Rudraksha Mala 7mm 108+1 Beads",
        "slug": "timeless-5-mukhi-rudraksha-mala-7mm-108-1-beads",
        "sku": "GF-RDR-5M7",
        "category_slug": "rudraksha",
        "description": "A traditional 108+1 bead 5 Mukhi Rudraksha mala in 7mm bead size — the gold standard for daily Japa meditation and spiritual practice across India.",
        "story": "The 5 Mukhi mala has been used for japa meditation for thousands of years. The 7mm size is ideal — large enough to feel in the hands during practice, small enough for comfortable daily wear.",
        "healing_props": "Balance and protection. Peace and clarity of mind. Health and wellbeing. Meditation support. Traditional 108+1 japa count. Most universally beneficial Rudraksha.",
        "chakra": "Crown",
        "zodiac": "All Signs",
        "origin": "Nepal",
        "weight_grams": None,
        "dimensions": "7mm beads, 108+1 count",
        "price": 1499.00,
        "compare_price": 2999.00,
        "stock_qty": 25,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Timeless 5 Mukhi Rudraksha Mala 7Mm 108 1 Beads _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Timeless 9 Mukhi Rudraksha Bead In 5 Mukhi Rudraksha Mala",
        "slug": "timeless-9-mukhi-rudraksha-bead-in-5-mukhi-mala",
        "sku": "GF-RDR-009",
        "category_slug": "rudraksha",
        "description": "The 9 Mukhi Rudraksha ruled by Goddess Durga — one of the most powerful divine feminine energies for courage, transformation and protection. Set within a 5 Mukhi mala.",
        "story": "The 9 Mukhi represents Goddess Durga in her nine forms (Navadurga). It gives the wearer power to overcome all nine obstacles in life — a rare and auspicious bead for transformation.",
        "healing_props": "Balance and protection. Goddess Durga's fierce protection. Courage and transformation. Overcomes all obstacles. Activates dormant energies. Removes fear.",
        "chakra": "Crown, Sacral",
        "zodiac": None,
        "origin": "Nepal/India",
        "weight_grams": None,
        "dimensions": "Standard mala length",
        "price": 9999.00,
        "compare_price": 19999.00,
        "stock_qty": 8,
        "is_featured": False,
        "is_bestseller": False,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Timeless 9 Mukhi Rudraksha Bead In 5 Mukhi Rudraksha Mala _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Timeless Aquarius Pendant With Amethyst",
        "slug": "timeless-aquarius-pendant-with-amethyst",
        "sku": "GF-PND-AQA",
        "category_slug": "pendants-malas",
        "description": "An Aquarius zodiac pendant featuring natural Amethyst — the perfect crystal companion for the visionary, humanitarian and intellectually driven Aquarius personality.",
        "story": "Amethyst has been Aquarius's companion stone across traditions — its purple hue resonates with the sign's connection to higher consciousness, innovation and the space between the known and the unknown.",
        "healing_props": "Healing and clarity. Aquarius intuition and vision. Amethyst spiritual wisdom. Higher consciousness connection. Calm and clarity for the busy Aquarius mind.",
        "chakra": "Third Eye, Crown",
        "zodiac": "Aquarius",
        "origin": "India",
        "weight_grams": 15.0,
        "dimensions": "Pendant on cord",
        "price": 699.00,
        "compare_price": 1399.00,
        "stock_qty": 25,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Timeless Aquarius Pendant With Amethyst _ Healing & Clarity/image1.png",
        ]
    },
    {
        "name": "Timeless Mahadev Trishul Damru Rudraksha Karungali Kavach Bracelet",
        "slug": "timeless-mahadev-trishul-damru-rudraksha-karungali-kavach-bracelet",
        "sku": "GF-BRC-MTD",
        "category_slug": "crystal-bracelets",
        "description": "A Kavach (armour) bracelet combining Lord Mahadev's Trishul and Damru symbols with Rudraksha and Karungali beads — complete spiritual protection in a single wearable piece.",
        "story": "Lord Shiva's Trishul represents the three powers of creation, preservation and destruction. His Damru represents the cosmic rhythm. This bracelet carries both as a wearable divine armour.",
        "healing_props": "Balance and protection. Lord Mahadev's complete protection. Trishul and Damru divine symbols. Rudraksha energy. Karungali sacred protection. Spiritual energy shield.",
        "chakra": "Root, Crown",
        "zodiac": None,
        "origin": "South India",
        "weight_grams": 45.0,
        "dimensions": "Standard size",
        "price": 899.00,
        "compare_price": 1799.00,
        "stock_qty": 22,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Timeless Mahadev Trishul Damru Rudraksha Karungali Kavach Bracelet For Protection Spiritual Energy _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Timeless Original Karungali Rudraksha Mala Ebony Wood Sacred Bead Necklace",
        "slug": "timeless-original-karungali-rudraksha-mala-ebony-wood-sacred-bead",
        "sku": "GF-PND-KRM",
        "category_slug": "pendants-malas",
        "description": "A traditional 108-bead necklace combining Karungali (Ebony wood) and Rudraksha — two of the most revered spiritual materials in Indian tradition. Certified authentic.",
        "story": "Karungali is used in South Indian temples to craft sacred objects for deity worship. Rudraksha are the tears of Lord Shiva. Together they form one of the most powerful traditional malas.",
        "healing_props": "Balance and protection. Meditation support. Karungali sacred protection. Rudraksha Lord Shiva blessings. Traditional 108-bead japa count. Daily spiritual practice.",
        "chakra": "Crown, Root",
        "zodiac": None,
        "origin": "South India",
        "weight_grams": None,
        "dimensions": "108 beads, standard mala",
        "price": 899.00,
        "compare_price": 1799.00,
        "stock_qty": 22,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Timeless Original Karungali Rudraksha Mala Ebony Wood Sacred Bead Necklace For Meditation Protection _ Balance & Protection/image1.png",
        ]
    },
    {
        "name": "Timeless Rough Peru Pyrite Ring For Wealth Luck Protection",
        "slug": "timeless-rough-peru-pyrite-ring-wealth-luck-protection",
        "sku": "GF-RNG-PPR",
        "category_slug": "pendants-malas",
        "description": "A raw rough Pyrite ring from Peru — the world's finest Pyrite origin — for wealth, luck and protection. Each ring is unique in shape, carrying the unpolished power of natural Pyrite.",
        "story": "Peruvian Pyrite is renowned for its superior lustre and crystalline perfection. Wearing it as a ring keeps wealth energy in direct contact with your active hand — the hand that creates and receives.",
        "healing_props": "Wealth and success. Peruvian Pyrite wealth attraction. Luck and protection. Each piece unique. Active hand manifestation energy. Financial abundance and confidence.",
        "chakra": "Solar Plexus",
        "zodiac": "Leo, Aries, Scorpio",
        "origin": "Peru",
        "weight_grams": None,
        "dimensions": "Adjustable rough ring",
        "price": 699.00,
        "compare_price": 1399.00,
        "stock_qty": 30,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Timeless Rough Peru Pyrite Ring For Wealth Luck Protection _ Wealth & Success/image1.png",
        ]
    },
    {
        "name": "Timeless Selenite Tumble",
        "slug": "timeless-selenite-tumble",
        "sku": "GF-SEL-TBL",
        "category_slug": "selenite",
        "description": "A beautifully smooth Selenite tumble — liquid moonlight in your pocket. Perfect for personal energy cleansing, meditation and carrying divine lunar energy throughout your day.",
        "story": "Selenite never needs cleansing — it is continuously cleansing. Carry this tumble in your pocket and it silently purifies your energy field all day. Place on your bedside table for overnight aura cleansing.",
        "healing_props": "Healing and clarity. Continuous personal energy cleansing. Connects to higher consciousness. Mental clarity and calm. Promotes peaceful sleep. Never needs cleansing itself.",
        "chakra": "Crown, Third Eye",
        "zodiac": "Taurus, Cancer",
        "origin": "Morocco",
        "weight_grams": 20.0,
        "dimensions": "Approx. 3-4 cm",
        "price": 299.00,
        "compare_price": 599.00,
        "stock_qty": 50,
        "is_featured": False,
        "is_bestseller": True,
        "is_new_arrival": False,
        "images": [
            "/static/images/products/Timeless Selenite Tumble _ Healing & Clarity/image1.png",
        ]
    },
    {
        "name": "Timeless Super Women Combo",
        "slug": "timeless-super-women-combo",
        "sku": "GF-CMB-SWC",
        "category_slug": "crystal-designs",
        "description": "A specially curated combo celebrating the strength, grace and power of women — combining crystals and sacred items that honour feminine energy, intuition and inner power.",
        "story": "The Super Women Combo was born from a belief that every woman carries extraordinary power within her. This combo was curated to reflect, honour and amplify that power — for every role she plays.",
        "healing_props": "Wealth and success. Feminine power and grace. Intuition and inner strength. Self-love and confidence. Emotional resilience. A meaningful gift for any woman.",
        "chakra": "Heart, Sacral, Crown",
        "zodiac": "All Signs",
        "origin": "India",
        "weight_grams": None,
        "dimensions": "Combo set",
        "price": 1199.00,
        "compare_price": 2399.00,
        "stock_qty": 15,
        "is_featured": True,
        "is_bestseller": True,
        "is_new_arrival": True,
        "images": [
            "/static/images/products/Timeless Super Women Combo _ Wealth & Success/image1.png",
        ]
    },
]

for pd in products_data:
    existing = db.query(Product).filter(Product.slug == pd["slug"]).first()
    if not existing:
        images       = pd.pop("images", [])
        category_slug = pd.pop("category_slug")
        cat_id        = cat_map.get(category_slug)
        if not cat_id:
            print(f"  ⚠ Category '{category_slug}' not found — skipping {pd['sku']}")
            continue

        product = Product(category_id=cat_id, **pd)
        db.add(product)
        db.flush()

        # images[0]   → is_primary=True  (card listing image)
        # images[1..] → is_primary=False (product gallery thumbnails)
        for i, url in enumerate(images):
            db.add(ProductImage(
                product_id=product.id,
                url=url,
                is_primary=(i == 0),
                sort_order=i,
                alt_text=f"{product.name} — photo {i + 1}"
            ))
        print(f"  ✓ Product [{pd['sku']}] : {product.name[:55]}")

db.commit()
db.close()

print("\n✅ Database seeded successfully!")

