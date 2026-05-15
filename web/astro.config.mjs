import { defineConfig } from 'astro/config';

// If deploying to a project page (user.github.io/repo), set `base` to "/repo".
// For a custom CNAME (apex/subdomain), leave base empty.
export default defineConfig({
  output: 'static',
  trailingSlash: 'ignore',
  devToolbar: { enabled: false },
});
