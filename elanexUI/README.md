# Elanex Spices

Elanex Spices is currently a marketing and portfolio website for a cardamom
cultivator and seller.

Tech stack:

- Frontend: Vite, React, TypeScript, and TanStack Router
- Backend: Django and Django REST Framework
- Database: Supabase PostgreSQL
- Storage: Supabase Storage

This project was built with [Lovable](https://lovable.dev) and uses Vite,
TanStack Router, and React.

The current release includes product discovery and enquiry pages only. Cart,
checkout, ordering, payments, shipping, and customer accounts are intentionally
deferred to a future ecommerce phase.

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/1bdf30a7-3df0-4821-b573-8f2c6449fa97).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm install
npm run dev
```

The frontend calls the Django backend health endpoint using
`VITE_API_BASE_URL`. Copy `.env.example` to `.env` for the local default:

```sh
cp .env.example .env
```

For hosting, set `VITE_API_BASE_URL` to the public HTTPS URL of the Django API
and rebuild the frontend. Do not add backend secrets, Supabase service-role
keys, or Resend API keys to frontend environment variables.
