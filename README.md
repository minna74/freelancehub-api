# FreelanceHub API

API REST backend pour la gestion de projets et clients freelance, avec isolation stricte multi-utilisateurs et authentification JWT.

## Contexte

Projet personnel construit pour consolider des compétences backend (Python/FastAPI) en vue d'une spécialisation DevOps. L'accent est mis sur une architecture propre (séparation routes/schémas/modèles), la sécurité (isolation des données par utilisateur), et une couverture de tests systématique plutôt que sur la richesse fonctionnelle.

## Stack technique

- **Framework** : FastAPI
- **Base de données** : PostgreSQL
- **ORM** : SQLAlchemy + Alembic (migrations versionnées)
- **Authentification** : JWT (python-jose) + hash argon2 (passlib)
- **Tests** : Pytest (32 tests, 93% de couverture)
- **Conteneurisation** : Docker + docker-compose

## Modèle de données

User (freelance ou client)
│
└── Client (créé par un freelance, rattaché automatiquement
│        à un compte User "client" par email à l'inscription)
│
└── Project (appartient à un Client et à un Freelance)
│
└── Task (statut, priorité, échéance optionnelle)

Chaque freelance est isolé des autres : il ne voit que ses propres clients, projets et tâches. Un client, une fois inscrit et rattaché à sa fiche, a un accès en lecture seule à ses projets et tâches.

## Installation et démarrage

Prérequis : Docker et Docker Compose installés.

```bash
git clone https://github.com/minna74/freelancehub-api.git
cd freelancehub-api
docker-compose up -d
```

L'API est accessible sur `http://localhost:8000`, la documentation interactive sur `http://localhost:8000/docs`.

Appliquer les migrations (si pas déjà fait automatiquement) :

```bash
alembic upgrade head
```

## Lancer les tests

```bash
pip install -r requirements.txt
pytest -v
```

Avec couverture :

```bash
pytest --cov=app
```

## Endpoints principaux

| Méthode | Route | Description |
|---|---|---|
| POST | `/auth/register` | Inscription (freelance ou client) |
| POST | `/auth/login` | Connexion, renvoie un JWT |
| GET | `/auth/me` | Profil de l'utilisateur connecté |
| POST | `/clients/` | Créer une fiche client (freelance) |
| GET | `/clients/` | Lister ses clients (freelance) |
| GET | `/clients/{id}` | Détail d'un client |
| POST | `/projects/` | Créer un projet |
| GET | `/projects/` | Lister ses projets (freelance ou client) |
| GET, PATCH, DELETE | `/projects/{id}` | Détail, modification, suppression |
| POST | `/tasks/` | Créer une tâche |
| GET | `/tasks/?statut=` | Lister ses tâches, filtre optionnel par statut |
| GET, PATCH, DELETE | `/tasks/{id}` | Détail, modification, suppression |

## Choix techniques et simplifications assumées

- **Pas de refresh token** — un seul access token JWT avec expiration fixe, suffisant pour l'exercice.
- **Pas de facturation** — hors scope, le projet se concentre sur la gestion de projets/tâches.
- **Pas de notion d'équipe** — un freelance gère seul ses tâches, pas d'assignation multi-utilisateurs.
- **Email non unique sur `Client`** — volontaire, un même email peut apparaître chez plusieurs freelances différents sans conflit (l'unicité n'a de sens que par freelance, pas globalement).
- **Rattachement automatique par email** — si plusieurs fiches `Client` non activées partagent le même email chez des freelances différents, seule la première trouvée est rattachée à l'inscription (cas limite assumé).
- **`freelance_id` dupliqué sur `Project`** — dénormalisation volontaire pour simplifier et accélérer les requêtes de filtrage par freelance, au prix d'une donnée techniquement déductible via `Client`.

## Sécurité

- Mots de passe hashés avec argon2 (jamais stockés en clair).
- Isolation stricte testée à chaque niveau (`Client`, `Project`, `Task`) : un freelance ne peut ni consulter ni modifier les ressources d'un autre freelance, même en devinant des identifiants.
- Vérification systématique de la chaîne de propriété avant toute lecture/modification/suppression (protection contre les failles de type IDOR).