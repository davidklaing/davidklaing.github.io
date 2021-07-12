---
layout: page
title: Git snippets
permalink: /git-snippets/
published: true
publication_date: 2021-07-07
tags: notes,data-science
backlinks: '<ul><li><a id="all-pages-by-date" class="internal-link" href="/all-pages-by-date/">All pages by date</a></li><li><a id="data-science" class="internal-link" href="/data-science/">Pages tagged &#39;data-science&#39;</a></li><li><a id="notes" class="internal-link" href="/notes/">Notes</a></li></ul>'
---

## Remove uncommitted files from staging area

```bash
git reset HEAD -- .
```

## Check out a remote branch

```bash
git checkout origin/{branch_name}
```