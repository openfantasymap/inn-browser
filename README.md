# 🏰 Fantasy Inn Tycoon

Un gioco gestionale/incrementale per browser dove gestisci una locanda in un mondo fantasy! Costruisci stanze, accogli ospiti, servi cibo e bevande, guadagna oro e migliora la tua locanda.

> **💡 Nota Backend**: Il progetto include due backend:
> - **`backend_django/`** ✨ - Backend attivo con Django, ORM, Admin interface e database persistente
> - **`backend/`** 📦 - Backend legacy FastAPI (mantenuto per riferimento)

## 🎮 Caratteristiche del Gioco

### Meccaniche di Gioco
- **Gestione Stanze**: Costruisci e gestisci diverse tipologie di stanze (Basic, Standard, Deluxe, Royal)
- **Sistema Ospiti**: Accogli 15 tipi diversi di ospiti con caratteristiche uniche
- **🍺 Taverna**: Sblocca la taverna per servire cibo e bevande agli ospiti
- **🎨 Crafting**: Crea 13 diversi piatti e bevande (5 livelli di qualità)
- **🌟 Ingredienti**: Raccogli 17 ingredienti rari dagli ospiti soddisfatti
- **Risorse**: Gestisci oro e reputazione per espandere la tua locanda
- **Upgrade**: Sblocca miglioramenti per aumentare i guadagni e automatizzare la gestione
- **Meccanica Incrementale**: Il gioco progredisce automaticamente con tick periodici
- **Pulizia Stanze**: Mantieni le stanze pulite per mantenere gli ospiti felici
- **Sistema Soddisfazione**: Gli ospiti felici lasciano ingredienti preziosi!

### Tipologie di Stanze
- 🛏️ **Basic**: Stanza base (50 oro, 1x guadagno)
- 🏠 **Standard**: Stanza standard (200 oro, 2x guadagno)
- 🏰 **Deluxe**: Stanza di lusso (500 oro, 4x guadagno)
- 👑 **Royal**: Stanza reale (1000 oro, 8x guadagno)

### Tipi di Ospiti (15 Tipi!)
- 🧑‍🌾 **Peasant**: Basso pagamento, bassa reputazione
- 💼 **Merchant**: Pagamento medio, reputazione media, **lascia ingredienti 2x più spesso!**
- 👔 **Noble**: Alto pagamento, alta reputazione
- ⚔️ **Adventurer**: Buon pagamento, buona reputazione
- 🧙 **Wizard**: Ottimo pagamento, ottima reputazione
- 🏴‍☠️ **Bandit**: Alto guadagno, bassa reputazione
- 🙏 **Monk**: Basso guadagno, altissima reputazione
- 🎵 **Bard**: Medio guadagno, alta reputazione
- 🐉 **Dragon (Disguised)**: Altissimo guadagno, reputazione casuale, **drop ingredienti leggendari 3x!**
- 🤲 **Beggar**: Bassissimo guadagno, media reputazione
- 👑 **Prince**: Altissimo guadagno, altissima reputazione
- 🗡️ **Thief**: Alto guadagno, reputazione negativa
- 📚 **Scholar**: Basso guadagno, alta reputazione
- 🍺 **Drunk**: Medio guadagno, bassa reputazione
- 👻 **Ghost**: Nessun guadagno, alta reputazione (speciale)

### Sistema Taverna

#### Cibi (6 piatti)
- 🍞 **Bread** (Basic) - Semplice ma nutriente
- 🥘 **Vegetable Stew** (Basic) - Caldo e sostanzioso
- 🍗 **Roasted Chicken** (Good) - Delizioso pollo arrosto
- 🥧 **Meat Pie** (Good) - Ricca torta salata
- 🍖 **Royal Feast** (Fine) - Banchetto regale
- 🐉 **Dragon Steak** (Exquisite) - Carne di drago leggendaria!

#### Bevande (8 drink)
- 💧 **Water** (Basic) - Acqua fresca dal pozzo
- 🍺 **Ale** (Basic) - Birra comune, amata dagli avventurieri
- 🍯 **Honey Mead** (Good) - Idromele dolce
- 🍷 **Fine Wine** (Good) - Vino di qualità
- 🧝 **Elven Wine** (Fine) - Vino mistico elfico
- 🍺 **Dwarven Ale** (Exquisite) - Birra leggendaria nanica
- ✨ **Divine Ambrosia** (Legendary) - La bevanda degli dei!

