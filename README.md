# 動画

![](/images/2022-07-05-21-50-50.png)

- github リポジトリ
  - [gwenf/python-polls](https://github.com/gwenf/python-polls)

# docker run だけでやろうとする 🙅
## Python の仮想環境作成

```bash
docker run -it --rm --name python -v $(pwd):/app --workdir /app python:3.9.0 python -mvenv venv
```

## Python の仮想環境有効化

docker run する限り、毎回有効化コマンドを最初にコンテナ上で実行して、&& のあとに python スクリプト実行のコマンド書いたりする

```bash
docker run -it --rm --name python -v $(pwd):/app --workdir /app python:3.9.0 bash -c  "source venv/bin/activate"
```

## fastapi インストール

```bash
docker run -it --rm --name python -v $(pwd):/app --workdir /app python:3.9.0 bash -c  "source venv/bin/activate && pip install fastapi"
```

## uvicorn インストール

```bash
docker run -it --rm --name python -v $(pwd):/app --workdir /app python:3.9.0 bash -c  "source venv/bin/activate && pip install uvicorn"
```

## uvicorn のサーバー起動

- docker の -p で 8000 をポートフォワーディングする
- uvicorn の --host を 0.0.0.0 にする

```bash
docker run -it --rm --name python -v $(pwd):/app -p 8000:8000 --workdir /app python:3.9.0 bash -c  "source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0"
```

# docker run だけだと 限界・・・なので Dockerfile を使う 🙅

## build

```bash
docker build -t python-polls-fast-api --build-arg work_dir=/app .
```

## poetry init

poetry の初期化、パッケージのインストールは手動 👨‍💻

```
❯ docker run -it --rm --name python -v $(pwd):/app python-polls-fast-api poetry init --name python-polls -n

This command will guide you through creating your pyproject.toml config.


You can specify a package in the following forms:
  - A single name (requests)
  - A name and a constraint (requests@^2.23.0)
  - A git url (git+https://github.com/python-poetry/poetry.git)
  - A git url with a revision (git+https://github.com/python-poetry/poetry.git#develop)
  - A file path (../my-package/my-package.whl)
  - A directory (../my-package/)
  - A url (https://example.com/packages/my-package-0.1.0.tar.gz)
```

## poetry add fastapi uvicorn

```
❯ docker run -it --rm --name python -v $(pwd):/app python-polls-fast-api poetry add fastapi uvicorn
Creating virtualenv python-polls in /app/.venv
Using version ^0.78.0 for fastapi
Using version ^0.18.2 for uvicorn

Updating dependencies
Resolving dependencies... (3.0s)

Writing lock file

Package operations: 10 installs, 0 updates, 0 removals

  • Installing idna (3.3)
  • Installing sniffio (1.2.0)
  • Installing anyio (3.6.1)
  • Installing typing-extensions (4.3.0)
  • Installing click (8.1.3)
  • Installing h11 (0.13.0)
  • Installing pydantic (1.9.1)
  • Installing starlette (0.19.1)
  • Installing fastapi (0.78.0)
  • Installing uvicorn (0.18.2)

```

> Creating virtualenv python-polls in /app/.venv
- Dockerfile で poetry がプロジェクトルートに python の仮想環境を作るように設定しているため、`/app/.venv` ディレクトリが作られる
  - `venv` ディレクトリも作られる
  - `.vscode` ディレクトリも作られる
    - 仮想環境用の python の場所が記述されているっぽい

## poetry shell & run the uvicorn server

```
docker run -it --rm --name python -v $(pwd):/app -p 8000:8000 python-polls-fast-api bash
```

bash に入ったら、

```
poetry shell
```
```
uvicorn main:app --reload --host 0.0.0.0
```

# 最終的には 💯
- docker-compose.yml を使った
- python 環境の web.Dockerfile を作った
  - pyton イメージに poetry をインストール、依存パッケージをインストールするようにした
- 参考担った stack overflow
  - [Integrating Python Poetry with Docker - Stack Overflow](https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker)

# TODO

- [x] multi-stage build する
  - [Use multi-stage builds | Docker Documentation](https://docs.docker.com/develop/develop-images/multistage-build/)
  - [Document docker poetry best practices · Discussion #1879 · python-poetry/poetry](https://github.com/python-poetry/poetry/discussions/1879)
    - 実際に multi-stage build で Dockerfile 書いている人たちの poetry スレッド
  - ヒント⚠️
    - poetry shell や、virtualenv の activate が実際にやっていることは、python のライブラリがある場所を $PATH に追加しているだけ
    - [Elegantly activating a virtualenv in a Dockerfile](https://pythonspeed.com/articles/activate-virtualenv-dockerfile/)
  - multi-stage build しなくても良かった
    - poetry の virtualenv を作らない設定にして、poetry install するだけ