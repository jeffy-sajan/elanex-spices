export type Product = { id: string; name: string; description: string | null; price: number; image: string; category: 'cardamom' | 'seeds' };
export let products: Product[] = [];
export const money = (amount: number) => '₹' + amount.toLocaleString('en-IN');
const WHATSAPP_NUMBER = '918921263343';
export const whatsappEnquiryUrl = (productName: string) =>
  `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(`Hello, I would like to enquire about this product: ${productName}.`)}`;
export function metadata(title: string, description: string) { const pageTitle = title === 'Elanex Spices' ? title : `Elanex Spices | ${title}`; return { meta: [{ title: pageTitle }, { name: 'description', content: description }, { property: 'og:title', content: pageTitle }, { property: 'og:description', content: description }, { property: 'og:type', content: 'website' }, { name: 'twitter:card', content: 'summary_large_image' }] }; }

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api";
const PRODUCT_CACHE_KEY = "elanex-products-cache";
const PRODUCT_CACHE_TTL_MS = 5 * 60 * 1000;

type ProductCache = {
  products: Product[];
  cachedAt: number;
};

let productsRequest: Promise<Product[]> | null = null;

function readProductCache(): Product[] | null {
  try {
    const stored = globalThis.localStorage?.getItem(PRODUCT_CACHE_KEY);
    if (!stored) return null;
    const cache = JSON.parse(stored) as ProductCache;
    if (
      !Array.isArray(cache.products) ||
      typeof cache.cachedAt !== "number" ||
      Date.now() - cache.cachedAt >= PRODUCT_CACHE_TTL_MS
    ) {
      return null;
    }
    return cache.products;
  } catch {
    return null;
  }
}

export function fetchProducts(): Promise<Product[]> {
  const cachedProducts = readProductCache();
  if (cachedProducts) {
    products = cachedProducts;
    return Promise.resolve(cachedProducts);
  }

  if (!productsRequest) {
    productsRequest = fetch(`${API_BASE_URL}/products/`, {
      headers: { Accept: "application/json" },
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`Product request failed with status ${response.status}`);
        }
        const data = (await response.json()) as Product[];
        products = data;
        try {
          globalThis.localStorage?.setItem(
            PRODUCT_CACHE_KEY,
            JSON.stringify({ products: data, cachedAt: Date.now() } satisfies ProductCache),
          );
        } catch {
          // The API response remains usable when browser storage is unavailable.
        }
        return data;
      })
      .finally(() => {
        productsRequest = null;
      });
  }

  return productsRequest;
}
