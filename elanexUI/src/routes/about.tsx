import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, CheckCircle2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { AromaBanner } from "@/components/store/sections";
import { metadata } from "@/lib/products";

import farm from "@/assets/kerala-farm.jpg";

const commitments = [
  {
    title: "Quality-conscious sourcing",
    text: "We recognize the importance of product quality, grade and consistency in spice trading.",
  },
  {
    title: "Transparency",
    text: "We aim to communicate product specifications, availability, pricing and order terms clearly.",
  },
  {
    title: "Reliable relationships",
    text: "We value long-term relationships with growers, suppliers and customers built on trust, communication and mutual growth.",
  },
  {
    title: "A customer-first approach",
    text: "We strive to understand each buyer's requirements and provide suitable sourcing solutions.",
  },
];

export const Route = createFileRoute("/about")({
  head: () =>
    metadata(
      "About Elanex Spices",
      "Learn how Elanex Spices connects quality Indian green cardamom with traders, wholesalers and bulk buyers.",
    ),
  component: About,
});

function About() {
  return (
    <>
      <div className="container-site page-section">
        <div className="page-heading">
          <div className="section-kicker">From Grower to Global Market</div>
          <h1>About Elanex Spices</h1>
          <p>
            Connecting India&apos;s spice-growing heritage with the markets that
            value it.
          </p>
        </div>

        <section className="content-split">
          <img
            src={farm}
            alt="Cardamom farm nestled in the green hills of Kerala"
            className="content-image"
            width={1280}
            height={1024}
          />
          <div>
            <h2 className="section-title">From Grower to Global Market</h2>
            <span className="title-rule" />
            <p className="body-copy">
              At <strong>Elanex Spices</strong>, we aim to bridge the gap
              between spice producers and the markets that value their
              products. With a primary focus on Indian green cardamom, our
              vision is to make spice sourcing more accessible, transparent and
              reliable for traders, wholesalers and bulk buyers across India.
            </p>
            <p className="body-copy mt-4">
              We believe successful spice trading begins with understanding the
              product — its quality, grade, origin and value. That is why we
              are building our business around quality-conscious sourcing,
              careful product handling and a customer-focused approach to every
              transaction.
            </p>
          </div>
        </section>

        <section className="content-split mt-16">
          <div>
            <div className="section-kicker">Our Mission</div>
            <h2 className="section-title">
              Making spice procurement simpler and more dependable.
            </h2>
            <span className="title-rule" />
            <p className="body-copy">
              To create a dependable and transparent spice trading platform
              that connects quality spice supplies with the right buyers,
              making procurement simpler and more efficient for businesses of
              every scale.
            </p>
          </div>
          <div>
            <div className="section-kicker">What We Do</div>
            <h2 className="section-title">
              Focused sourcing for every kind of buyer.
            </h2>
            <span className="title-rule" />
            <p className="body-copy">
              Elanex Spices focuses on sourcing green cardamom and supplying
              products to meet the requirements of traders, wholesalers and
              bulk buyers.
            </p>
            <p className="body-copy mt-4">
              Through our digital platform, buyers can explore available
              products, understand their specifications, enquire about
              quantities and connect with us for their sourcing needs.
            </p>
            <p className="body-copy mt-4">
              Whether the requirement is a smaller commercial order or a bulk
              purchase, our aim is to make every interaction straightforward,
              professional and responsive.
            </p>
          </div>
        </section>

        <section className="mt-16">
          <div className="section-heading">
            <div className="section-kicker">Our Commitment</div>
            <h2 className="section-title">Built on quality and trust.</h2>
            <span className="title-rule" />
          </div>
          <div className="why-grid commitment-grid">
            {commitments.map((commitment) => (
              <div key={commitment.title}>
                <div className="why-icon">
                  <CheckCircle2 />
                </div>
                <h3>{commitment.title}</h3>
                <p>{commitment.text}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="content-split mt-16">
          <div>
            <div className="section-kicker">Looking Ahead</div>
            <h2 className="section-title">
              Connecting India&apos;s spice heritage with wider opportunities.
            </h2>
            <span className="title-rule" />
          </div>
          <div>
            <p className="body-copy">
              Beginning with Indian green cardamom, Elanex Spices aspires to
              expand its portfolio to include other spices over time. Our
              vision is to build a trusted spice trading business that connects
              India&apos;s rich spice-growing heritage with wider market
              opportunities.
            </p>
            <p className="body-copy mt-4">
              At Elanex Spices, we believe every successful transaction begins
              with a reliable connection.
            </p>
            <p className="body-copy mt-4 font-semibold">
              Elanex Spices — From Grower to Global Market.
            </p>
            <Button asChild variant="pill" className="mt-6">
              <Link to="/contact">
                Connect with Us <ArrowRight />
              </Link>
            </Button>
          </div>
        </section>
      </div>
      <AromaBanner />
    </>
  );
}
