import { createFileRoute } from '@tanstack/react-router';
import { metadata } from '@/lib/products';
import { FAQList } from '@/components/store/sections';
export const Route=createFileRoute('/faq')({head:()=>metadata('Frequently Asked Questions','Find answers about Elanex Spices products, quality, storage and sourcing enquiries.'),component:FAQ});
function FAQ(){return <div className="container-site page-section"><div className="page-heading"><div className="section-kicker">A few helpful answers</div><h1>Frequently Asked Questions</h1><p>Learn more about our products, quality and sourcing approach.</p></div><div className="max-w-3xl"><FAQList/></div></div>;}
