if [ ! -f config/data.toml ]; then
    cp config/data.toml.example config/data.toml
fi
uv sync