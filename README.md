### Installation
https://docs.getpelican.com/en/latest/install.html
```
python -m pip install "pelican[markdown]"
```

- Themes:
```
# git clone https://github.com/Pelican-Elegant/elegant.git themes/elegant
git submodule init
git submodule update
```

### Run
```
pelican content && pelican --listen
```