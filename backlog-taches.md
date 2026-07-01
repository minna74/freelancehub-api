# Backlog — FreelanceHub API (format "quelques jours")

Découpage pensé pour 2 à 4 jours de travail effectif, en travaillant avec un agent IA gratuit comme assistant de code. Chaque tâche est volontairement petite pour permettre un commit Git par tâche (historique propre = bon point pour ton GitHub).

**Méthode recommandée avec l'agent IA** : pour chaque tâche, écris d'abord toi-même ce que tu attends en 2-3 phrases avant de demander à l'agent de générer le code. Relis et comprends chaque ligne générée avant de committer. Si tu ne peux pas expliquer une ligne, demande à l'agent de te l'expliquer avant de continuer — sinon l'exercice ne consolide rien.

---

## Jour 1 — Setup + Authentification

### Bloc A — Setup (environ 1h-1h30)
- [ ] Initialiser le repo Git (`.gitignore` Python/Docker inclus)
- [ ] Créer la structure : `app/`, `app/models/`, `app/schemas/`, `app/routers/`, `tests/`
- [ ] Écrire `docker-compose.yml` (service `api` + service `db` PostgreSQL)
- [ ] FastAPI minimal avec endpoint `GET /health` qui répond 200
- [ ] Vérifier que `docker-compose up` lance bien l'API accessible en local
- [ ] Premier commit : "setup: structure projet + docker-compose"

### Bloc B — Connexion DB et migrations (environ 1h)
- [ ] Configurer SQLAlchemy (engine, session, `Base`)
- [ ] Configurer `pydantic-settings` pour lire le `.env` (DB_URL, SECRET_KEY)
- [ ] Initialiser Alembic, vérifier qu'une migration vide s'applique correctement
- [ ] Commit : "setup: connexion DB + alembic"

### Bloc C — Authentification (environ 2h-3h, le plus dense)
- [ ] Modèle `User` (id, email, password_hash, nom, type, créé_le) + migration
- [ ] Schémas Pydantic : `UserCreate`, `UserOut`, `LoginRequest`
- [ ] Fonction de hash/vérification mot de passe (passlib ou argon2-cffi)
- [ ] Endpoint `POST /auth/register`
- [ ] Génération JWT (fonction `create_access_token`)
- [ ] Endpoint `POST /auth/login`
- [ ] Dependency `get_current_user` (décode le JWT, récupère l'utilisateur)
- [ ] Endpoint `GET /users/me`
- [ ] Tests : register OK, register email déjà pris, login OK, login mauvais mot de passe, accès `/users/me` sans token (401)
- [ ] Commit : "feat: authentification JWT"

**Fin de journée 1 attendue** : un utilisateur peut s'inscrire, se connecter, et accéder à son profil. Tests d'auth verts.

---

## Jour 2 — Clients et isolation par freelance

### Bloc D — Modèle Client et rattachement (environ 2h)
- [ ] Modèle `Client` (id, nom, email, freelance_id, user_id nullable) + migration
- [ ] Schémas `ClientCreate`, `ClientOut`
- [ ] Endpoint `POST /clients` (freelance uniquement — dependency de vérification de type)
- [ ] Endpoint `GET /clients` (uniquement ceux du freelance connecté)
- [ ] Endpoint `GET /clients/{id}` (vérifier l'appartenance au freelance)
- [ ] Logique de rattachement automatique : à l'inscription d'un `type=client`, chercher une fiche Client avec le même email et `user_id` null, et la mettre à jour
- [ ] Tests : création client par freelance, isolation (freelance A ne voit pas les clients de freelance B), rattachement auto à l'inscription
- [ ] Commit : "feat: gestion des clients + rattachement auto"

### Bloc E — Dependencies de permission réutilisables (environ 1h)
- [ ] Dependency `require_freelance` (bloque si `type != freelance`)
- [ ] Dependency `require_client` (pour les futurs endpoints en lecture seule client)
- [ ] Refactor des endpoints Clients pour utiliser ces dependencies
- [ ] Commit : "refactor: dependencies de permission centralisées"

**Fin de journée 2 attendue** : un freelance peut créer et lister ses clients, l'isolation entre freelances est garantie et testée, un client qui s'inscrit avec le bon email se rattache automatiquement.

---

## Jour 3 — Projects et Tasks

### Bloc F — Projects (environ 2h)
- [ ] Modèle `Project` (id, nom, description, statut, client_id, freelance_id) + migration
- [ ] Schémas `ProjectCreate`, `ProjectOut`, `ProjectUpdate`
- [ ] `POST /projects` (freelance, vérifie que le client_id lui appartient)
- [ ] `GET /projects` (freelance : les siens / client : uniquement ceux liés à sa fiche)
- [ ] `GET /projects/{id}` (vérification d'accès selon le type d'utilisateur)
- [ ] `PATCH /projects/{id}`, `DELETE /projects/{id}` (freelance uniquement)
- [ ] Tests : isolation freelance, accès lecture seule du client, refus PATCH/DELETE pour un client
- [ ] Commit : "feat: gestion des projets"

### Bloc G — Tasks (environ 2h)
- [ ] Modèle `Task` (id, titre, description, statut, priorité, date_échéance, project_id) + migration
- [ ] Schémas `TaskCreate`, `TaskOut`, `TaskUpdate`
- [ ] `POST /projects/{id}/tasks` (freelance uniquement)
- [ ] `GET /projects/{id}/tasks` (avec filtre `?status=`)
- [ ] `PATCH /tasks/{id}`, `DELETE /tasks/{id}` (freelance uniquement)
- [ ] Cascade : suppression d'un Project supprime ses Tasks (vérifier en test)
- [ ] Tests : CRUD complet, filtre par statut, cascade de suppression
- [ ] Commit : "feat: gestion des tâches"

**Fin de journée 3 attendue** : CRUD complet et fonctionnel sur Projects et Tasks, avec permissions et isolation testées.

---

## Jour 4 — Robustesse, finition, documentation (peut être raccourci à une demi-journée si tu es en avance)

### Bloc H — Gestion d'erreurs et logging (environ 1h30)
- [ ] Exception handlers centralisés (format JSON cohérent pour toutes les erreurs)
- [ ] Vérification systématique des codes HTTP sur tous les endpoints (401/403/404/422)
- [ ] Logging basique des requêtes (méthode, route, status, durée) en console structurée
- [ ] Commit : "feat: gestion d'erreurs centralisée + logging"

### Bloc I — Finition (environ 2h)
- [ ] Relecture rapide de la couverture de tests (`pytest --cov`), combler les trous évidents
- [ ] Nettoyage des descriptions OpenAPI (`/docs` doit être présentable)
- [ ] Rédaction du README : contexte, stack, instructions d'installation (`docker-compose up`), schéma simple du modèle de données, choix techniques et simplifications assumées (pas de refresh token, pas de facturation, etc.)
- [ ] Vérifier `docker-compose up` sur un dossier fraîchement cloné (test à blanc)
- [ ] Commit final : "docs: README + finitions"

**Fin de journée 4 attendue** : projet complet, testé, documenté, prêt à être présenté sur GitHub.

---

## Si tu as du temps en rab (optionnel, ne pas faire avant le reste)
- [ ] Pagination simple (`limit`/`offset`) sur `GET /projects` et `GET /projects/{id}/tasks`
- [ ] Endpoint `PATCH /users/me`
- [ ] Petit script de seed (données de démo) pour faciliter la présentation du projet
