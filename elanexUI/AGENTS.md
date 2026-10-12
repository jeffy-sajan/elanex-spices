<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->

## Storefront architecture
- Use TanStack Start file-based routes and shared storefront components; the supported platform does not run Next.js or Django.
- Keep the initial catalog and cart client-side with no real order submission or payment collection; production commerce requires a connected service and verified business details.
- Keep product data and cart logic in client-safe shared modules so every shopping page uses the same prices and quantities.
- Render the supplied brand image through the shared storefront Brand component so header and footer stay consistent without recreating its typography.
- Keep homepage editorial sections in shared storefront section components so the route composes the page flow without duplicating presentation.
