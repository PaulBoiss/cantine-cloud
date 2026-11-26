# Cantine

Une petite API de menus de cantine, fil rouge du cours **Architecture cloud** (ESGI). Elle est volontairement minuscule : le sujet du cours, c'est l'architecture autour d'elle. On la fait grandir bloc après bloc, d'une seule VM à une architecture sur deux zones, sécurisée et chiffrée en coût.

## Les routes

| Route | Réponse |
| --- | --- |
| `GET /` | `{"app": "cantine", "version": "1.0", "host": "…"}` : le nom d'hôte dit quelle instance a répondu |
| `GET /health` | `{"status": "ok"}` : pour les contrôles de santé |
| `GET /menus?day=lundi` | les plats du jour (lundi à vendredi), `400` pour un autre jour |

L'application écoute sur le port **5000**. Sa base SQLite vit dans le conteneur : elle disparaît avec lui, et chaque instance a la sienne. C'est voulu, on en parle au bloc 2.

## Lancer l'image publiée

```bash
docker run -d -p 80:5000 ghcr.io/paulboiss/cantine-cloud:1.0
curl http://localhost/health
```

## Construire depuis les sources

```bash
docker build -t cantine .
docker run -d -p 80:5000 cantine
```

## Tests

```bash
pip install -r app/requirements.txt pytest
python -m pytest
```

## Publier une nouvelle version (enseignant)

```bash
git tag v1.1
git push origin v1.1
```

Le workflow `image` lance les tests puis publie `ghcr.io/paulboiss/cantine-cloud:1.1` et `:latest`.
