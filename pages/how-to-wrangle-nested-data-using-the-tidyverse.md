---
layout: page
title: How to wrangle nested data using the tidyverse
permalink: /how-to-wrangle-nested-data-using-the-tidyverse/
published: true
last_updated: 2019-02-25
backlinks: <ul><li><a id="how-tos" class="internal-link" href="/how-tos/">How-tos</a></li></ul>
tooltips: 
- path: tooltip_how-tos.js
---

Most of my R training involved operations on dataframes, usually with `dplyr` functions like `filter`, `select`, `mutate`, `group_by`, and `summarize`. These are wonderful tools that I use every day. However, there is a second set of tools that have become equally important in my day-to-day data manipulation work in R: those for working with lists.

You may have been told on your first day learning R that a list is a special type of vector that can contain elements of different types, including lists. If you're like me, you promptly forgot this fact, and spent the next year working with deliciously rectangular dataframes. But if you spend enough time working with data, it eventually becomes clear that most data isn't born as a tidy CSV. Instead, it's usually stored in a nested structure such as JSON or XML. That's why lists are so useful in R. They are the most natural data type for representing a nested structure.

If `filter`, `select`, `mutate`, `group_by`, and `summarize` form my basic vocabulary for working with rectangular data, then `stringr::str_detect`, `jsonlite::fromJSON`, `magrittr::extract2`, and `purrr::map` form my basic vocabulary for working with nested data.

Say you're working with telemetry data from a website. Your raw data probably comes out of a database looking something like this:

``` r
library(tidyverse)
library(magrittr)
library(jsonlite)
library(knitr)

user_actions <- tibble(
  user = c("david", "david", "david", "david", "david", "david"),
  action = c(
    '{"Type": "Login", "UtcTimestamp": "2019-03-05 12:30:41", "user": "david"}',
    '{"Type": "ButtonPress", "UtcTimestamp": "2019-03-05 12:30:43", "ButtonID": "2kdkkdfl-jnsdol32", "ButtonName": "Settings"}',
    '{"Type": "ToggleCheckbox", "UtcTimestamp": "2019-03-05 12:30:44", "CheckboxID": "5d2ddnn8-polen2e7", "CheckboxName": "Subscribe to email newsletter", "CheckboxStatus": "FALSE"}',
    '{"Type": "ToggleCheckbox", "UtcTimestamp": "2019-03-05 12:30:45", "CheckboxID": "jjdfj133-883jdnb3", "CheckboxName": "Desktop notifications", "CheckboxStatus": "FALSE"}',
    '{"Type": "ButtonPress", "UtcTimestamp": "2019-03-05 12:30:50", "ButtonID": "lop29cdk-4jns910d", "ButtonName": "Home"}',
    '{"Type": "FollowLink", "UtcTimestamp": "2019-03-05 12:30:59", "URL": "https://www.theglobeandmail.com/"}'
  )
)
user_actions %>% kable()
```

| user  | action                                                                                                                                                                           |
|:------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| david | {"Type": "Login", "UtcTimestamp": "2019-03-05 12:30:41", "user": "david"}                                                                                                        |
| david | {"Type": "ButtonPress", "UtcTimestamp": "2019-03-05 12:30:43", "ButtonID": "2kdkkdfl-jnsdol32", "ButtonName": "Settings"}                                                        |
| david | {"Type": "ToggleCheckbox", "UtcTimestamp": "2019-03-05 12:30:44", "CheckboxID": "5d2ddnn8-polen2e7", "CheckboxName": "Subscribe to email newsletter", "CheckboxStatus": "FALSE"} |
| david | {"Type": "ToggleCheckbox", "UtcTimestamp": "2019-03-05 12:30:45", "CheckboxID": "jjdfj133-883jdnb3", "CheckboxName": "Desktop notifications", "CheckboxStatus": "FALSE"}         |
| david | {"Type": "ButtonPress", "UtcTimestamp": "2019-03-05 12:30:50", "ButtonID": "lop29cdk-4jns910d", "ButtonName": "Home"}                                                            |
| david | {"Type": "FollowLink", "UtcTimestamp": "2019-03-05 12:30:59", "URL": "<https://www.theglobeandmail.com/>"}                                                                       |

Each logged event is a JSON string containing properties of the event. In my experience, the most common tasks for converting these nested structures into more legible rectangular structures are these:

## 1. Finding all events of a particular type.


Assuming that event types can be identified by the presence or absence of specific strings in the JSON, you can use `filter` along with `stringr::str_detect` to keep all rows of your events dataframe where the `action` string contains a pattern of interest. For example, say you want get all the `ToggleCheckbox` events.

``` r
user_actions %>% 
  filter(str_detect(action, "ToggleCheckbox")) %>% 
  kable()
```

| user  | action                                                                                                                                                                           |
|:------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| david | {"Type": "ToggleCheckbox", "UtcTimestamp": "2019-03-05 12:30:44", "CheckboxID": "5d2ddnn8-polen2e7", "CheckboxName": "Subscribe to email newsletter", "CheckboxStatus": "FALSE"} |
| david | {"Type": "ToggleCheckbox", "UtcTimestamp": "2019-03-05 12:30:45", "CheckboxID": "jjdfj133-883jdnb3", "CheckboxName": "Desktop notifications", "CheckboxStatus": "FALSE"}         |

