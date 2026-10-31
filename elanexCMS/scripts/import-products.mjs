import { createClient } from "@sanity/client";

const projectId = process.env.SANITY_PROJECT_ID;
const dataset = process.env.SANITY_DATASET ?? "production";
const token = process.env.SANITY_API_TOKEN;
const sourceApiUrl = process.env.SOURCE_PRODUCTS_API_URL;

if (!projectId || !token || !sourceApiUrl) {
  throw new Error(
    "Set SANITY_PROJECT_ID, SANITY_API_TOKEN, and SOURCE_PRODUCTS_API_URL before importing products.",
  );
}

const client = createClient({
  projectId,
  dataset,
  apiVersion: "2025-01-01",
  token,
  useCdn: false,
});

const response = await fetch(sourceApiUrl);
if (!response.ok) {
  throw new Error(`Could not read the existing product API: HTTP ${response.status}`);
}

const products = await response.json();
if (!Array.isArray(products)) {
  throw new Error("The existing product API did not return a product list.");
}

for (const product of products) {
  const imageResponse = await fetch(product.image);
  if (!imageResponse.ok) {
    throw new Error(
      `Could not download the image for ${product.name}: HTTP ${imageResponse.status}`,
    );
  }

  const imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
  const filename = `${product.id}.jpg`;
  const asset = await client.assets.upload("image", imageBuffer, { filename });

  await client.createOrReplace({
    _id: `product-${product.id}`,
    _type: "product",
    name: product.name,
    slug: { _type: "slug", current: product.id },
    description: product.description ?? "",
    price: Number(product.price),
    image: {
      _type: "image",
      asset: { _type: "reference", _ref: asset._id },
    },
    category: product.category,
    available: true,
  });

  console.log(`Imported ${product.name}`);
}

console.log(`Imported ${products.length} product(s).`);
