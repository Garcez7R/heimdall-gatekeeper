# Cloudflare Deployment

Heimdall Gatekeeper is now prepared to run on Cloudflare using:

- `Pages` for the static SecOps dashboard in `frontend/`
- `Pages Functions` for the API in `functions/`
- `D1` for events, alerts and metrics

## Included in this repo

- Root [wrangler.toml](/home/rgarcez/Documentos/heimdall-gatekeeper/wrangler.toml)
- D1 schema at [cloudflare/d1/0001_init.sql](/home/rgarcez/Documentos/heimdall-gatekeeper/cloudflare/d1/0001_init.sql)
- Pages Functions API under [functions/](/home/rgarcez/Documentos/heimdall-gatekeeper/functions)

The frontend already points to `/api/*`, so no code changes are needed to deploy the dashboard on Pages.

## Deployment flow

1. Create a D1 database in Cloudflare.
2. Copy the generated `database_id`.
3. Replace `replace-with-your-d1-id` in [wrangler.toml](/home/rgarcez/Documentos/heimdall-gatekeeper/wrangler.toml).
4. Apply the schema from [cloudflare/d1/0001_init.sql](/home/rgarcez/Documentos/heimdall-gatekeeper/cloudflare/d1/0001_init.sql).
5. Create a Pages project pointing to this repository root.
6. Keep `frontend` as the build output directory.
7. Deploy and verify:
   - `/api/config`
   - `/api/overview`
   - `/api/demo/bootstrap`

## CLI example

```bash
npx wrangler d1 create heimdall-gatekeeper
npx wrangler d1 execute heimdall-gatekeeper --remote --file=cloudflare/d1/0001_init.sql
```

## Notes

- The FastAPI backend remains useful for local development and Docker demos.
- The Cloudflare version uses the Pages Functions implementation in `functions/`.
- Demo data is automatically seeded through the D1-backed API when the database is empty.
