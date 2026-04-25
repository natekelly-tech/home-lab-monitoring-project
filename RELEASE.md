# LabWatch Backend — Release Process
Auxcon Technologies

## Branching

All work happens on feature branches. Main is always deployable.
No commits go directly to main.

## Versioning

Follow semantic versioning: MAJOR.MINOR.PATCH
Tags are the release mechanism. A tag triggers the production build.

- PATCH: config changes, bug fixes, dependency updates
- MINOR: new endpoints, new monitored services
- MAJOR: breaking API contract changes

## CI/CD Pipeline (GitHub Actions)

Workflow file: .github/workflows/docker-build.yml
Trigger: push of a version tag (v*)

Steps:
1. Checkout code
2. Set up Docker buildx
3. Login to DockerHub (auxcon)
4. Build multi-platform image (linux/amd64, linux/arm64)
5. Push to DockerHub as auxcon/labwatch-api:VERSION and auxcon/labwatch-api:latest

Regular commits to main do NOT trigger a build.
Only version tags trigger a production image push.

## Release Workflow

1. Work on feature branch, merge PR to main
2. Verify the change looks right: git log --oneline -3
3. Tag the release: git tag v0.5.0 && git push origin v0.5.0
4. Watch GitHub Actions complete at github.com/natekelly-tech/homelab-monitoring-project/actions
5. Pull and deploy on EC2:
   - ssh -i C:\Users\kh4r0\.ssh\id_ed25519 ubuntu@54.67.70.105
   - cd /home/ubuntu/lab
   - docker compose pull
   - docker compose down && docker compose up -d
6. Verify: curl https://api.auxcon.dev/status

## Rollback

Edit docker-compose.yml to pin a specific version:

    image: auxcon/labwatch-api:0.4.1

Then restart: docker compose down && docker compose up -d
Revert to latest tag when the fix is released.

## Changelog

CHANGELOG.md at repo root. One entry per tag.

Example:
    v0.5.0 — 2026-05-01
    Added: GET /history/<name> endpoint for time-series data
    Fixed: LabWatch API self-monitoring URL changed from localhost to public URL

## Production Environment

| Item        | Value                        |
|-------------|------------------------------|
| Host        | AWS EC2 us-west-1            |
| Public URL  | https://api.auxcon.dev       |
| Image       | auxcon/labwatch-api:latest   |
| Deploy path | /home/ubuntu/lab/            |

## What Never Deploys Automatically

Production on EC2 always requires a manual docker compose pull and docker compose up -d.
There is no auto-deploy to EC2. The manual step is intentional.
It gives a human a moment to verify the Actions build succeeded before the change goes live.
