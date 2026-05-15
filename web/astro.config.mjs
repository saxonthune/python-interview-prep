import { defineConfig } from 'astro/config';

// Deployed to Cloudflare Pages at the custom domain pythoning.saxon.zone,
// served from the root path (no base prefix).
export default defineConfig({
  site: 'https://pythoning.saxon.zone',
  output: 'static',
  trailingSlash: 'ignore',
  devToolbar: { enabled: false },
});
