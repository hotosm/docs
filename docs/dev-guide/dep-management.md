# Dependency Management

## Javascript

This section will be brief.

Javascript already has a great dependency management ecosystem.

Tools like NPM, Yarn, PNPM all work in a Node environment to
solve dependency version compatibility and install them locally
within your repo, in a `node_modules` directory.

The only recommendation would be to **use PNPM**, as it has a much neater
concept then the other two tools. Dependency locking is fast, and
package installation is _shared_ across repositories using a global
package store on your system.

This sets the standard for dependency management that some Python
tools have attempted to replicate.

## Python

### tl;dr

- Use `pyproject.toml` over `requirements.txt` and separate config files.
- Use PDM to solve the depenedencies for your packages.
- Lock with `>=` for libraries, and `==` for applications.
- Upper bound caping should not be used, e.g. `<=x.x.x`.

### Using pyproject.toml

As per [PEP 621](https://peps.python.org/pep-0621/), most information
about a Python package should live in a file `pyproject.toml` in the
root of your package (often the root of the repo, except in a monorepo setup).

This file contains information on required dependencies (no more
`requirement.txt` files), configuration for build tool, linters, test
suites (pytest), etc.

### Dependency Solvers

[PDM](https://pdm-project.org/latest/) is recommended.

TODO add extra info.

### Locking Dependency Versions

Generally it is good practice to pin the version of an underlying
dependency you use in your code. This helps to prevent future breakage.

However, there is an important distinction between two types of package:

- Libraries: An underlying Python module that is used _within_ another tool.
- Applications: A software tool. Typically not installable.
  Such as HOT's web APIs that underpin it's tools
  (raw-data-api, TM, FMTM, etc).

> Capping **upper limits** for library dependencies has long term negative
> effects, and should never be taken lightly.

#### Locking for Applications

An application would sit at the highest level in the chain of installed
dependencies: it uses underlying libraries/packages, but is not installed itself.

There are three main options for pinning.

##### Specific Versions 👍

```bash
pip install mydep==1.0.4
```

**This is generally the recommended approach for reproducable environments.**

##### Approximate Versions

```bash
pip install mydep~=1.0.4
```

This will install >1.0.4, but not increment the minor version.

So the maximum installable version here would be 1.0.11, if this is
the last version before the 1.2.x minor increment.

This is an acceptable approach for some dependencies, but generally not
recommended, as SEMVER is no guarantee of avoiding breakage (definitions are
quite subjective, so patch versions can sometimes also introduce breakage).

##### Minimum Versions

```bash
pip install mydep>=1.0.4
```

This will install any version **greater** than that specified.

This means breaking changes may be introduced if v2.0.0 is released.

This is not recommended for applications, as installing one day may work,
then break the next day due a dependency update.

#### Locking for Packages

Sometimes we develop a package that is used as a dependency in other
tools.

Examples would be:

- [osm-login-python](https://github.com/hotosm/osm-login-python)
- [osm-fieldwork](https://github.com/hotosm/osm-fieldwork)
- [osm-rawdata](https://github.com/hotosm/osm-rawdata)
- [fmtm-splitter](https://github.com/hotosm/fmtm-splitter)

In these cases, the packages requires underlying dependencies to function.

The packages should **never** have pinned dependencies to a specific version.

**It is recommended that versions should be pinned in an open ended way, using
greater than or equal too (>=)**.

> For this to work, a minimum required version of a dependency should
> be established. There is little point pinning >= if a very up to
> date version of a dependency is used (forcing the installer to update
> to a very recent version).

This ensures that a minimum version of the dependency is used, but does not
prevent dependency upgrades for those using the package.

Using approximate pinning (~=) may also be possible, however, this assumes
too much about future compatibility, which is something that is difficult to
predict.

For longevity, it is best to provide the most flexible option for dependency
solvers: **>=**.

> Only add a cap if a dependency is known to be incompatible or there is
> a high (>75%) chance of it being incompatible in its next release.
> An example of a library that should probably be capped is GDAL.

Some more in depth technical reading can be found
[here](https://iscinumpy.dev/post/bound-version-constraints/#tldr).
