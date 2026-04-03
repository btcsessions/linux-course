#!/usr/bin/env fish
# CachyCLI — Install alias, desktop entry, and systemd service

set script_dir (dirname (status filename))

echo "Installing CachyCLI shortcuts..."

# 1. Fish alias
if not grep -q 'alias learn=' ~/.config/fish/config.fish 2>/dev/null
    echo '' >> ~/.config/fish/config.fish
    echo '# CachyCLI shortcut' >> ~/.config/fish/config.fish
    echo 'alias learn="xdg-open http://localhost:8080"' >> ~/.config/fish/config.fish
    echo "  [+] Added 'learn' alias to fish config"
else
    echo "  [=] 'learn' alias already exists"
end

# 2. Desktop entry
cp "$script_dir/cachycli.desktop" ~/.local/share/applications/cachycli.desktop
echo "  [+] Installed desktop entry (find CachyCLI in your app launcher)"

# 3. Systemd user service
mkdir -p ~/.config/systemd/user
cp "$script_dir/cachycli.service" ~/.config/systemd/user/cachycli.service
systemctl --user daemon-reload
systemctl --user enable --now cachycli.service
echo "  [+] Enabled systemd service (CachyCLI starts on login)"

echo ""
echo "Done! You can now:"
echo "  - Type 'learn' in your terminal to open CachyCLI"
echo "  - Find 'CachyCLI' in your app launcher"
echo "  - CachyCLI web UI runs automatically at http://localhost:8080"
echo ""
echo "Reload your shell to use the alias: exec fish"