#### Ingredienti (17 tipi, 5 rarità)
- **Common**: Flour, Fresh Water, Salt, Herbs
- **Uncommon**: Fresh Meat, Wild Honey, Grapes, Exotic Spices
- **Rare**: Truffle, Elven Herbs, Aged Wine Base
- **Epic**: Phoenix Feather, Dragon Blood, Moonflower
- **Legendary**: Ambrosia Essence, Time Crystal

## 🛠️ Stack Tecnologico

### Frontend
- **Angular 17** - Framework frontend con standalone components
- **TypeScript** - Linguaggio di programmazione
- **RxJS** - Programmazione reattiva

### Backend
- **Django 4.2** - Framework web Python con ORM
- **Django REST Framework** - API REST
- **SQLite** - Database (facilmente aggiornabile a PostgreSQL)
- **Django Admin** - Interfaccia admin integrata con visualizzazioni personalizzate

## 📋 Prerequisiti

- **Node.js** (versione 18 o superiore)
- **npm** o **yarn**
- **Python** (versione 3.11 o superiore)
- **pip** (gestore pacchetti Python)

## 🚀 Installazione

### 1. Backend Django Setup

```bash
# Naviga nella directory backend Django
cd backend_django

# Crea un ambiente virtuale Python (opzionale ma consigliato)
python -m venv venv

# Attiva l'ambiente virtuale
# Su Linux/Mac:
source venv/bin/activate
# Su Windows:
venv\Scripts\activate

# Installa le dipendenze
pip install -r requirements.txt

# Applica le migrazioni del database
python manage.py migrate

# Inizializza i dati di gioco (tavern items e ingredienti)
python manage.py init_game_data

# Crea un superuser per l'admin (opzionale)
python manage.py createsuperuser

# Avvia il server Django
python manage.py runserver 8001
```

Il server backend sarà disponibile su `http://localhost:8001`
- **API Base**: `http://localhost:8001/api/`
- **Django Admin**: `http://localhost:8001/admin/` (username: admin, password: admin se non hai creato un nuovo superuser)
- **Health Check**: `http://localhost:8001/api/health/`

### Interfaccia Admin Django 🎨

L'admin Django include visualizzazioni ricche:
- 💰 Visualizzazione oro e risorse con colori
- 😊 Indicatori di soddisfazione ospiti
- 🍖 Status cibo/bevande servite
- ✨ Livelli di pulizia stanze
- 📊 Filtri e ricerca avanzata

### 2. Frontend Setup

```bash
# Naviga nella directory frontend
cd frontend

# Installa le dipendenze
npm install

# Avvia il server di sviluppo Angular
npm start
```

Il frontend sarà disponibile su `http://localhost:4200`

## 🎯 Come Giocare

### Obiettivi
1. **Guadagna Oro**: Gli ospiti nelle stanze generano reddito passivo
2. **Costruisci Stanze**: Espandi la tua locanda con stanze migliori
3. **Sblocca la Taverna**: Acquista l'upgrade "Build Tavern" (150 oro)
4. **Servi Cibo e Bevande**: Aumenta soddisfazione e guadagni degli ospiti
5. **Raccogli Ingredienti**: Gli ospiti molto soddisfatti (80%+) lasciano ingredienti
6. **Sblocca Upgrade**: Acquista miglioramenti per aumentare i guadagni
7. **Mantieni la Reputazione**: Tieni gli ospiti felici per bonus reputazione

### Gameplay Base
1. **Spawn Automatico**: Gli ospiti arrivano automaticamente (20% chance per tick)
2. **Assegnazione Automatica**: Gli ospiti vengono assegnati automaticamente a stanze vuote
3. **Pulizia**: Le stanze si sporcano nel tempo. Puliscile manualmente o acquista "Hire Cleaning Staff"
4. **Pazienza**: Gli ospiti hanno pazienza che diminuisce se la stanza è sporca (<50%)
5. **Guadagni**: Ogni tick genera oro in base a: tipo ospite × stanza × moltiplicatori
6. **Partenza**: Gli ospiti partono dopo il loro stay_duration o se la pazienza arriva a 0

