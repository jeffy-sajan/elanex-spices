export type Product = { id: string; name: string; description: string | null; price: number; image: string; category: 'cardamom' | 'seeds' };
export let products: Product[] = [];
export const money = (amount: number) => '₹' + amount.toLocaleString('en-IN');
export function metadata(title: string, description: string) { return { meta: [{ title: `${title} | Elanex Spices` }, { name: 'description', content: description }, { property: 'og:title', content: `${title} | Elanex Spices` }, { property: 'og:description', content: description }, { property: 'og:type', content: 'website' }, { name: 'twitter:card', content: 'summary_large_image' }] }; }

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api";

export async function fetchProducts(): Promise<Product[]> {
  const response = await fetch(`${API_BASE_URL}/products/`, {
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new Error(`Product request failed with status ${response.status}`);
  }
  const data = (await response.json()) as Product[];
  products = data;
  return data;
}
