# Cameron Mitchell — personal website

Static personal and résumé website for https://cameronengineer.com/.

## Preview

```sh
python3 -m http.server 8001 --directory site
```

Open http://localhost:8001. There are no build dependencies or server application.

## Structure

- `site/index.html`: homepage, experience, projects, writing and contact.
- `site/resume/index.html`: full résumé and print layout.
- `site/projects/`: project overview and individual project pages.
- `site/assets/`: shared CSS, small print script, screenshots, favicon and PDF.
- `site/robots.txt` and `site/sitemap.xml`: search discovery.
- `render.yaml`: Render static site configuration.

Edit the HTML and CSS directly. Push to `main` to deploy automatically. The PDF
is a printable snapshot of `/resume/`; regenerate it when changing the résumé.

The public content is a concise professional profile. The original private CV
and interview material are not included in this repository. Certification dates
are presented as dates earned rather than claims about current expiry status.

## Search

Canonical URLs use `https://cameronengineer.com`. The homepage and résumé include
`ProfilePage`, `Person` and `WebSite` structured data with the existing GitHub and
LinkedIn profile URLs. The website links to the separately hosted blog and
Italian flashcards site.

Verify `cameronengineer.com` as a Domain property in Google Search Console and
submit `https://cameronengineer.com/sitemap.xml` after DNS is connected. Update
profile website fields on GitHub and LinkedIn to this domain.