### Sistema Taverna 🍺
1. **Sblocca Taverna**: Acquista upgrade "Build Tavern" (150 oro)
2. **Sblocca Ricette**: Le ricette Basic sono gratis, quelle migliori costano oro
3. **Crafta Items**: Spendi oro per creare cibo/bevande (es. Bread = 2 oro)
4. **Servi Ospiti**: Dai cibo/bevande agli ospiti per bonus:
   - ⬆️ **Pazienza**: Evita che se ne vadano
   - ⬆️ **Soddisfazione**: Aumenta fino a 100%
   - 💰 **Oro per tick**: Bonus permanente finché rimangono
   - ⭐ **Reputazione**: Bonus reputazione
5. **Raccogli Ingredienti**: Ospiti con 80%+ soddisfazione lasciano ingredienti quando partono
   - 💼 **Mercanti**: 2x drop chance!
   - 👔 **Nobili/Maghi/Principi**: 1.5x per ingredienti rari
   - 🐉 **Draghi**: 3x per ingredienti epici/leggendari!

### Strategia Avanzata
- **Early Game**: Costruisci stanze Basic, sblocca taverna velocemente
- **Mid Game**: Servi Bread/Ale agli Adventurers per massimizzare guadagni
- **Late Game**: Cerca Merchants e Dragons per ingredienti rari
- **Soddisfazione**: Mantieni 80%+ satisfaction per drop ingredienti
- **Priorità Upgrade**:
  1. Build Tavern (150 oro)
  2. Auto Clean (300 oro)
  3. Better Beds (200 oro)
  4. Expand capacity e stanze migliori

## 🏗️ Struttura del Progetto

```
inn-browser/
├── backend_django/                 # ✨ Backend Django
│   ├── game_api/
│   │   ├── models.py              # Django ORM models (7 modelli)
│   │   ├── admin.py               # Admin interface con visualizzazioni
│   │   ├── game_service.py        # Logica di business
│   │   ├── serializers.py         # DRF serializers
│   │   ├── views.py               # API endpoints
│   │   ├── urls.py                # URL routing
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── init_game_data.py  # Comando inizializzazione
│   │   └── migrations/
│   │       └── 0001_initial.py    # Database schema
│   ├── inn_project/
│   │   ├── settings.py            # Django settings (CORS, DRF)
│   │   └── urls.py                # URL principale
│   ├── manage.py                  # Django management
│   ├── requirements.txt           # Dipendenze Python
│   └── db.sqlite3                 # Database SQLite (generato)
├── backend/                       # 📦 Backend FastAPI (legacy)
│   ├── app/
│   │   ├── models/
│   │   │   └── game_models.py     # Modelli Pydantic
│   │   ├── routes/
│   │   │   └── game_routes.py     # Endpoint API
│   │   └── services/
│   │       └── game_service.py    # Logica di business
│   ├── main.py                    # Entry point FastAPI
│   └── requirements.txt           # Dipendenze Python
├── frontend/                      # 🎨 Frontend Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── models/
│   │   │   │   └── game.models.ts  # Interfacce TypeScript
│   │   │   ├── services/
│   │   │   │   └── game.service.ts # Servizio API
│   │   │   ├── app.component.ts    # Componente principale
│   │   │   ├── app.component.html  # Template
│   │   │   └── app.component.css   # Stili
│   │   ├── index.html              # HTML principale
│   │   ├── main.ts                 # Entry point Angular
│   │   └── styles.css              # Stili globali
│   ├── angular.json                # Configurazione Angular
│   ├── package.json                # Dipendenze npm
│   └── tsconfig.json               # Configurazione TypeScript
└── README.md
```

## 🔌 API Endpoints (Django REST Framework)

### Sistema Base
- **GET** `/api/health/` - Health check
- **GET/POST** `/api/game/{player_id}` - Ottiene/crea stato gioco
- **POST** `/api/tick/{player_id}` - Processa tick di gioco

### Gestione Locanda
- **POST** `/api/add-room/{player_id}` - Costruisce nuova stanza
  - Body: `{"room_type": "basic|standard|deluxe|royal"}`
- **POST** `/api/clean-room/{player_id}/{room_id}` - Pulisce stanza
- **POST** `/api/purchase-upgrade/{player_id}/{upgrade_id}` - Acquista upgrade

### Sistema Taverna 🍺
- **POST** `/api/unlock-recipe/{player_id}/{recipe_id}` - Sblocca ricetta
  - Es: `/api/unlock-recipe/player1/recipe_food_roast`
