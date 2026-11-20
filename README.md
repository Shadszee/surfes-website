# SURFES website

Static website for SURFES silica-free solid surfaces and MDF routed doors, made in Australia by Craftmark.
Rebuilt from the old Craftmark Surfaces Webflow site (surfaces.craftmark.com.au) in November 2026.

## How it is put together

| Folder | What is in it |
| --- | --- |
| `build/products.json` | Every surface colour and door profile: names, descriptions, specs and image file names. **Edit this to change products.** |
| `build/site.py` | Generates every HTML page from `products.json`. Contact details are set at the top of this file. |
| `site/` | The finished website. This is the folder that gets hosted. |
| `site/css/site.css` | All styling (SURFES colours: Warm White #F7F5EF, Stone #C9BEA8, Clay #B5623B, Black #181816; font: Roboto Condensed). |
| `site/images/` | Every image the site uses. |
| `site/_redirects` | Sends old Webflow addresses to the new pages. |
| `archive/` | Full text backup of the old Webflow site and images it no longer uses. |

## Making changes

1. Edit `build/products.json` (or the page text in `build/site.py`).
2. Run `python3 build/site.py` (needs Python 3, nothing else to install).
3. Commit and push. Cloudflare Pages rebuilds the live site automatically.

To add a colour: copy an existing entry in `surfaces`, change the name, slug, description, `tone` line and image names, and put the images in `site/images/`.
To hide a colour without deleting it: set `"discontinued": true`.

To preview on your own computer by double-clicking files, build with `PRETTY=0 python3 build/site.py` (links then point at `index.html` files directly). Build without it before pushing.

## Hosting on Cloudflare Pages

- Framework preset: None
- Build command: `python3 build/site.py`
- Build output directory: `site`
- Custom domain: add it under the Pages project, then point the domain's DNS at Cloudflare as instructed.

## Before launch

- [ ] Replace placeholder email, address and Facebook/Instagram links at the top of `build/site.py`
- [ ] Pietra Urbana needs a swatch photo (old site was showing the Bruma Vagli image)
- [ ] Confirm the Bilpin 40 profile (currently "40mm spaced V grooves", marked to be confirmed)
- [ ] Confirm the Wentworth spec ("225 degree", probably 22.5)
- [ ] Confirm the spelling "Grigio Pallazzo"
- [ ] Rewrite the colour descriptions in the SURFES voice (old copy still uses "luxurious" and similar)
- [ ] Build the Trade, About, News and Contact pages (currently placeholders)
- [ ] Decide the final domain and whether the doors sit under SURFES or Craftmark
