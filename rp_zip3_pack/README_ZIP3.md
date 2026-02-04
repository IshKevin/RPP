# RevenuePressAI — ZIP3 (Ops + Marketing + Deployment)

Contents:
- **ops/** 90-day daily execution plans (Smit/Isha/Boris) + Daily Command Report template
- **marketing/** 5 EN/FR video ad scripts + posting playbook (free-footage)
- **deployment/** Dockerfile, docker-compose, .env example, Nginx sample, GitLab CI test
- **qa/** compileall report

How to use:
1) Replace deployment/.env.example with deployment/.env and set keys
2) Put ZIP1 source folder one level above deployment/ (or adjust docker-compose build context)
3) Run: `docker compose -f deployment/docker-compose.yml up --build`

Notes:
- Payment methods are configured via environment variables; you can enable only what you need.
- All content should remain bilingual and auto-detect language.
