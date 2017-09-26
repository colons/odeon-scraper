# odeon-scraper

Cinelist, while useful, has [some problems with accuracy][issue]. This project
is an attempt to solve this for a single chain of cinemas, in an extremely
fragile way.

[issue]: https://github.com/seanmtracey/CineList-API/issues/17

## JSON API

You can get responses similar to Cinelist's at URLs structured like the
following:

    https://odeon-scraper.colons.co/odeon/<cinema-id>/`

Replace that `<cinema-id>` with an Odeon cinema ID. Odeon's branch URLs are
structured as `http://www.odeon.co.uk/cinemas/<slug>/<cinema-id>/`. You can
ignore the slug. You should end up with something like
<https://odeon-scraper.colons.co/odeon/104/>.

## Local use

If you're comfortable with Python development, you might want to run the
scraper locally or in part of a project you're working on.

`odeon-scraper` requires Python 3.5 and the contents of `requirements.txt`,
which you can install from an appropriate virtualenv with `pip install -r
requirements.txt` from the root of this repository.

### On the command line

`python scraper.py <cinema-id> --json` will output a list of screenings in JSON
format. Currently, so will `python scraper.py`, but I don't intend for that to
be the case forever, so if you're relying on this behaviour, I encourage you to
use the `--json` flag.

### In your Python project

The `scraper` module contains a function `get_screenings()`, which takes the ID
of the cinema you're interested in as an argument. It also takes a `date`
argument, but it is currently ignored.

## Limitations

Odeon don't list screenings that have already begun, so this project cannot be
used to access anything historical.
