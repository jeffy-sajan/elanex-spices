import { createClient } from "@sanity/client";

export type Product = { id: string; name: string; description: string | null; price: number; image: string; category: 'cardamom' | 'seeds' };
export let products: Product[] = [];
export const money = (amount: number) => '₹' + amount.toLocaleString('en-IN');
const WHATSAPP_NUMBER = '918921263343';
export const whatsappContactUrl = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent('Hello, I would like to enquire about Elanex Spices.')}`;
export const whatsappEnquiryUrl = (productName: string) =>
  `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(`Hello, I would like to enquire about this product: ${productName}.`)}`;
export function metadata(title: string, description: string) { const pageTitle = title === 'Elanex Spices' ? title : `Elanex Spices | ${title}`; return { meta: [{ title: pageTitle }, { name: 'description', content: description }, { property: 'og:title', content: pageTitle }, { property: 'og:description', content: description }, { property: 'og:type', content: 'website' }, { name: 'twitter:card', content: 'summary_large_image' }] }; }

const API_BASE_URL =
  import.meta.env["VITE_API_BASE_URL"] ?? "http://127.0.0.1:8000/api";
const SANITY_PROJECT_ID = import.meta.env["VITE_SANITY_PROJECT_ID"];
const SANITY_DATASET = import.meta.env["VITE_SANITY_DATASET"] ?? "production";
const SANITY_API_VERSION = import.meta.env["VITE_SANITY_API_VERSION"] ?? "2025-01-01";
const sanityClient = SANITY_PROJECT_ID
  ? createClient({
      projectId: SANITY_PROJECT_ID,
      dataset: SANITY_DATASET,
      apiVersion: SANITY_API_VERSION,
      useCdn: true,
    })
  : null;

const PRODUCTS_QUERY = `*[
  _type == "product" &&
  defined(slug.current) &&
  available != false
] | order(coalesce(sortOrder, 9999) asc, _createdAt asc) {
  "id": slug.current,
  name,
  description,
  price,
  "image": image.asset->url,
  category
}`;

let productsRequest: Promise<Product[]> | null = null;

function fetchProductsFromDjango(): Promise<Product[]> {
  return fetch(`${API_BASE_URL}/products/`, {
    headers: { Accept: "application/json" },
    cache: "no-store",
  }).then(async (response) => {
    if (!response.ok) {
      throw new Error(`Product request failed with status ${response.status}`);
    }
    return (await response.json()) as Product[];
  });
}

function fetchProductsFromSanity(): Promise<Product[]> {
  if (!sanityClient) {
    return Promise.reject(new Error("Sanity is not configured."));
  }
  return sanityClient.fetch<Product[]>(PRODUCTS_QUERY);
}

export function fetchProducts(): Promise<Product[]> {
  if (!productsRequest) {
    productsRequest = (sanityClient
      ? fetchProductsFromSanity()
      : fetchProductsFromDjango())
      .then((data) => {
        products = data;
        return data;
      })
      .finally(() => {
        productsRequest = null;
      });
  }

  return productsRequest;
}
