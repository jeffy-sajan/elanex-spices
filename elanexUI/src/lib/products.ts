import productImage from '@/assets/cardamom-product.jpg';
import heroImage from '@/assets/cardamom-hero.jpg';
import plantImage from '@/assets/cardamom-plant.jpg';
export type Product = { id: string; name: string; description: string | null; price: number; image: string };
export const demoProducts: Product[] = [
 { id: 'premium-green-cardamom', name: 'Premium Green Cardamom', description: 'Bold size, rich aroma. Carefully selected for your finest recipes.', price: 1200, image: productImage },
 { id: 'medium-green-cardamom', name: 'Green Cardamom (Medium)', description: 'A beautifully balanced aroma for everyday cooking and chai.', price: 600, image: heroImage },
 { id: 'mixed-size-cardamom', name: 'Cardamom (Mixed Size)', description: 'A natural mix of carefully selected pods, full of authentic flavour.', price: 400, image: productImage },
 { id: 'cardamom-seeds', name: 'Cardamom Seeds', description: 'Aromatic seeds from green cardamom, for grinding and spice blends.', price: 800, image: plantImage },
];
export let products: Product[] = demoProducts;
export const packs = [100, 250, 500, 1000];
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
