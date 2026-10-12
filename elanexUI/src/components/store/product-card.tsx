import { Link } from '@tanstack/react-router';
import { ShoppingCart, Check } from 'lucide-react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { type Product, money } from '@/lib/products';
import { useCart } from '@/lib/cart';
export function ProductCard({product}:{product:Product}) { const {add}=useCart(); const [added,setAdded]=useState(false); return <article className="product-card"><Link to="/products/$productId" params={{productId:product.id}} className="block product-image-wrap"><img className="product-image" src={product.image} alt={product.category==='seeds'?'Cardamom growing at the farm':product.name} width={1024} height={1024} loading="lazy"/>{product.badge&&<span className="product-badge">{product.badge}</span>}</Link><div className="product-body"><h3><Link to="/products/$productId" params={{productId:product.id}}>{product.name}</Link></h3><p>{product.description}</p><div className="product-price">{money(product.price)} <span>/ 100g</span></div><Button onClick={()=>{add(product.id);setAdded(true);setTimeout(()=>setAdded(false),1800)}}>{added?<Check/>:<ShoppingCart/>}{added?'Added to Cart':'Add to Cart'}</Button></div></article>; }
