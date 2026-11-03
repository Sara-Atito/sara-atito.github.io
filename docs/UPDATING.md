# Keep your academic website up to date

Your content lives in **`content/profile.json`**. You can edit it directly on GitHub without installing anything.

1. Open the website repository and select `content/profile.json`.
2. Click the pencil icon to edit.
3. Make the change and click **Commit changes** to save it to `main`.
4. Open **Actions** to check that **Publish academic website** finishes successfully. Then refresh the website.

The website rebuilds from this one file. Avoid editing generated HTML in `site/`, because the next build replaces it.

## Add news

Inside the `news` array, copy an existing entry and place the new one at the top. Replace the example text with your real update:

```json
{
  "period": "2027",
  "title": "A new research update",
  "text": "Write one or two sentences about the publication, talk, award, or project."
}
```

Use the date or academic year you know; do not guess an appointment's exact month. Keep entries in the order you want them displayed, with the newest first.

## Add a publication

Inside `publications`, copy an existing entry and update its details. This is a template, not a real paper:

```json
{
  "year": 2027,
  "venue": "Conference or journal",
  "title": "Your paper title",
  "category": "Vision",
  "role": "Your contribution",
  "summary": "A short, plain-language description of the research.",
  "links": [
    {
      "label": "Paper",
      "url": "https://example.org/replace-with-the-real-paper-link"
    }
  ]
}
```

Use an existing category to keep the publication filters consistent. Add additional link objects for code, a project page, or models. If a paper has no public link yet, use `"links": []`. Keep workshop and main-conference venue names distinct, and identify preprints as preprints.

## Update service, teaching, or your biography

Find the matching section in the JSON file and edit its existing fields. For example, service entries contain the position and its relevant period. Use the latest confirmed role and describe appointments for future conferences clearly.

Your displayed job title uses `person.role_short`. After making an update, change the top-level `updated` date to the date you edited the content, in `YYYY-MM-DD` format.

## JSON editing tips

- Keep double quotes around field names and text.
- Put a comma between entries, but no comma after the last entry in an array or object.
- Use `\"` if you need a quotation mark inside text.
- Do not insert comments into JSON.
- If an edit breaks the build, restore the last working version through the file's history, then try the change again.

For a local check before publishing, run:

```bash
python scripts/build.py
```

## Refresh the separate GitHub profile README

The same build generates `site/profile-README.md`. To update the introduction shown on your GitHub profile, copy this generated file's contents into `README.md` in the separate `Sara-Atito` repository. Website publication does not automatically change that repository.
