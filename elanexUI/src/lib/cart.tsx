import { createContext, useContext, useState, type ReactNode } from 'react';
import { products } from './products';
export type CartItem = { productId: string; grams: number; quantity: number };
type CartValue = { items: CartItem[]; add: (id: string, grams?: number, quantity?: number) => void; update: (id: string, grams: number, quantity: number) => void; remove: (id: string, grams: number) => void; count: number; subtotal: number };
const CartContext = createContext<CartValue | null>(null);
export function CartProvider({ children }: { children: ReactNode }) {
 const [items, setItems] = useState<CartItem[]>([]);
 const add = (productId: string, grams = 100, quantity = 1) => setItems(previous => { const existing = previous.find(i => i.productId === productId && i.grams === grams); return existing ? previous.map(i => i === existing ? { ...i, quantity: Math.min(99, i.quantity + quantity) } : i) : [...previous, { productId, grams, quantity }]; });
 const update = (id: string, grams: number, quantity: number) => setItems(previous => previous.map(i => i.productId === id && i.grams === grams ? { ...i, quantity: Math.max(1, Math.min(99, quantity)) } : i));
 const remove = (id: string, grams: number) => setItems(previous => previous.filter(i => !(i.productId === id && i.grams === grams)));
 const count = items.reduce((sum, i) => sum + i.quantity, 0);
 const subtotal = items.reduce((sum, i) => sum + (products.find(p => p.id === i.productId)?.price ?? 0) * i.grams / 100 * i.quantity, 0);
 return <CartContext.Provider value={{ items, add, update, remove, count, subtotal }}>{children}</CartContext.Provider>;
}
export function useCart() { const cart = useContext(CartContext); if (!cart) throw new Error('Cart provider is required'); return cart; }
