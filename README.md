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

FAITBien joué — c'est la dernière pièce du backlog. Récapitulons où en est le projet maintenant.
Récap final du projet FreelanceHub API
✅ Bloc A — Setup Docker + FastAPI
✅ Bloc B — SQLAlchemy + Alembic
✅ Bloc C — Authentification JWT
✅ Bloc D — Client + rattachement automatique
✅ Bloc E — Permissions (require_freelance) + accès client lecture seule
✅ Bloc F — Projects CRUD complet
✅ Bloc G — Tasks CRUD complet + cascade de suppression
✅ Bloc H — Logging structuré des requêtes
✅ Bloc I — README complet

32 tests automatisés, 93% de couverture
Ce qui reste, uniquement les points "optionnels" du backlog
Rappel de la dernière section du backlog, explicitement marquée comme non prioritaire :

Pagination sur GET /projects et GET /tasks
PATCH /users/me
Script de seed pour la démo

Ces trois points sont clairement étiquetés "si tu as du temps en rab" — le cœur du projet est terminé et solide sans eux.
Dernière vérification avant de considérer le projet fini
Le backlog mentionnait un "test à blanc" — vérifier que docker-compose up fonctionne sur un dossier fraîchement cloné, pour s'assurer qu'un recruteur qui clone ton repo n'aura aucune surprise. Veux-tu qu'on fasse ce test (cloner dans un nouveau dossier et vérifier que tout démarre sans ton venv/configuration locale), ou tu es confiant que ça fonctionnera vu qu'on a suivi Docker de bout en bout ?VERIFIONBonne prudence — c'est le test le plus révélateur, il simule exactement ce qu'un recruteur ferait en clonant ton repo.
Étape 1 — Cloner dans un dossier neutre
Ouvre un terminal dans un dossier différent (pas dans freelancehub-api), par exemple directement dans C:\Users\Paris\ :
powershellcd C:\Users\Paris
git clone https://github.com/minna74/freelancehub-api.git freelancehub-test
cd freelancehub-test
Remarque : on clone dans un dossier au nom différent (freelancehub-test) pour être sûr de ne pas toucher accidentellement à ton projet original.
Étape 2 — Vérifier qu'il n'y a pas de fichier .env (normal, il est dans .gitignore)
powershellls
Remarque importante à vérifier : .env ne doit pas apparaître dans cette liste (puisqu'il est ignoré par Git) — ce qui veut dire que docker-compose up va probablement échouer sans lui, puisque docker-compose.yml en dépend (env_file: .env). C'est le point le plus probable de friction pour un nouvel utilisateur.
Étape 3 — Tenter le démarrage tel quel (pour confirmer le problème)
powershelldocker-compose up -d
Colle-moi le résultat de ls et de cette commande — je m'attends à une erreur liée à l'absence de .env, qu'on va devoir documenter (ou résoudre) dans le README.(venv) PS C:\Users\Paris\freelancehub-test> LS
    Répertoire : C:\Users\Paris\freelancehub-test
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        04/07/2026     15:28                alembic
d-----        04/07/2026     15:28                app
d-----        04/07/2026     15:28                docs
d-----        04/07/2026     15:28                tests
-a----        04/07/2026     15:28           4846 .gitignore
-a----        04/07/2026     15:28           5121 alembic.ini
-a----        04/07/2026     15:28            858 docker-compose.yaml
-a----        04/07/2026     15:28            229 Dockerfile
-a----        04/07/2026     15:28           4195 README.md
-a----        04/07/2026     15:28            171 requirements.txt
(venv) PS C:\Users\Paris\freelancehub-test>Afficher plusConfirmé, exactement ce qu'on attendait : .env est absent — normal, il est dans .gitignore et n'a jamais été poussé sur GitHub (bonne pratique de sécurité, on ne commit jamais de secrets).
Remarque importante à noter : ton fichier s'appelle docker-compose.yaml ici, alors que partout dans nos échanges on l'a appelé docker-compose.yml — vérifie que c'est bien le même fichier et pas une différence accidentelle. Les deux extensions fonctionnent avec Docker Compose, donc ce n'est pas un problème technique, juste une incohérence de nommage à noter mentalement.
Tentative de démarrage — pour confirmer le problème
powershelldocker-compose up -d
Cette commande va très probablement échouer ou démarrer avec des valeurs manquantes, puisque docker-compose.yaml référence des variables (${POSTGRES_USER}, ${DB_URL}, etc.) qui n'existent nulle part sans .env.
Colle-moi le résultat exact.PS C:\Users\Paris\freelancehub-test> docker-compose up -d
time="2026-07-04T15:31:14+01:00" level=warning msg="The \"POSTGRES_USER\" variable is not set. Defaulting to a blank string."
time="2026-07-04T15:31:15+01:00" level=warning msg="The \"POSTGRES_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-07-04T15:31:15+01:00" level=warning msg="The \"POSTGRES_DB\" variable is not set. Defaulting to a blank string."
time="2026-07-04T15:31:15+01:00" level=warning msg="The \"POSTGRES_USER\" variable is not set. Defaulting to a blank string."
time="2026-07-04T15:31:15+01:00" level=warning msg="The \"POSTGRES_DB\" variable is not set. Defaulting to a blank string."
time="2026-07-04T15:31:15+01:00" level=warning msg="The \"POSTGRES_USER\" variable is not set. Defaulting to a blank string."
time="2026-07-04T15:31:15+01:00" level=warning msg="The \"POSTGRES_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-07-04T15:31:15+01:00" level=warning msg="The \"POSTGRES_DB\" variable is not set. Defaulting to a blank string."
env file C:\Users\Paris\freelancehub-test\.env not found: GetFileAttributesEx C:\Users\Paris\freelancehub-test\.env: The system cannot find the file specified.
(venv) PS C:\Users\Paris\freelancehub-test>Afficher plusConfirmé, exactement le problème anticipé : env file C:\...\.env not found — sans ce fichier, impossible de démarrer. C'est exactement ce qu'un recruteur (ou n'importe qui clonant ton repo) rencontrerait.
Solution — créer un fichier .env.example
Remarque sur la bonne pratique standard : on ne commit jamais le vrai .env (secrets), mais on commit un .env.example — un modèle sans valeurs sensibles réelles, que la personne copie et adapte. C'est la convention universelle sur GitHub.
Retourne dans ton vrai projet (freelancehub-api, pas le clone de test) et crée un fichier .env.example à la racine avec ce contenu :
POSTGRES_USER=freelancehub
POSTGRES_PASSWORD=freelancehub_dev
POSTGRES_DB=freelancehub
POSTGRES_PORT=5432
API_PORT=8000
DB_URL=postgresql://freelancehub:freelancehub_dev@localhost:5432/freelancehub
SECRET_KEY=change-moi-en-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Remarque sur SECRET_KEY : dans ce fichier d'exemple, on met une valeur clairement factice (change-moi-en-production) plutôt que ta vraie clé — même si ta vraie clé n'est pas ultra-sensible en développement, c'est le principe qui compte pour l'habitude.
Mise à jour du README
Ajoute cette section dans README.md, juste avant la section "Installation et démarrage" :

## Configuration

Copier le fichier d'exemple et l'adapter si besoin (les valeurs par défaut fonctionnent telles quelles en local) :

```bash
cp .env.example .env
```

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