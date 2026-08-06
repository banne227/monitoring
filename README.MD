# Bot de veille d'annonces en ligne

*[Read this in English](./README.en.md)*

## Le problème

Sur n'importe quel marché d'annonces — immobilier, véhicules d'occasion, offres d'emploi, matériel spécialisé... — les meilleures opportunités partent en quelques heures. Passer plusieurs fois par jour sur un site pour vérifier les nouveautés est chronophage et peu fiable : on rate forcément des occasions.

Ce bot surveille automatiquement les nouvelles annonces publiées sur un site donné selon des critères définis (localisation, budget, mots-clés...) et envoie une notification par email dès qu'une nouvelle annonce correspondante est publiée. Aucune intervention manuelle requise.

**Cette implémentation cible [PAP.fr](https://www.pap.fr) (annonces immobilières) à titre d'exemple concret**, mais le principe et l'architecture s'appliquent à n'importe quel site d'annonces : véhicules (Leboncoin, La Centrale), emploi (Indeed), équipement professionnel, etc. Seul le module de scraping change d'un site à l'autre — le reste (dédup, notification, planification, logs) est directement réutilisable.

## Aperçu

![Exemple d'email reçu](./docs/screenshot-email.png)

*Capture d'écran : notification reçue pour une nouvelle annonce détectée.*

## Fonctionnalités

- Scraping automatique des résultats de recherche du site cible (PAP.fr dans cet exemple)
- Filtrage par critères géré directement via l'URL de recherche du site (aucun paramétrage supplémentaire côté code, quel que soit le site)
- Détection des nouvelles annonces uniquement (déduplication basée sur l'identifiant unique de chaque annonce)
- Notification email instantanée dès qu'une nouvelle annonce est détectée
- Exécution automatique planifiée via cron, à intervalle configurable
- Logging complet de l'activité (succès, erreurs réseau, échecs d'envoi)

## Stack technique

| Composant | Choix | Pourquoi |
|---|---|---|
| Scraping | `requests` + `BeautifulSoup` | Simple, léger, suffisant pour du HTML statique (pas besoin d'un navigateur headless) |
| Notification | `smtplib` (SMTP Gmail) | Aucune dépendance externe, gratuit, fiable |
| Déduplication | Fichier texte + `set` Python | Lookup en O(1), pas besoin d'une base de données pour ce volume |
| Planification | `cron` | Le bot n'a besoin de tourner que ponctuellement — plus léger et plus simple à superviser qu'un process qui tourne en continu |
| Logging | Module `logging` (standard) | Traçabilité complète sans dépendance supplémentaire |

## Architecture

```
monitoring_bot/
├── main.py           # Point d'entrée : orchestre le scraping, la dédup et l'envoi
├── scrapper.py        # Récupération et parsing des annonces PAP.fr
├── storage.py         # Gestion des identifiants d'annonces déjà vues
├── notifier.py         # Envoi des notifications par email
├── setup_cron.py       # Installation automatique de la tâche planifiée
├── .env.example       # Modèle de configuration
└── requirements.txt
```

## Installation

### 1. Cloner le projet et installer les dépendances

```bash
git clone <url-du-repo>
cd monitoring_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurer les variables d'environnement

Copier `.env.example` vers `.env` et renseigner les valeurs :

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `SEARCH_URL` | URL de recherche PAP.fr avec vos critères (localisation, budget...) déjà appliqués |
| `EMAIL_ADDRESS` | Adresse Gmail utilisée pour l'envoi |
| `EMAIL_APP_PASSWORD` | Mot de passe d'application Gmail (voir ci-dessous) |
| `EMAIL_TO` | Adresse destinataire des notifications |

Pour obtenir `SEARCH_URL` : effectuez une recherche sur PAP.fr avec vos critères, puis copiez l'URL générée dans la barre d'adresse.

**Pour obtenir `EMAIL_APP_PASSWORD`** (un mot de passe Gmail classique ne fonctionnera pas) :
1. Activez la validation en 2 étapes sur le compte Google utilisé, si ce n'est pas déjà fait : [myaccount.google.com/security](https://myaccount.google.com/security)
2. Rendez-vous sur [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Donnez un nom à l'application (ex. `Bot veille`) et cliquez sur "Créer"
4. Copiez le mot de passe généré (16 caractères) dans `EMAIL_APP_PASSWORD` — il ne sera plus jamais réaffiché ensuite

### 3. Tester manuellement

```bash
python3 main.py
```

### 4. Automatiser l'exécution

```bash
python3 setup_cron.py --interval 30
```

Le paramètre `--interval` définit la fréquence en minutes (30 par défaut). Le script est idempotent : le relancer met à jour la tâche existante sans créer de doublon.

### Désinstaller la tâche planifiée

```bash
crontab -l | grep -v "# bot-veille-pap" | crontab -
```

## Logs

Toute l'activité du bot est tracée dans `bot.log` (succès, erreurs de scraping, échecs d'envoi d'email). Les sorties standard de cron sont redirigées vers `cron.log`.

## Limites actuelles et évolutions possibles

- Filtrage limité aux critères disponibles nativement sur le site cible ; un filtrage avancé côté code (mots-clés, critères combinés...) peut être ajouté sur demande
- Un seul canal de notification (email) ; d'autres canaux (Telegram, Slack, webhook...) peuvent être intégrés
- Un seul site source dans cet exemple ; l'architecture permet d'adapter le bot à n'importe quel autre site d'annonces (immobilier, véhicules, emploi...) en ne remplaçant que le module de scraping

## Licence

Projet développé sur mesure — usage et adaptation possibles sur demande.