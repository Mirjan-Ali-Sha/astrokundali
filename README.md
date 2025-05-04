# pyproject.toml
[project]
name = "astrokundali"
version = "0.1.0"
description = "Flexible astrokundali package with Different house calculation methods and interpretation JSONs"
authors = [ { name="Mirjan Ali Sha", email="mastools.help@gmail.com" } ]
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.7"

[project.scripts]
astrokundali = "astrokundali.core:main"

[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"