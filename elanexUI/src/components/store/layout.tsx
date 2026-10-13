import { Link, useRouterState } from '@tanstack/react-router';
import { useState } from 'react';
import { Menu, X, MapPin, Phone, Mail, ArrowUpRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { BackendStatus } from '@/components/backend-status';
export function Brand() { return <Link to="/" className="brand" aria-label="Elanex Spices home"><img src="/elanex-logo.png" alt="Elanex Spices — From Grower to Global Market" className="brand-logo"/></Link>; }
export function Header() {
 const [open,setOpen] = useState(false);
 const pathname = useRouterState({ select: s => s.location.pathname });
 const overlay = pathname === '/';
 return <header className={`site-header ${overlay ? 'is-overlay' : ''}`}><div className="container-site header-inner"><Brand/><nav className={`main-nav ${open ? 'is-open' : ''}`} aria-label="Main navigation" onClick={() => setOpen(false)}><Link to="/" activeOptions={{exact:true}}>Home</Link><Link to="/about">About</Link><Link to="/products">Products</Link><Link to="/our-process">Our Process</Link><Link to="/why-us">Why Us</Link><Link to="/contact">Contact</Link></nav><div className="header-actions"><Button variant="pill" asChild className="header-order" size="sm"><Link to="/contact">Enquire <ArrowUpRight size={12}/></Link></Button><Button variant="ghost" size="icon" className="mobile-menu-button" onClick={()=>setOpen(!open)} aria-label={open?'Close menu':'Open menu'} aria-expanded={open}>{open?<X/>:<Menu/>}</Button></div></div></header>;
}
export function Footer() { return <footer className="footer"><div className="container-site"><div className="footer-grid"><div className="footer-brand"><Brand/><p>From the green hills of Kerala to your home. Cardamom with a story, and an aroma to remember.</p></div><div className="footer-contact"><h4>Contact Elanex Spices</h4><div className="footer-links"><span className="contact-address"><MapPin size={13}/><span><strong>ELANEX SPICES</strong><br/>V.P VII/204<br/>Kochara P.O<br/>Vandanmedu<br/>685551</span></span><a href="tel:+918921263343" className="flex items-center gap-2"><Phone size={13}/> +91 8921263343</a><a href="mailto:elanexspices@gmail.com" className="flex items-center gap-2"><Mail size={13}/> elanexspices@gmail.com</a><span className="contact-gstin">GSTIN: 32SZMPS4547B1ZV</span></div></div></div><div className="footer-bottom"><span>© {new Date().getFullYear()} Elanex Spices. All rights reserved.</span><div className="flex gap-5"><span>From Grower to Global Market</span><BackendStatus /></div></div></div></footer>; }
