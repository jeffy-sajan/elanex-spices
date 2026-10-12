import { createFileRoute } from '@tanstack/react-router';
import { metadata } from '@/lib/products';
import { FAQList } from '@/components/store/sections';
export const Route=createFileRoute('/faq')({head:()=>metadata('Frequently Asked Questions','Find answers about Elanex Spices cardamom pack sizes, storage, quality and wholesale enquiries.'),component:FAQ});
function FAQ(){return <div className="container-site page-section"><div className="page-heading"><div className="section-kicker">A few helpful answers</div><h1>Frequently Asked Questions</h1><p>Everything from choosing a pack to keeping your cardamom fresh.</p></div><div className="max-w-3xl"><FAQList/></div></div>;}
