import { defineConfig } from "sanity";
import { structureTool } from "sanity/structure";
import { visionTool } from "@sanity/vision";

import { schemaTypes } from "./schemaTypes";

const projectId = process.env.SANITY_STUDIO_PROJECT_ID;
const dataset = process.env.SANITY_STUDIO_DATASET ?? "production";

if (!projectId) {
  throw new Error(
    "SANITY_STUDIO_PROJECT_ID is required. Add it to elanexCMS/.env before running Sanity Studio.",
  );
}

export default defineConfig({
  name: "elanex-spices",
  title: "Elanex Spices",
  projectId,
  dataset,
  plugins: [structureTool(), visionTool()],
  schema: {
    types: schemaTypes,
  },
});
