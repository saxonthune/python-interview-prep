import { defineConfig } from 'astro/config';

// Deployed to a GitHub Pages project page at saxonthune.github.io/python-interview-prep.
// For a custom CNAME (apex/subdomain), drop `base` and adjust `site`.
export default defineConfig({
  site: 'https://saxonthune.github.io',
  base: '/python-interview-prep',
  output: 'static',
  trailingSlash: 'ignore',
  devToolbar: { enabled: false },
});
