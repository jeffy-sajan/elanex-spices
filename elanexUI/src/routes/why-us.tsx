import { createFileRoute } from '@tanstack/react-router';
import { metadata } from '@/lib/products';
import { WhySection, FarmIntro, AromaBanner } from '@/components/store/sections';
export const Route=createFileRoute('/why-us')({head:()=>metadata('Why Choose Elanex Spices','Discover our approach to carefully selected Kerala cardamom, thoughtful packing and natural flavour.'),component:Why});
function Why(){return <><div className="container-site page-heading"><div className="section-kicker">Naturally, Elanex Spices</div><h1>Good Spices. Honest Roots.</h1><p>Close to the farm, careful about quality and passionate about the little things.</p></div><WhySection/><FarmIntro/><AromaBanner/></>;}
