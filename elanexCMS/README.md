# Elanex Spices Sanity Studio

This folder contains the Sanity Studio used to manage the public product
catalogue. The frontend reads published `product` documents from Sanity's CDN.

## Create the Sanity project

1. Create an account at [sanity.io](https://www.sanity.io/).
2. Create a new project named **Elanex Spices**.
3. Choose the `production` dataset.
4. Copy the project ID from the Sanity project settings.
5. From this folder, install dependencies and create `.env`:

```powershell
npm install
Copy-Item .env.example .env
```

Set the project ID in `elanexCMS/.env`:

```text
SANITY_STUDIO_PROJECT_ID=5tugpqtz
SANITY_STUDIO_DATASET=production
```

## Run the Studio locally

```powershell
npm run dev
```

Open the local Studio URL shown in the terminal and sign in with the Sanity
account. Add a product under **Product**. Product fields include name, URL ID,
description, indicative price, image, category, display order, and visibility.

If the Studio shows **This studio is not registered and cannot access your
content yet**, verify all of the following:

1. `SANITY_STUDIO_PROJECT_ID` is exactly `5tugpqtz` (not `y5tugpqtz`).
2. Run `npx sanity login` from this folder and complete the browser login.
3. In Sanity Manage, add the exact local Studio origin shown by the terminal
   under **API > CORS origins** (usually `http://localhost:3333`).
4. Confirm the logged-in account is a member of project `5tugpqtz`.
5. Stop and restart `npm run dev`.

## Deploy the Studio

```powershell
npm run deploy
```

Follow the prompts to choose the project and deployment hostname. The client
can then manage products through the hosted Studio URL.

## Connect the frontend

In the frontend deployment environment, set:

```text
VITE_SANITY_PROJECT_ID=your-project-id
VITE_SANITY_DATASET=production
VITE_SANITY_API_VERSION=2025-01-01
```

When `VITE_SANITY_PROJECT_ID` is set, the frontend reads products from Sanity.
When it is empty, the current Django product API remains available as a
temporary fallback during migration.

## Import the existing products

Create a Sanity API token with permission to create and update documents. Then
run this from `elanexCMS` while the existing Django API is still available:

```powershell
$env:SANITY_PROJECT_ID="your-project-id"
$env:SANITY_DATASET="production"
$env:SANITY_API_TOKEN="your-write-token"
$env:SOURCE_PRODUCTS_API_URL="https://your-render-service.onrender.com/api/products/"
npm run import:products
```

The script imports product metadata and uploads each existing product image to
Sanity. The token is used only locally and must never be added to Git or
frontend/Vercel environment variables.
