# 🏰 Fantasy Inn Tycoon

Un gioco gestionale/incrementale per browser dove gestisci una locanda in un mondo fantasy! Costruisci stanze, accogli ospiti, guadagna oro e migliora la tua locanda.

## 🎮 Caratteristiche del Gioco

### Meccaniche di Gioco
- **Gestione Stanze**: Costruisci e gestisci diverse tipologie di stanze (Basic, Standard, Deluxe, Royal)
- **Sistema Ospiti**: Accogli vari tipi di ospiti (contadini, mercanti, nobili, avventurieri, maghi)
- **Risorse**: Gestisci oro e reputazione per espandere la tua locanda
- **Upgrade**: Sblocca miglioramenti per aumentare i guadagni e automatizzare la gestione
- **Meccanica Incrementale**: Il gioco progredisce automaticamente con tick periodici
- **Pulizia Stanze**: Mantieni le stanze pulite per mantenere gli ospiti felici

### Tipologie di Stanze
- 🛏️ **Basic**: Stanza base (50 oro, 1x guadagno)
- 🏠 **Standard**: Stanza standard (200 oro, 2x guadagno)
- 🏰 **Deluxe**: Stanza di lusso (800 oro, 4x guadagno)
- 👑 **Royal**: Stanza reale (3000 oro, 8x guadagno)

### Tipi di Ospiti
- 🧑‍🌾 **Peasant**: Basso pagamento, bassa reputazione
- 💼 **Merchant**: Pagamento medio, reputazione media
- 👔 **Noble**: Alto pagamento, alta reputazione
- ⚔️ **Adventurer**: Buon pagamento, buona reputazione
- 🧙 **Wizard**: Ottimo pagamento, ottima reputazione

## 🛠️ Stack Tecnologico

### Frontend
- **Angular 17** - Framework frontend
- **TypeScript** - Linguaggio di programmazione
- **RxJS** - Programmazione reattiva

### Backend
- **FastAPI** - Framework web Python
- **Pydantic** - Validazione dati
- **Uvicorn** - Server ASGI

## 📋 Prerequisiti

- **Node.js** (versione 18 o superiore)
- **npm** o **yarn**
- **Python** (versione 3.9 o superiore)
- **pip** (gestore pacchetti Python)

## 🚀 Installazione

### 1. Backend Setup

```bash
# Naviga nella directory backend
cd backend

# Crea un ambiente virtuale Python (opzionale ma consigliato)
python -m venv venv

# Attiva l'ambiente virtuale
# Su Linux/Mac:
source venv/bin/activate
# Su Windows:
venv\Scripts\activate

# Installa le dipendenze
pip install -r requirements.txt

# Avvia il server FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Il server backend sarà disponibile su `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

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
1. **Guadagna Oro**: Assegna ospiti alle stanze per generare reddito passivo
2. **Costruisci Stanze**: Espandi la tua locanda con stanze migliori
3. **Sblocca Upgrade**: Acquista miglioramenti per aumentare i guadagni
4. **Mantieni la Reputazione**: Tieni gli ospiti felici mantenendo le stanze pulite

### Gameplay
1. **Ospiti in Attesa**: Gli ospiti arrivano automaticamente e aspettano nella lobby
2. **Assegnazione Stanze**: Clicca su un ospite in attesa, poi clicca su una stanza vuota per assegnarlo
3. **Pulizia**: Le stanze si sporcano nel tempo. Puliscile manualmente o acquista l'upgrade "Hire Cleaning Staff"
4. **Pazienza**: Gli ospiti hanno una barra di pazienza che diminuisce se la stanza è sporca
5. **Guadagni**: Ogni tick genera oro in base al tipo di ospite, stanza e moltiplicatori
6. **Upgrade**: Usa l'oro per acquistare upgrade permanenti
7. **Espansione**: Costruisci nuove stanze per ospitare più clienti

### Strategia
- Inizia costruendo stanze Basic economiche per massimizzare il numero di ospiti
- Mantieni le stanze pulite per evitare che gli ospiti se ne vadano
- Prioritizza gli upgrade che aumentano il moltiplicatore di reddito
- Investi in stanze migliori quando hai abbastanza oro
- L'upgrade "Auto Clean" è essenziale per la gestione a lungo termine

## 🏗️ Struttura del Progetto

```
inn-browser/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── game_models.py      # Modelli Pydantic
│   │   ├── routes/
│   │   │   └── game_routes.py      # Endpoint API
│   │   └── services/
│   │       └── game_service.py     # Logica di business
│   ├── main.py                     # Entry point FastAPI
│   └── requirements.txt            # Dipendenze Python
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/         # Componenti Angular
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

## 🔌 API Endpoints

### GET `/api/game/state/{player_id}`
Ottiene lo stato attuale del gioco per un giocatore

### POST `/api/game/new/{player_id}`
Inizia una nuova partita

### POST `/api/game/tick/{player_id}`
Processa un tick di gioco (chiamato automaticamente dal frontend)

### POST `/api/game/assign-guest/{player_id}`
Assegna un ospite a una stanza
- Query params: `guest_id`, `room_id`

### POST `/api/game/clean-room/{player_id}/{room_id}`
Pulisce manualmente una stanza

### POST `/api/game/purchase-upgrade/{player_id}/{upgrade_id}`
Acquista un upgrade

### POST `/api/game/build-room/{player_id}`
Costruisce una nuova stanza
- Query param: `room_type` (basic, standard, deluxe, royal)

## 🎨 Features Implementate

- ✅ Sistema di stanze con diversi livelli
- ✅ Sistema ospiti con vari tipi
- ✅ Sistema di risorse (oro, reputazione)
- ✅ Meccanica incrementale automatica
- ✅ Sistema di pulizia manuale e automatica
- ✅ Sistema di upgrade
- ✅ Costruzione di nuove stanze
- ✅ UI responsive e accattivante
- ✅ Aggiornamenti real-time
- ✅ Gestione pazienza ospiti
- ✅ Sistema di moltiplicatori

## 🚀 Possibili Miglioramenti Futuri

- 🔄 Sistema di salvataggio persistente (database)
- 👥 Sistema di autenticazione multi-giocatore
- 📊 Statistiche e grafici di progresso
- 🎭 Eventi random (festival, draghi, etc.)
- 🏆 Sistema di achievement
- 🎵 Audio e musica di sottofondo
- 🌙 Tema scuro/chiaro
- 📱 Ottimizzazione mobile
- 🛡️ Sistema di difesa da mostri
- 🍺 Taverna e negozi aggiuntivi
- 🗺️ Espansione con multiple locande
- 💎 Valute premium
- 🎲 Mini-giochi

## 📝 Licenza

Questo è un progetto educativo e dimostrativo.

## 🤝 Contributi

Contributi, issues e feature requests sono benvenuti!

---

Divertiti a gestire la tua locanda fantasy! 🏰✨
