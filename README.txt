# Harsha Dhore portfolio site

## Pages
- `index.html` — portfolio homepage
- `MBG_index.html` — Pragati / Mahila Bachat Gat case study
- `StrategicUX_index.html` — Food Delivery UX case study
- `MedicalAdher_index.html` — Medical Adherence case study
- `assets/` — images extracted from the original Base64-embedded HTML
- `images/` — project-card thumbnails for the homepage
- `resume/Harsha_Dhore.pdf` — temporary explanatory PDF, not a real resume

## Recommended free hosting: GitHub Pages
This site is about 160 MB unpacked, and some HTML pages are over 10 MB. Netlify's own guidance says drag-and-drop deploys work best under 50 MB and individual files over 10 MB may stall, so a Git-based deployment is more suitable.

1. Install **GitHub Desktop** from https://desktop.github.com/.
2. On GitHub.com, create a new **public** repository, for example `harsha-portfolio`. Leave the options to add a README, license, or `.gitignore` unchecked.
3. In GitHub Desktop, choose **File → Clone Repository** and clone the empty repository you created.
4. Unzip this package. Open the `harsha-portfolio-site` folder inside it and copy its *contents* into the cloned repository folder. Make sure `index.html`, the other three HTML files, `assets/`, `images/`, `resume/`, and `README.txt` are directly inside the cloned repository folder, not nested in another folder.
5. In GitHub Desktop, review the changes, enter a summary such as `Add portfolio site`, click **Commit to main**, then click **Push origin**.
6. On GitHub.com, open your repository and go to **Settings → Pages**.
7. Under Build and deployment, select **Deploy from a branch**, choose branch `main` and folder `/ (root)`, then save.
8. Wait for deployment to finish. Your live site URL will appear in Settings → Pages. The homepage is the root URL; the case studies are at `MBG_index.html`, `StrategicUX_index.html`, and `MedicalAdher_index.html`.
9. For future updates, edit or replace files in the cloned repository folder, then commit and push in GitHub Desktop. GitHub Pages redeploys automatically.

Official guide: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

## Important notes
- Embedded image data was extracted to separate files, and the HTML references were updated to use them.
- The original portfolio references `resume/Harsha_Dhore.pdf`, but no real resume PDF was supplied. The current PDF is an explanatory notice, not a resume. Replace it with your actual CV before publishing.
- External dependencies (Google Fonts, Font Awesome, Tailwind CDN, Google Drive/Sheets resources) still require internet access and may depend on their own sharing permissions.
- The pages were checked for missing local references and missing extracted assets. Preview all four live pages after deployment, especially interactions and external links.
