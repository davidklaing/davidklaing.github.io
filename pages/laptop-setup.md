---
layout: page
title: My laptop setup
permalink: /laptop-setup/
published: true
publication_date: 2018-10-01
last_updated: 2020-12-15
tags: notes,data-science
backlinks: '<ul><li><a id="all-pages-by-date" class="internal-link" href="/all-pages-by-date/">All pages by date</a></li><li><a id="data-science" class="internal-link" href="/data-science/">Data science</a></li><li><a id="notes" class="internal-link" href="/notes/">Notes</a></li></ul>'
---

After setting myself up on four laptops in the space of two years, I figured it was time to write this all down. [Mike Gelbart's setup](https://github.com/mgelbart/misc/blob/master/laptop_setup.md) has been useful to me, so maybe mine will be useful to you.

## macOS preferences

1. Enable tap to click.
  - `System Preferences` → `Trackpad`
  - Check `Tap to click`
2. Set mouse speed to maximum.
  - `System Preferences` → `Trackpad`
  - Set `Tracking Speed` to `Fast`
3. Enable 3-finger drag.
  - `System Preferences` → `Trackpad` → `Accessibility`→ `Mouse & Trackpad` → `Trackpad Options` 
  - Check `Enable dragging` with `three finger drag`
4. Configure hot corners. 
  - `System Preferences` → `Mission Control` → `Hot Corners`
  - Top left: `Desktop`
  - Top right: `Mission Control`
  - Bottom left: `Put Display to Sleep`
  - Bottom right: `Launchpad`
5. Turn on Night Shift.
   - `System Preferences` → `Displays` → `Night Shift`
   - Set schedule to `Sunset to Sunrise`
6. Reduce motion.
  - `System Preferences` → `Accessibility` → `Display`
  - Check `Reduce motion`

## Installations

1. developer tools: `xcode-select --install`
2. [1Password](https://1password.com/)
3. [Chrome](https://www.google.ca/chrome/?brand=CHBD&gclid=Cj0KCQiAgMPgBRDDARIsAOh3uyLH9FyD5U6BuJ2Co_vlFaAEiDZYtHyFz2Wf-ESUYLTFpSxdpRLTXgQaAvyDEALw_wcB&gclsrc=aw.ds)
4. [iTerm2](https://www.iterm2.com/)
5. [Homebrew](https://brew.sh/)
6. [R](https://cran.rstudio.com/bin/macosx/)
7. [RStudio](https://www.rstudio.com/products/rstudio/download/)
8. [Anaconda](https://www.anaconda.com/download/#macos)
9. [Visual Studio Code](https://code.visualstudio.com/)
10. [Spotify](https://www.spotify.com/ca-en/download/other/)
11. [BetterSnapTool](https://folivora.ai/bettersnaptool)

## iTerm2 configurations

1. Set the default typing style  to Natural:
	- `Preferences` → `Profiles` → `Keys`
	- Set `Load preset` to `Natural Text Editing`
2. Set new windows/tabs to open from previous session's directory:
	- `Preferences` → `Profiles` → `General`

## Bash aliases

Put the following in `.zshenv`:

```zsh
alias rst="open -a rstudio"
alias vs="open -a visual\ studio\ code"
alias prev="open -a preview"
alias cdpr="cd ~/Documents/projects"
alias cdar="cd ~/Documents/areas"
alias cdre="cd ~/Documents/resources"
```

## SSH

[Instructions](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)

## Git 

### Configure my user.

```zsh
git config --global user.name "David Laing"
git config --global user.email davidkendalllaing@gmail.com
```

### Create a global gitignore file.

`touch ~/.gitignore_global`

Put this in it:

```zsh
.DS_Store
.ipynb_checkpoints
.Trashes
.RHistory
.RData
__pycache__
```

```zsh
git config --global core.excludesfile ~/.gitignore_global
```

### Set up git aliases.

```zsh
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```

### Set up tab completion for git branches.

```zsh
curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.zsh -o ~/.git-completion.zsh
```

Add this to `.zshenv`:

```zsh
if [ -f ~/.git-completion.zsh ]; then
  . ~/.git-completion.zsh
fi
```

Run `chmod -X ~/.git-completion.zsh`, and restart iTerm2.

## RStudio configurations

### Change the default RStudio pane layout.

- `Preferences` → `Pane Layout`
- Top left: `Source`
- Top right: `Console`
- Bottom left: `History`
- Bottom right: everything else

### Add a margin line.

- `Preferences` → `Code` → `Display`
- Check `Show margin`

### Remove the default to save `.RData`.

- `Preferences` → `General`
- Uncheck `Restore .RData into workspace at startup`
- Change `Save workspace to .RData on exit` to `Never`

### Set up keyboard shortcuts.

- `Preferences` → `Code` → `Editing` → `Modify Keyboard Shortcuts`
- Open Previous Tab: `Alt+Cmd+Left`
- Open Next Tab: `Alt+Cmd+Right`

### Create custom snippets.

- `Preferences` → `Code` → `Edit Snippets`
- Add these:

```R
snippet pview
	{View(.); .}

snippet pprint
	{print(.); .}
```

## Jekyll

### [Install rbenv](https://jekyllrb.com/docs/installation/macos/) 

(So you don't have to alter the version of Ruby that comes with Mac.)

```zsh
# Install rbenv and ruby-build
brew install rbenv

# Setup rbenv integration to your shell
rbenv init

# Check your install
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/master/bin/rbenv-doctor | bash

# Install a new version of Ruby
rbenv install 2.5.3
rbenv global 2.5.3
ruby -v
```

### Install Jekyll

[This post was useful](http://kbroman.org/simple_site/pages/local_test.html), as was [this issue comment](https://github.com/bundler/bundler/issues/1767#issuecomment-4787059).

```zsh
gem install bundler
bundle install
```

To build a site:

```zsh
bundle exec jekyll build
```

To test it locally:

```zsh
bundle exec jekyll serve
```