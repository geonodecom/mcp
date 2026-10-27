# Contributing

Use Python 3.10 or newer. There are no development dependencies for the discovery tests.

```sh
python3 -m unittest discover -s tests -v
python3 -m py_compile examples/discover.py
python3 examples/discover.py
```

These commands make no network requests. The final command prints a plan; `--connect` explicitly enables anonymous metadata discovery. Never add extraction, authenticated requests or tool invocation to an automatic test. Test new protocol behavior with fixtures and distinguish local checks from a production run.

Branch from `main`. Keep example protocol behavior narrow and describe limitations. Check current Geonode documentation before changing endpoint/authentication instructions. No server deployment, registry publication or release process is configured here; read [the boundary](docs/source-and-releases.md).

For API/account problems, [contact Geonode](https://geonode.com/contact). For vulnerabilities, use [SECURITY.md](SECURITY.md). Contributions use [MIT](LICENSE).
