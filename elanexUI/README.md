# Spice Route Emporium

i have got a project from client and the client is a cardomom manufacturer and seller so they need a website for marketing and selling cardomom and its seed so i decided to build it 

this is the tech stacks:
Frontend: Next.js + TypeScript + Tailwind CSS
Backend: Django + Django REST Framework
Database: PostgreSQL
Cache/background: Redis, with Celery added when needed

also i showed a demo landing page to the client and they liked it so i need to develope almost the same one i showed and i attached it with this please help me create a landing page, cart page, product page then whatever left

This project was built with [Lovable](https://lovable.dev) and uses Vite,
TanStack Router, and React.

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