- **POST** `/api/craft-item/{player_id}` - Crafta items
  - Query params: `item_id`, `quantity` (default: 1)
  - Es: `/api/craft-item/player1?item_id=food_bread&quantity=5`
- **POST** `/api/serve-guest/{player_id}` - Servi cibo/bevanda
  - Query params: `guest_id`, `item_id`
  - Es: `/api/serve-guest/player1?guest_id=123&item_id=food_bread`

### Struttura Risposta

Tutti gli endpoint restituiscono l'intero stato di gioco:
```json
{
  "player_id": "player1",
  "gold": 150.5,
  "reputation": 10.2,
  "max_guests": 5,
  "tavern_unlocked": true,
  "item_inventory": {"food_bread": 5, "drink_ale": 3},
  "ingredient_inventory": {"ing_flour": 10, "ing_honey": 2},
  "rooms": [...],
  "guests": [...],
  "upgrades": [...],
  "recipes": [...],
  "available_items": [...],
  "available_ingredients": [...]
}
```

## 🎨 Features Implementate

### Backend Django
- ✅ Database persistente con Django ORM (SQLite)
- ✅ 7 modelli Django (GameState, Room, Guest, TavernItem, Ingredient, Recipe, Upgrade)
- ✅ Django Admin con visualizzazioni ricche e colorate
- ✅ Django REST Framework con serializers
- ✅ Management command per inizializzazione dati
- ✅ Sistema transazioni atomiche
- ✅ CORS configurato per Angular

### Meccaniche di Gioco
- ✅ Sistema di stanze con 4 livelli (Basic, Standard, Deluxe, Royal)
- ✅ 15 tipi diversi di ospiti con spawn pesato
- ✅ Sistema di risorse (oro, reputazione)
- ✅ Meccanica incrementale automatica (tick processing)
- ✅ Sistema di pulizia manuale e automatica
- ✅ Sistema di upgrade con 7 upgrade
- ✅ Costruzione di nuove stanze
- ✅ Gestione pazienza e soddisfazione ospiti
- ✅ Sistema di moltiplicatori di reddito

### Sistema Taverna 🍺
- ✅ 13 tavern items (6 cibi + 8 bevande, 13 totale)
- ✅ 5 livelli di qualità (Basic, Good, Fine, Exquisite, Legendary)
- ✅ Sistema ricette con sblocco progressivo
- ✅ Crafting con costo in oro
- ✅ Serving ospiti con bonus multipli (pazienza, soddisfazione, oro, reputazione)
- ✅ 17 ingredienti con 5 livelli di rarità
- ✅ Sistema drop ingredienti da ospiti soddisfatti (80%+)
- ✅ Bonus drop per guest types specifici (Merchants 2x, Dragons 3x)

### Frontend Angular
- ✅ UI responsive e accattivante
- ✅ Aggiornamenti real-time con RxJS
- ✅ Componenti standalone Angular 17
- ✅ TypeScript con interfacce tipizzate

## 🚀 Possibili Miglioramenti Futuri

### Backend
- 🔄 Migrazione a PostgreSQL per production
- 👥 Sistema di autenticazione JWT multi-giocatore
- 📊 API di statistiche e leaderboard
- 🎭 Eventi random schedulati (festival, invasioni)
- 🏆 Sistema di achievement con tracking
- 🔧 Celery per task asincroni
- 📈 Monitoring e logging avanzato

### Frontend
- 🎨 Aggiornamento UI per taverna
- 🎵 Audio e musica di sottofondo
- 🌙 Tema scuro/chiaro
- 📱 Ottimizzazione mobile/responsive
- 📊 Grafici di progresso con Chart.js
- 🎬 Animazioni e transizioni
- 💬 Notifiche push

### Gameplay
- 🧪 **Sistema combinazione ingredienti** - Scopri nuove ricette sperimentando
- 🛡️ Sistema di difesa da eventi negativi
- 🗺️ Espansione con multiple locande/città
- 💎 Valuta premium per speed-up
- 🎲 Mini-giochi per bonus
- 🏪 Negozio per vendere items
- 👨‍🍳 Staff da assumere (cuochi, camerieri)
- 🎪 Eventi stagionali e limited-time

## 📝 Licenza

Questo è un progetto educativo e dimostrativo.

## 🤝 Contributi

Contributi, issues e feature requests sono benvenuti!

---

Divertiti a gestire la tua locanda fantasy! 🏰✨
