# Cahier des charges — FreelanceHub API (version resserrée, format "quelques jours")

## 1. Contexte et contraintes

Projet d'apprentissage backend pratique (Python/FastAPI), à réaliser en **2 à 4 jours** de travail effectif, avec l'aide d'un agent IA gratuit (Claude Code, Cursor, Copilot ou équivalent) comme assistant de codage.

**Conséquence directe sur le périmètre** : on garde uniquement ce qui est nécessaire pour pratiquer les fondamentaux (auth, relations, permissions, validation, tests) et on supprime tout ce qui est secondaire ou chronophage (facturation, commentaires, notifications, invitations par email). L'objectif n'est pas l'exhaustivité fonctionnelle, mais la **qualité d'exécution** sur un périmètre volontairement réduit.

**Rôle de l'agent IA** : il assiste l'écriture de code (boilerplate, suggestions, debug), mais ne remplace pas ta compréhension. Avant d'accepter une suggestion, tu dois savoir l'expliquer. Sinon l'exercice perd son sens.

## 2. Scénario fonctionnel (rappel)

Plusieurs freelances indépendants utilisent la plateforme, chacun isolé des autres. Chaque freelance gère ses clients, projets et tâches. Un client peut s'auto-inscrire et se rattache automatiquement (par email) à une fiche client existante créée par le freelance ; il a alors un accès en lecture seule à ses projets/tâches.

## 3. Stack technique

- Python 3.12+, FastAPI, Pydantic v2
- PostgreSQL via Docker + docker-compose
- SQLAlchemy + Alembic (migrations)
- JWT (access token uniquement — **pas de refresh token en v1**, simplification assumée pour tenir le délai)
- Pytest + httpx pour les tests
- Logging standard `logging` en JSON simple (pas de lib externe nécessaire)

## 4. Modèle de données (périmètre minimal)

1. **User**
   - id, email (unique), mot de passe hashé, nom, `type` (`freelance` | `client`), créé_le
2. **Client** (fiche)
   - id, nom, email (sert au rattachement auto), freelance_id (FK → User), user_id (FK → User, nullable tant que non activé), créé_le
3. **Project**
   - id, nom, description, statut (`active` | `done` | `archived`), client_id (FK), freelance_id (FK), créé_le
4. **Task**
   - id, titre, description, statut (`todo` | `in_progress` | `done`), priorité (`low` | `medium` | `high`), date_échéance (nullable), project_id (FK), créé_le, modifié_le

Pas de table Comment, pas de table Invoice. Pas de notion d'équipe/multi-freelance par projet.

## 5. Règles métier essentielles

- Isolation stricte : un freelance ne voit/modifie que ses propres clients, projets, tâches.
- Un client connecté ne voit que les projets liés à sa fiche Client, en lecture seule (aucun POST/PATCH/DELETE autorisé pour un `type=client`).
- À l'inscription d'un `type=client`, si une fiche Client existe avec le même email et `user_id` null, rattachement automatique (`user_id` mis à jour).
- Suppression d'un Project entraîne la suppression de ses Tasks (cascade), avec confirmation explicite (paramètre ou double appel, pas de suppression silencieuse).

## 6. Endpoints (périmètre minimal)

**Auth**
- `POST /auth/register` (avec `type`)
- `POST /auth/login` (retourne un access token JWT)

**Users**
- `GET /users/me`

**Clients** (freelance uniquement)
- `POST /clients`
- `GET /clients`
- `GET /clients/{id}`

**Projects**
- `POST /projects` (freelance uniquement)
- `GET /projects` (freelance : tous les siens / client : uniquement les siens)
- `GET /projects/{id}`
- `PATCH /projects/{id}` (freelance uniquement)
- `DELETE /projects/{id}` (freelance uniquement)

**Tasks**
- `POST /projects/{id}/tasks` (freelance uniquement)
- `GET /projects/{id}/tasks` (avec filtre par statut)
- `PATCH /tasks/{id}` (freelance uniquement)
- `DELETE /tasks/{id}` (freelance uniquement)

## 7. Exigences non fonctionnelles (gardées car formatrices, peu coûteuses en temps)

- Gestion d'erreurs centralisée (handlers FastAPI), format JSON cohérent
- Codes HTTP corrects (401 non authentifié / 403 pas le droit / 404 introuvable / 422 validation)
- Variables de config via `.env`
- Tests automatisés sur : auth, isolation freelance, accès lecture seule du client, rattachement automatique
- `docker-compose up` doit suffire à lancer API + DB

## 8. Explicitement hors périmètre (pour respecter le délai)

Facturation, commentaires, notifications/emails, invitations, refresh token, gestion d'équipe multi-freelance, recherche full-text, pagination avancée (un simple `limit`/`offset` basique suffit si tu as le temps, sinon pas bloquant).

## 9. Définition de "terminé"

Tous les endpoints listés fonctionnent, les règles d'isolation et de permission sont testées et passent, `docker-compose up` fonctionne sans intervention manuelle, le README explique l'architecture et les choix faits (y compris les simplifications volontaires comme l'absence de refresh token).
