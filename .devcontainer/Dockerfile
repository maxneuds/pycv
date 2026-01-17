FROM debian:trixie

ARG PYTHON_VERSION
ARG DOCKER_GID
ARG UID
ARG GID
ENV STARSHIP_PRESET=gruvbox-rainbow
ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    DEBIAN_FRONTEND=noninteractive
# Devcontainer variables
ENV USERNAME=dev
ENV WORKSPACE=/workspace

# --------------------------------------------------------------------------
# 🛠️ BASE SYSTEM & USER SETUP
# --------------------------------------------------------------------------

# Setup container user, groups and workspace
RUN groupadd -g ${GID} ${USERNAME} && \
    useradd -m -u ${UID} -g ${GID} ${USERNAME} && \
    mkdir ${WORKSPACE} && chown ${USERNAME}:${USERNAME} /workspace
# Update packages and generate locales
RUN apt-get update && \
    apt-get install -y locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# ### ⚡ PYTHON ENVIRONMENT (uv)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
# Tell uv where to store its cache and managed pythons
ENV UV_CACHE_DIR=${WORKSPACE}/.cache/uv \
    UV_PYTHON_INSTALL_DIR=${WORKSPACE}/.python-versions \
    # Add our future venv to PATH immediately
    PATH="${WORKSPACE}/.venv/bin:$PATH"
RUN apt-get install -y \
    # Python Build Dependencies (Required to compile Python from source)
    build-essential libffi-dev libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev libncursesw5-dev xz-utils \
    tk-dev libxml2-dev libxmlsec1-dev liblzma-dev

# ### ⚡ Project Specifics
RUN apt-get install -y \
    weasyprint

# --------------------------------------------------------------------------
# 🛠️ SYSTEM TOOLS (Docker Devcontainer)
# --------------------------------------------------------------------------

# Install devcontainer tools, setup sudo and shell
RUN apt-get install -y \
    sudo \
    git wget curl unzip fontconfig rsync htop fastfetch vim neovim zsh \
    apt-transport-https ca-certificates gnupg lsb-release && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers && \
    chsh -s /bin/zsh ${USERNAME}

# Install Nerd Fonts (Hasklig & FiraCode)
# Requires 'fontconfig' and 'unzip' to be installed in the apt-get step above
RUN mkdir -p /usr/local/share/fonts && \
    # Download FiraCode
    wget https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraCode.zip -O /tmp/FiraCode.zip && \
    unzip -o /tmp/FiraCode.zip -d /usr/local/share/fonts && \
    # Download Hasklig
    wget https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Hasklig.zip -O /tmp/Hasklig.zip && \
    unzip -o /tmp/Hasklig.zip -d /usr/local/share/fonts && \
    # Cleanup & Cache
    rm /tmp/FiraCode.zip /tmp/Hasklig.zip && \
    fc-cache -fv

# Install Starship (Modern Prompt)
RUN curl -fsSL https://starship.rs/install.sh | sh -s -- -y

# Install Docker & set permissions
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    (groupadd -g ${DOCKER_GID} docker || groupmod -g ${DOCKER_GID} docker) && \
    apt-get install -y \
    docker-ce docker-ce-cli containerd.io && \
    usermod -aG docker ${USERNAME}
# Cleanup apt cache
RUN rm -rf /var/lib/apt/lists/*


# --------------------------------------------------------------------------
# 💻 USER CONFIGURATION (ZSH & PYTHON)
# --------------------------------------------------------------------------

USER ${USERNAME}
WORKDIR ${WORKSPACE}

# Install Oh-My-Zsh & Plugins
RUN sh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)" "" --unattended && \
    git clone https://github.com/zsh-users/zsh-completions ~/.oh-my-zsh/custom/plugins/zsh-completions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions

# Configure Zsh + Starship
RUN mkdir -p /home/${USERNAME}/.config && \
    # Configure Starship
    starship preset ${STARSHIP_PRESET} -o /home/${USERNAME}/.config/starship.toml && \
    # Configure Neovim
    mkdir -p /home/${USERNAME}/.config/nvim && \
    echo 'set number' >> /home/${USERNAME}/.config/nvim/init.vim && \
    echo 'set relativenumber' >> /home/${USERNAME}/.config/nvim/init.vim && \
    # Configure .zshrc
    sed -i 's/plugins=(git)/plugins=(git zsh-completions zsh-syntax-highlighting zsh-autosuggestions)/' ~/.zshrc && \
    sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME=""/' ~/.zshrc && \
    echo 'eval "$(starship init zsh)"' >> ~/.zshrc && \
    # Custom alias
    echo 'alias ll="ls -lah --color=auto"' >> ~/.zshrc && \
    echo 'alias cp="rsync -avh --progress"' >> ~/.zshrc \
    echo 'alias vim="nvim"' >> ~/.zshrc && \
    echo 'alias vi="nvim"' >> ~/.zshrc

# Switch user
USER ${USERNAME}
WORKDIR ${WORKSPACE}

# Install uv, python kernel and register it for tools
RUN uv python install ${PYTHON_VERSION}

# Entrypoint
CMD ["/bin/zsh"]
