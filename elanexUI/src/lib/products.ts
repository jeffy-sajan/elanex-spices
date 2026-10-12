import productImage from '@/assets/cardamom-product.jpg';
import heroImage from '@/assets/cardamom-hero.jpg';
import plantImage from '@/assets/cardamom-plant.jpg';
export type Product = { id: string; name: string; description: string; price: number; image: string; category: 'pods' | 'seeds'; badge?: string; grade: string };
export const products: Product[] = [
 { id: 'premium-green-cardamom', name: 'Premium Green Cardamom', description: 'Bold size, rich aroma. Carefully selected for your finest recipes.', price: 1200, image: productImage, category: 'pods', badge: 'BEST SELLER', grade: '8 mm · Premium grade' },
 { id: 'medium-green-cardamom', name: 'Green Cardamom (Medium)', description: 'A beautifully balanced aroma for everyday cooking and chai.', price: 600, image: heroImage, category: 'pods', badge: 'EVERYDAY FAVOURITE', grade: '6–7 mm · Medium grade' },
 { id: 'mixed-size-cardamom', name: 'Cardamom (Mixed Size)', description: 'A natural mix of carefully selected pods, full of authentic flavour.', price: 400, image: productImage, category: 'pods', grade: 'Mixed size · Whole pods' },
 { id: 'cardamom-seeds', name: 'Cardamom Seeds', description: 'Aromatic seeds from green cardamom, for grinding and spice blends.', price: 800, image: plantImage, category: 'seeds', badge: 'FOR SPICE LOVERS', grade: 'Shelled seeds · Culinary use' },
];
export const packs = [100, 250, 500, 1000];
export const money = (amount: number) => '₹' + amount.toLocaleString('en-IN');
export function metadata(title: string, description: string) { return { meta: [{ title: `${title} | Elanex Spices` }, { name: 'description', content: description }, { property: 'og:title', content: `${title} | Elanex Spices` }, { property: 'og:description', content: description }, { property: 'og:type', content: 'website' }, { name: 'twitter:card', content: 'summary_large_image' }] }; }
