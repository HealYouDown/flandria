SKILLS = {
    "noble": {
        "cp002300": { # Fireball
            "max_level": 14,
            "relies_on": None,
        },
        "ck500000": { # Fishing
            "max_level": 5,
            "relies_on": None,
        },
        "cp008700": { # Sword of Spirit
            "max_level": 15,
            "relies_on": None,
        },
        "cp006800": { # Mind Up
            "max_level": 10,
            "relies_on": None,
        },
        "cp010200": { # Iceball
            "max_level": 15,
            "relies_on": ["cp002300"], # Fireball
        },
        "cp002400": { # Ice Shield
            "max_level": 11,
            "relies_on": ["cp010200"], # Iceball
        },
        "cp006200": { # Ice Bomb
            "max_level": 11,
            "relies_on": ["cp002400"], # Ice Shield
        },
        "cp008300": { # Ice Thorn
            "max_level": 7,
            "relies_on": ["cp006200"], # Ice Bomb
        },
        "cp006000": { # Lightning Shock
            "max_level": 12,
            "relies_on": ["cp002300"], # Fireball
        },
        "cp002600": { # Heavy Lightning
            "max_level": 10,
            "relies_on": ["cp006000"], # Lightning Shock
        },
        "cp006100": { # Fire Pole
            "max_level": 10,
            "relies_on": ["cp002300"], # Fireball
        },
        "cp008200": { # Wrath of Earth
            "max_level": 6,
            "relies_on": ["cp006100"], # Fire Pole
        },
        "cp002900": { # Warp
            "max_level": 3,
            "relies_on": None,
        },
        "cp006400": { # Teleport
            "max_level": 3,
            "relies_on": ["cp002900"], # Warp
        },
        "cp002500": { # Phantom Grief
            "max_level": 14,
            "relies_on": ["cp008700"], # Sword of Spirit
        },
        "cp006300": { # Phantom Pain
            "max_level": 11,
            "relies_on": ["cp002500"], # Phantom Grief
        },
        "cp008800": { # Vampiric Touch
            "max_level": 6,
            "relies_on": ["cp006300"], # Phantom Pain
        },
        "cp008900": { # Blessing of Mana
            "max_level": 7,
            "relies_on": ["cp008800"], # Vampiric Touch
        },
        "cp006700": { # Shade of Fear
            "max_level": 3,
            "relies_on": None,
        },
        "cp002800": { # Lure of Incubus
            "max_level": 5,
            "relies_on": ["cp006700"], # Shade of Fear
        },
        "cp006600": { # Temptation
            "max_level": 3,
            "relies_on": ["cp006300", "cp002800"], # Phantom Pain, Lure of Incubus
        },
        "cp009100": { # Royal Slave
            "max_level": 6,
            "relies_on": ["cp006600"], # Temptation
        },
        "cp007000": { # Insight of Magic
            "max_level": 8,
            "relies_on": ["cp006800"], # Mind Up
        }, 
        "cp002700": { # Magic Boost
            "max_level": 10,
            "relies_on": ["cp007000"], # Insight of Magic
        },
        "cp003000": { # Magic Power
            "max_level": 11,
            "relies_on": ["cp002700"], # Magic Boost
        },
        "cp006500": { # Recharge 
            "max_level": 4,
            "relies_on": ["cp003000"], # Magic Power
        },
        "cp006900": { # Mental Concentration
            "max_level": 9,
            "relies_on": ["cp006500"], # Recharge
        },
        "cp008400": { # Protection of Mana
            "max_level": 6,
            "relies_on": ["cp006900"], # Mental Concentration
        },
        "cp008600": { # Quick Spell
            "max_level": 4,
            "relies_on": ["cp008400"], # Protection of Mana
        }, 
        "cp008500": { # Balance Up
            "max_level": 4,
            "relies_on": None,
        },
    },
    "explorer": {
        "ck500000": { #fishing
            "max_level": 5,
            "relies_on": None,
        },
        "ck000700": { #Down Strike
            "max_level": 12,
            "relies_on": None,
        },
        "ck005200": { #Spiral Breaker
            "max_level": 10,
            "relies_on": ["ck000700"], #Down Strike
        },
        "ck008700": { #Balance Up
            "max_level": 4,
            "relies_on": None,
        },
        "ck009000": { #Aimed Shot
            "max_level": 15,
            "relies_on": ["ck000800"], #Quick Shot
        },
        "ck005800": { #Rifle Mastery
            "max_level": 11,
            "relies_on": ["ck009000"], #Aimed Shot
        },
        "ck009100": { #Poison Bullet Shot
            "max_level": 12,
            "relies_on": ["ck005800"], #Rifle Mastery    
        },
        "ck005300": { #Sniping
            "max_level": 11,
            "relies_on": ["ck009100"], #Poison Bullet Shot    
        },
        "ck008500": { #Pierce Shot
            "max_level": 6,
            "relies_on": ["ck005300"], #Sniping    
        },
        "ck000800": { #Quick Shot
            "max_level": 13,
            "relies_on": None,    
        },
        "ck001000": { #Burst Shot
            "max_level": 11,
            "relies_on": ["ck009000"], #Aimed Shot    
        },
        "ck000900": { #Shooting Nova
            "max_level": 10,
            "relies_on": ["ck005800"], #Rifle Mastery    
        },
        "ck008400": { #Frame Splash
            "max_level": 7,
            "relies_on": ["ck000900"], #Shooting Nova    
        },
        "ck008800": { #Net Launch
            "max_level": 7,
            "relies_on": None,    
        },
        "ck005900": { #Dual Gun Mastery
            "max_level": 5,
            "relies_on": ["ck000800"], #Quick Shot    
        },
        "ck005400": { #Gunkata
            "max_level": 11,
            "relies_on": ["ck005900"], #Dual Gun Mastery    
        },
        "ck001100": { #Moving Shot
            "max_level": 12,
            "relies_on": ["ck005400"], #Gunkata    
        },
        "ck001200": { #Assault Vermillion
            "max_level": 10,
            "relies_on": ["ck001100"], #Moving Shot    
        },
        "ck009200": { #Gas Bomb
            "max_level": 12,
            "relies_on": None,    
        },
        "ck008000": { #Explosion
            "max_level": 6,
            "relies_on": ["ck009200"], #Gas Bomb    
        },
        "ck008300": { #Crimson Dust
            "max_level": 6,
            "relies_on": ["ck008000"], #Explosion    
        },
        "ck007900": { #Mine Trap
            "max_level": 7,
            "relies_on": ["ck008300"], #Crimson Dust    
        },
        "ck001500": { #Eagle Eye
            "max_level": 11,
            "relies_on": None,    
        },
        "ck001300": { #Hit Chain
            "max_level": 10,
            "relies_on": None,    
        },
        "ck005700": { #Raise Agility
            "max_level": 10,
            "relies_on": ["ck001300"], #Hit Chain    
        },
        "ck005500": { #Calm
            "max_level": 3,
            "relies_on": ["ck005700"], #Raise Agility    
        },
        "ck008100": { #Wind Walk
            "max_level": 5,
            "relies_on": ["ck005500"], #Calm    
        },
        "ck005600": { #Wings Of Wind
            "max_level": 3,
            "relies_on": ["ck001300"], #Hit Chain    
        },
        "ck008600": { #Aerial Wing
            "max_level": 7,
            "relies_on": ["ck005500"], #Calm
        },
    },
    "mercenary": {
        "ck500000": { #fishing
            "max_level": 5,
            "relies_on": None,
        },
        "ck004600": { #Shield Mastery
            "max_level": 15,
            "relies_on": ["ck000100"], #Cross Edge
        },
        "ck000400": { #Shield Bash
            "max_level": 11,
            "relies_on": ["ck004600"], #Shield Mastery
        },
        "ck008900": { #Absolute Defense
            "max_level": 6,
            "relies_on": ["ck000400"], #Shield Bash
        },
        "ck000100": { #Cross Edge
            "max_level": 12,
            "relies_on": ["ck003900"], #Spiral Slash
        },
        "ck004700": { #Sword Mastery
            "max_level": 11,
            "relies_on": ["ck000100"] ,#Cross Edge
        },
        "ck004200": { #Smash Quake
            "max_level": 10,
            "relies_on": ["ck004700"], #Sword Mastery
        },
        "ck004400": { #Storm Edge
            "max_level": 9,
            "relies_on": ["ck004200"], #Smash Quake
        },
        "ck007000": { #Sacrifice Of Blood
            "max_level": 7,
            "relies_on": ["ck004400"], #Storm Edge
        },
        "ck003900": { #Spiral Slash
            "max_level": 15,
            "relies_on": None,
        },
        "ck000000": { #Breaker
            "max_level": 12,
            "relies_on": ["ck003900"], #Spiral Slash
        },
        "ck004000": { #Upper Slash
            "max_level": 12,
            "relies_on": ["ck000000"], #Breaker
        },
        "ck004300": { #Gale Smash
            "max_level": 9,
            "relies_on": None,
        },
        "ck004500": { #Berseker
            "max_level": 10,
            "relies_on": ["ck004300", "ck000500"], #Gale Smash, Tornado Slash
        },
        "ck007600": { #Lightning Recall
            "max_level": 6,
            "relies_on": ["ck004500"], #Berserker
        },
        "ck007400": { #Deathblow Training
            "max_level": 6,
            "relies_on": ["ck007600"], #Lightning Recall
        },
        "ck004100": { #Deep Slash
            "max_level": 15,
            "relies_on": ["ck003900"], #Spiral Slash
        },
        "ck004800": { #Two Hand Sword Mastery
            "max_level": 15,
            "relies_on": ["ck004100"], #Deep Slash
        },
        "ck000500": { #Tornado Slash
            "max_level": 10,
            "relies_on": ["ck004800"], #Two Hand Sword Mastery
        },
        "ck007100": { #Blood Fury
            "max_level": 7,
            "relies_on": None,
        },
        "ck004900": { #Stone Skin
            "max_level": 15,
            "relies_on": None,
        },
        "ck005100": { #Composure
            "max_level":9,
            "relies_on": ["ck004900"], #Stone Skin
        },
        "ck000300": { #Provocation
            "max_level": 10,
            "relies_on": ["ck005100"], #Composure
        },
        "ck005000": { #Aggression
            "max_level": 4,
            "relies_on": ["ck000300"], #Provocation
        },
        "ck007500": { #Cry Of Courage
            "max_level": 3,
            "relies_on": ["ck005000"], #Aggression
        },
        "ck007800": { #Impact Energy
            "max_level": 4,
            "relies_on": None,
        },
        "ck000200": { #Berserk
            "max_level": 12,
            "relies_on": ["ck004900"], #Stone Skin
        },
        "ck000600": { #Heart Of Steel
            "max_level": 9,
            "relies_on": ["ck000200"], #Berserk
        },
        "ck007700": { #Balance Up
            "max_level": 5,
            "relies_on": None,
        },
        "ck007200": { #Blood Thirst
            "max_level": 5,
            "relies_on": ["ck005000"], #Aggreesion
        },
    },
    "saint": {
        "cp003500": { #Light Transition
            "max_level": 13,
            "relies_on": None,
        },
        "cp007700": { #Armor Of Light
            "max_level": 7,
            "relies_on": ["cp003500"], #Light Transition
        },
        "cp007600": { #Chain Of Light
            "max_level": 5,
            "relies_on": ["cp007700"], #Armor Of Light
        },
        "cp009600": { #Training Of Mental Power
            "max_level": 5,
            "relies_on": None,
        },
        "cp003100": { #Healing Hands
            "max_level": 12,
            "relies_on": None,
        },
        "cp008000": { #Instant Recovery
            "max_level": 12,
            "relies_on": ["cp003100"], #Healing Hands
        },
        "cp003200": { #Recovery
            "max_level": 12,
            "relies_on": ["cp008000"], #Instant Recovery
        },
        "cp007100": { #Master Recovery
            "max_level": 12,
            "relies_on": ["cp003200"], #Recovery
        },
        "cp009300": { #Blessing Of Life
            "max_level": 7,
            "relies_on": ["cp007100"], #Master Recovery
        },
        "cp009200": { #Aurora Of Life
            "max_level": 7,
            "relies_on": ["cp009300"], #Blessing Of Life
        },
        "cp007800": { #Breathing Of Earth
            "max_level": 10,
            "relies_on": ["cp009200"], #Aurora Of Life
        },
        "cp003800": { #Spiritual Power
            "max_level": 10,
            "relies_on": ["cp003100"], #Healing Hands
        },
        "cp003400": { #Soul Rivival
            "max_level": 3,
            "relies_on": ["cp003800"], #Spiritual Power
        },
        "cp003600": { #Blessing Of Nature
            "max_level": 11,
            "relies_on": ["cp003400"], #Soul Revival
        },
        "cp009400": { #Prayer
            "max_level": 5,
            "relies_on": ["cp003600"], #Blessing Of Nature
        },
        "cp007200": { #Flow Of Darkness
            "max_level": 12,
            "relies_on": None,
        },
        "cp007900": { #Thorn Shield
            "max_level": 9,
            "relies_on": ["cp007200"], #Flow Of Darkness
        },
        "cp003300": { #Thorn Trunk
            "max_level": 5,
            "relies_on": ["cp007900"], #Thorn Shield
        },
        "cp009500": { #Balance Up
            "max_level": 4,
            "relies_on": None,
        },
        "cp003700": { #Curse Of Leaf
            "max_level": 13,
            "relies_on": ["cp007200"], #Flow Of Darkness
        },
        "cp007300": { #Mist Of Darkness
            "max_level": 10,
            "relies_on": ["cp003700"], #Curse Of Leaf
        },
        "cp007400": { #Darkness Wave
            "max_level": 9,
            "relies_on": ["cp007300"], #Mist Of Darkness
        },
        "cp009800": { #Revenants Curse
            "max_level": 7,
            "relies_on": ["cp007400"], #Darkness Wave
        },
        "cp009700": { #Sudden Darkness
            "max_level": 7,
            "relies_on": ["cp009800"], #Revenants Curse
        },
        "cp010100": { #Touch Of Death
            "max_level": 5,
            "relies_on": ["cp009700"], #Sudden Darkness
        },
        "ck500000": { #Fishing
            "max_level": 5,
            "relies_on": None,
        },
        "cp010300": { #Cure
            "max_level": 1,
            "relies_on": None,
        },
        "cp008100": { #Depravity OPf Soul
            "max_level": 10,
            "relies_on": ["cp007300"], #Mist Of Darkness
        },
        "cp007500": { #Door Of Darkness
            "max_level": 9,
            "relies_on": ["cp008100"], #Deptravity Of Soul
        },
        "cp009900": { #Deceitful Penalty
            "max_level": 7,
            "relies_on": ["cp007500"], #Door Of Darkness
        },
    },

"ship": {
        "sksinso00": { #Quick Cannonace
            "max_level": 8,
            "relies_on": None,
        },
        "skpogye00": { #Cannonade Mastery
            "max_level": 5,
            "relies_on": ["sksinso00"],
        },
        "skjojun00": { #Order of Aiming Shot
            "max_level": 5,
            "relies_on": ["skpogye00"], #Cannonade Mastery
        },
        "skwehyu00": { #Threatening Cannonade
            "max_level": 7,
            "relies_on": ["skjojun00"], #Order of Aiming Shot
        },
        "skpokba00": { #Charge Explosive Shot
            "max_level": 5,
            "relies_on": ["skwehyu00"], #Threatening Cannonade
        },
        "skchain00": { #Chain
            "max_level": 3,
            "relies_on": ["skpokba00"], #Charge Explosive Shot
        },
        "skadomi00": { #Area Domination
            "max_level": 3,
            "relies_on": ["skchain00"], #Chain
        },
        "skhwaks00": { #Order of Diffuse Shooting
            "max_level": 5,
            "relies_on": ["skpogye00"], #Cannonade Mastery
        },
        "skstst000": { #Charge Stop Shot
            "max_level": 5,
            "relies_on": ["skhwaks00"], #Order of Diffuse Shooting
        },
        "skgwant00": { #Charge Piercing Shot
            "max_level": 5,
            "relies_on": ["skstst000"], #Charge Stop Shot
        },
        "skrange00": { #Range Up
            "max_level": 3,
            "relies_on": ["skgwant00"], #Charge Piercing Shot
        },
        "skunpro00": { #Unbeatable Protect
            "max_level": 3,
            "relies_on": ["skrange00"], #Range Up
        },
        "skgyeon00": { #Checked Shooting
            "max_level": 5,
            "relies_on": None,
        },
        "skjilju00": { #Order of Speeding
            "max_level": 3,
            "relies_on": ["skgyeon00"], #Checked Shooting
        },
        "skwinds00": { #Charge Wind Shot
            "max_level": 3,
            "relies_on": ["skjilju00"], #Order of Speeding
        },
        "skpagoe00": { #Charge Destructive Shot
            "max_level": 5,
            "relies_on": ["skwinds00"], #Charge Wind Shot
        },
        "skransh00": { #Randomly Shooting
            "max_level": 3,
            "relies_on": ["skpagoe00"], #Charge Destructive Shot
        },
        "skadest00": { #Area Destroy
            "max_level": 3,
            "relies_on": ["skransh00"], #Randomly Shooting
        },
        "skyeonb00": { #Repeated Shooting
            "max_level": 8,
            "relies_on": None,
        },
        "skgeunj00": { #Shooting Mastery
            "max_level": 5,
            "relies_on": ["skyeonb00"], #Repeated Shooting
        },
        "skangae00": { #Fog of Darkness
            "max_level": 5,
            "relies_on": None,
        },
        "skhide000": { #Hide
            "max_level": 3,
            "relies_on": ["skangae00"], #Fog of Darkness
        },
        "skdarks00": { #Charge Darkness Shot
            "max_level": 3,
            "relies_on": ["skangae00"], #Hide
        },
        "skchung00": { #Charge Impact Shot
            "max_level": 5,
            "relies_on": ["skdarks00"], #Charge Darkness Shot
        },
        "skload000": { #Reload Mastery
            "max_level": 5,
            "relies_on": ["skchung00"], #Charge Impact Shot
        },
        "skflash00": { #Charge Flash Bang
            "max_level": 3,
            "relies_on": ["skload000"], #Reload Mastery
        },
        "skavoid00": { #Auto Avoid
            "max_level": 3,
            "relies_on": None,
        },
        "skjaesa00": { #Charge Recovery Shot
            "max_level": 5,
            "relies_on": ["skavoid00"], #Auto Avoid
        },
        "skhambo00": { #Ship Recovery
            "max_level": 5,
            "relies_on": ["skjaesa00"], #Charge Recovery Shot
        },
        "sksiles00": { #Charge Silence Shot
            "max_level": 3,
            "relies_on": ["skhambo00"], #Ship Recovery
        },
        "skchiyu00": { #Song of Recovery
            "max_level": 5,
            "relies_on": ["sksiles00"], #Charge Silence Shot
        },
        "skshipr00": { #Ship Revival
            "max_level": 3,
            "relies_on": ["skchiyu00"], #Song of Recovery
        },
        "skchund00": { #Collision Mastery
            "max_level": 5,
            "relies_on": None,
        },
        "skendur00": { #Endure
            "max_level": 3,
            "relies_on": ["skchund00"], #Collision Mastery
        },
        "sksick000": { #Charge Sickness Shot
            "max_level": 3,
            "relies_on": ["skendur00"], #Endure
        },
        "skspecs00": { #Charge Spectre Shot
            "max_level": 5,
            "relies_on": ["sksick000"], #Charge Sickness Shot
        },
        "skturn000": { #Turning Power Mastery
            "max_level": 3,
            "relies_on": None,
        },
        "skyuck000": { #Headwind Resist
            "max_level": 3,
            "relies_on": ["skturn000"], #Turning Power Mastery
        },
        "skjunja00": { #Song of War
            "max_level": 5,
            "relies_on": ["skyuck000"], #Headwind Resist
        },
        "skgyeol00": { #Song of Union
            "max_level": 5,
            "relies_on": ["skjunja00"], #Song of War
        },
        "skjunso00": { #Crazy Speeding
            "max_level": 5,
            "relies_on": ["skgyeol00"], #Song of Union
        },
        "skshotm00": { #Shot Speed Mastery
            "max_level": 3,
            "relies_on": ["skjunso00"], #Crazy Speeding
        },
        "skdouca00": { #Double Cannon
            "max_level": 3,
            "relies_on": ["skshotm00"], #Shot Speed Mastery
        },
        "sklimit00": { #Limit
            "max_level": 2,
            "relies_on": ["skdouca00"], #Double Cannon
        },
    },
}