## 2. Extracting one or more properties from an event.

To extract a property from an event, you need to convert the event to a list and then index it. Let's take the first `ToggleCheckbox` event as an example.

``` r
(first_toggle_checkbox_event <- user_actions %>% 
  filter(str_detect(action, "ToggleCheckbox")) %>% 
  slice(1) %>% 
  pull())
```

    ## [1] "{\"Type\": \"ToggleCheckbox\", \"UtcTimestamp\": \"2019-03-05 12:30:44\", \"CheckboxID\": \"5d2ddnn8-polen2e7\", \"CheckboxName\": \"Subscribe to email newsletter\", \"CheckboxStatus\": \"FALSE\"}"

We'll use `jsonlite::fromJSON` to convert this string to a list, and then we'll use `magrittr::extract2` to retrieve the `CheckboxName` property.

``` r
first_toggle_checkbox_event %>% 
  fromJSON() %>% 
  extract2("CheckboxName")
```

    ## [1] "Subscribe to email newsletter"

If you've never seen `extract2` before, it does the exact same thing as double square brackets, except that it takes the list as its first argument. This makes it very easy to use inside a chain of piped commands. (By contrast, `extract` does the same thing as single square brackets — usually not quite as useful.)

An alternative option is to use `%$%` — a `magrittr` infix function designed to work just like the standard pipe (`%>%`) — except that the second argument is the name of the element to extract. For example, the code below is equivalent to the code above.

``` r
first_toggle_checkbox_event %>% 
  fromJSON() %$%
  CheckboxName
```

    ## [1] "Subscribe to email newsletter"

I prefer `extract2` because it feels a bit more explicit, but the second option is arguably more readable.

## 3. Operating on multiple events simultaneously.

Lastly, you might wish to write an extraction function and map it across all events, regardless of their type. For this, you'll want to pass `purrr::map` into `mutate`. For example, say we want to extract the timestamp from all events. We would start by writing a function to extract the `UtcTimestamp` field from a given event.

``` r
extract_utc_timestamp <- function(event) {
  event %>% 
    fromJSON() %>% 
    extract2("UtcTimestamp")
}
```

Our next step is to map this function across the values of the `action` column in our dataframe. You might wonder why it's not possible to do the following:

``` r
user_actions %>% 
  mutate(utc_timestamp = extract_utc_timestamp(action))
```

    ## Error in mutate_impl(.data, dots): Evaluation error: parse error: trailing garbage
    ##            12:30:41", "user": "david"} {"Type": "ButtonPress", "UtcTim
    ##                      (right here) ------^
    ## .

The reason is that our function, `extract_utc_timestamp`, expects `event` to be a character vector of length 1. But `mutate` is passing in the entire character vector that is the `action` column. Unlike `sum` or `mean`, which can be passed into `mutate` with no issues, our function takes a single input and gives a single output.

If we want to apply this function across the whole set of values in the `action` column, we'll need `map`, which does just that: it applies a function across a set of values and returns the resulting set of values. Now, `map` has a few variants depending on the desired class of the output; the default just returns a list. But in this case we want a character vector, so we'll use `map_chr`.

``` r
user_actions %>% 
  mutate(
    user_actions = map_chr(
      .x = action,
      .f = extract_utc_timestamp
    )
  ) %>% 
  kable()
```

| user  | action                                                                                                                                                                           | user\_actions       |
|:------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------|
| david | {"Type": "Login", "UtcTimestamp": "2019-03-05 12:30:41", "user": "david"}                                                                                                        | 2019-03-05 12:30:41 |
| david | {"Type": "ButtonPress", "UtcTimestamp": "2019-03-05 12:30:43", "ButtonID": "2kdkkdfl-jnsdol32", "ButtonName": "Settings"}                                                        | 2019-03-05 12:30:43 |
| david | {"Type": "ToggleCheckbox", "UtcTimestamp": "2019-03-05 12:30:44", "CheckboxID": "5d2ddnn8-polen2e7", "CheckboxName": "Subscribe to email newsletter", "CheckboxStatus": "FALSE"} | 2019-03-05 12:30:44 |
| david | {"Type": "ToggleCheckbox", "UtcTimestamp": "2019-03-05 12:30:45", "CheckboxID": "jjdfj133-883jdnb3", "CheckboxName": "Desktop notifications", "CheckboxStatus": "FALSE"}         | 2019-03-05 12:30:45 |
| david | {"Type": "ButtonPress", "UtcTimestamp": "2019-03-05 12:30:50", "ButtonID": "lop29cdk-4jns910d", "ButtonName": "Home"}                                                            | 2019-03-05 12:30:50 |
| david | {"Type": "FollowLink", "UtcTimestamp": "2019-03-05 12:30:59", "URL": "<https://www.theglobeandmail.com/>"}                                                                       | 2019-03-05 12:30:59 |

There you have it! With these four functions — `str_detect`, `fromJSON`, `extract2`, and `map` — you can perform all sorts of operations on large sets of nested data.
