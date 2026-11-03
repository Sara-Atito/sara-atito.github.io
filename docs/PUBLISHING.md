# Publish on GitHub Pages

These instructions assume you want to publish with your existing **Sara-Atito** account. No GitHub repository or deployment has been created by this package.

## Publish the website

1. Sign in at [GitHub](https://github.com/).
2. Create a new **public** repository named exactly `sara-atito.github.io`, with `main` as the default branch. If a repository with that name already exists, review its contents before adding these files; do not overwrite an existing website without checking.
3. Extract the ZIP package on your computer. Upload the **contents** of the `sara-academic` folder to the repository root. `README.md`, `content`, `scripts`, `assets`, and `templates` must appear directly at the top level, rather than inside an extra `sara-academic` folder.
4. Make sure `.github/workflows/pages.yml` is uploaded too. File managers may hide folders beginning with a dot. If the browser upload omits it, use **Add file → Create new file**, enter `.github/workflows/pages.yml` as the filename, and paste the workflow from this package.
5. Open the repository's **Settings → Pages**. Under **Build and deployment → Source**, choose **GitHub Actions**.
6. Open **Actions → Publish academic website → Run workflow**, select `main`, and run it. A new commit to `main` also starts publication automatically.
7. Wait for the workflow to finish successfully. Its deployment link is the authoritative website address. For this repository name it should be [https://sara-atito.github.io/](https://sara-atito.github.io/).

The workflow builds only the website into `site/` and deploys that folder. It requires no personal access token or paid hosting service. A public repository makes its source files visible too, so keep its content suitable for public sharing.

## If your repository is named Sara-Atito

That name also works for the website. It creates a project site at `https://sara-atito.github.io/Sara-Atito/`, rather than the shorter main-site address above. Use the same files and GitHub Actions setup; the site's relative asset links support either location. Set `person.website` in `content/profile.json` to the project-site address if you choose this option.

A public repository named `Sara-Atito` also supplies your GitHub profile README. To show your academic introduction on your profile, use the generated `site/profile-README.md` as its root `README.md` instead of the website's setup guide. Keep the publishing and editing guides in `docs/`.

## Add the GitHub profile README

This optional step adds an introduction to the top of [your GitHub profile](https://github.com/Sara-Atito), in addition to the website.

1. Create a separate public repository named exactly `Sara-Atito`. If it already exists, preserve any existing README material you want to keep.
2. Create or edit its root `README.md`.
3. Copy in the contents of the generated `site/profile-README.md` from this package.
4. Commit the change. The README appears on the profile page.

To refresh it later, rebuild the website and copy the new `profile-README.md` contents. Once the website is live, the generated Markdown is also available at `https://sara-atito.github.io/profile-README.md`.

## If publication fails

- **Pages is not configured:** confirm that Settings → Pages → Source is set to GitHub Actions, then rerun the workflow.
- **Build fails after a content edit:** open the failed build log. A missing comma, quote, or bracket in `content/profile.json` is a common cause. Use the file's history to restore the previous version if needed.
- **Workflow is missing:** check that `.github/workflows/pages.yml` is present in the repository root, not nested in another folder.
- **No run after a commit:** check that the commit was made to `main`. The workflow deliberately deploys only that branch.
- **A page is still old:** wait for the new workflow to finish, then refresh the browser.

GitHub's official guides: [Custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme).
