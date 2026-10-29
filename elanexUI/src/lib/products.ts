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
let productsRequest: Promise<Product[]> | null = null;

export function fetchProducts(): Promise<Product[]> {
  if (!productsRequest) {
    productsRequest = fetch(`${API_BASE_URL}/products/`, {
      headers: { Accept: "application/json" },
      cache: "no-store",
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`Product request failed with status ${response.status}`);
        }
        const data = (await response.json()) as Product[];
        products = data;
        return data;
      })
      .finally(() => {
        productsRequest = null;
      });
  }

  return productsRequest;
}
