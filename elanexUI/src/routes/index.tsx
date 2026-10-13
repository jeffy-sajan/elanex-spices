import { createFileRoute } from "@tanstack/react-router";
import { Link } from '@tanstack/react-router';
import { Leaf, Truck, ShieldCheck, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { fetchProducts, metadata, type Product } from '@/lib/products';
import { useEffect, useState } from 'react';
import { ProductCard } from '@/components/store/product-card';
import { FarmIntro, AromaBanner, SectionHeading, ProcessSection, WhySection, CardamomUses } from '@/components/store/sections';
import hero from '@/assets/cardamom-hero.jpg';
export const Route = createFileRoute("/")({
  head: () => metadata('Pure Cardamom from the Hills of Kerala', 'Discover Elanex Spices green cardamom and culinary seeds. Carefully selected in Kerala, full of natural fragrance and flavour.'),
  component: Index,
});
function Index() {
  const [products, setProducts] = useState<Product[]>([]);
  useEffect(() => { fetchProducts().then(setProducts).catch(() => undefined); }, []);
  return (
    <>
      <section className="hero">
        <img src={hero} alt="Fresh green cardamom in a wooden bowl overlooking the misty hills of Kerala" className="hero-photo" width={1920} height={1024} fetchPriority="high" />
        <div className="container-site hero-inner">
          <div className="eyebrow">Naturally grown. Thoughtfully selected.</div>
          <h1>Pure Cardamom<br/>From Our Hills<br/>to Your Home</h1>
          <p className="hero-description">The finest little treasures from the lush hills of Kerala. Carefully cultivated, selected and packed to bring you exceptional freshness and aroma.</p>
          <div className="hero-ctas"><Button asChild variant="pill"><Link to="/products">Explore Products <ArrowRight/></Link></Button><Button asChild variant="heroOutline"><Link to="/about">Our Story <ArrowRight/></Link></Button></div>
          <div className="hero-trust"><div><Leaf/><span>Farm Fresh<br/>Quality</span></div><div><Truck/><span>Trusted<br/>Sourcing</span></div><div><ShieldCheck/><span>Carefully<br/>Selected</span></div></div>
        </div>
      </section>
      <FarmIntro/>
      <section className="products-section"><div className="container-site"><SectionHeading title="Our Cardamom Products" subtitle="A world of aroma, carefully selected for you."/><div className="product-grid">{products.slice(0,3).map(product=><ProductCard key={product.id} product={product}/>)}</div><div className="view-products"><Button asChild variant="outline"><Link to="/products">View All Products <ArrowRight/></Link></Button></div></div></section>
      <AromaBanner/><ProcessSection/><WhySection/><CardamomUses/>
    </>
  );
}
