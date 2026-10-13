# Elanex Spices

Elanex Spices is a cardamom cultivator and seller website. The repository is
organized as a Vite/TanStack React frontend in `elanexUI` and a Django REST
backend in `elanexBE`.

The frontend currently displays the marketing UI and reports Django API health.
The backend provides the API foundation and an admin-managed product catalog.

The first release is a marketing and portfolio website. It displays the
admin-managed product catalogue and product enquiries, but does not include
cart, checkout, ordering, payments, shipping, or customer accounts. Those
features can be added in a later ecommerce phase.

Product images are uploaded through the Django admin and stored in a Supabase
Storage bucket. Product metadata, including the public image URL, is stored in
Supabase PostgreSQL. See [elanexBE/README.md](./elanexBE/README.md) for local
setup, Storage configuration, contact email setup, and admin instructions.
