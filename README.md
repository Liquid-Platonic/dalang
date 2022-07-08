# Installation

If you're working under **M1** processor, have a look at the next section.

First, clone this repository:
```bash
git clone https://github.com/Liquid-Platonic/music-orchistrator.git
```

Install python 3.8.13 if you do not have it already(via pyenv or directly):
```shell
pyenv install 3.8.13
```

Then, install poetry via:
```bash
pip install poetry
```
Finally install dependencies via:
```shell
make install
```

## M1 processors & conda

Activate your environment, and before installing the dependencies run:
```shell
poetry config virtualenvs.path <conda-installation-path>
```

### HuggingFace Transformers for Text Emotion Recognition

You have to compile `transformers` from source using Rust. Please follow run the following commands:

- `curl https://sh.rustup.rs -sSf | sh -s -- --no-modify-path`
- `git clone https://github.com/huggingface/tokenizers`
- `pip install setuptools_rust`
- `cd tokenizers/bindings/python && python setup.py install`
- `pip install torch==1.11.0 torchaudio==0.11.0`

You can find more info here: https://towardsdatascience.com/hugging-face-transformers-on-apple-m1-26f0705874d7.

### Speechbrain for Speech Emotion Recognition

`conda install scipy==1.6.1` `conda install librosa`

# Makefile

- Run `make install` to install dependencies
- Run `make clean` to remove unnecessary files from the repo
- Run `make pre-commit` to run pre-commit hooks
- Run `make reformat` to reformat code to the PEP8 format

# pre-commit hooks

First you should run `pre-commit install` for the pre-commit hooks to be installed. When committing to the repo, pre-commit hooks are automatically triggered. You can run them manually via `make pre-commit`.

# Setup Cyanite API

Follow the tutorial [here](https://api-docs.cyanite.ai/docs/create-integration) on how to create an integration with the Cyanite API.

You have two get the following keys:
- Secret
- Access Token

These two keys should be registered on the config file found in `dalang/config/config.env`.

`PORT` should be set to `8080` and `API_URL` to `https://api.cyanite.ai/graphql`.

To establish a connection with the API run:
`python dalang/apis/proxyport.py`