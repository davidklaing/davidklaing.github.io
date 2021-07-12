---
layout: page
title: Rmarkdown snippets
permalink: /rmarkdown-snippets/
published: true
publication_date: 2021-07-06
tags: notes,data-science
backlinks: '<ul><li><a id="all-pages-by-date" class="internal-link" href="/all-pages-by-date/">All pages by date</a></li><li><a id="data-science" class="internal-link" href="/data-science/">Pages tagged &#39;data-science&#39;</a></li><li><a id="notes" class="internal-link" href="/notes/">Notes</a></li></ul>'
---

## Render with parameters

First, write parameters in the YAML of the Rmarkdown file. E.g. if you want to parameterize the title of the rendered file, you could do this:

```r
---
output: html_document
params: 
    set_title: "My Title!"
title: "`r params$set_title`"
---
```

Then, from R, run `rmarkdown::render`:

```r
rmarkdown::render(
    "MyDocument.Rmd", 
    params = list(
        set_title = "New Title"
    )
)
```

## Generate markdown text inside a loop

Set code block `results` to `"asis"`, and use `cat` in the loop.

````r
```{r echo = FALSE, results = "asis"}
sections <- c('a', 'b', 'c', 'd')

for (new_section in sections) {
    cat(paste0('\n\n ## New section: ': new_section))
}
```
````

## Render pretty tables in PDF

```r
sample_table %>%
    flextable() %>% 
    autofit() %>% 
    flextable_to_rmd()
```

## Add a line break when rendering to PDF

```r
\newpage
```