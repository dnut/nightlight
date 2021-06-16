if [ "$EUID" -eq 0 ]; then
    echo 'Do not run as root'
    exit 1
fi

sudo cp nightlight.py /usr/local/bin/nightlight
sudo chmod +x /usr/local/bin/nightlight
sudo cp nightlight.service /etc/systemd/user/nightlight.service
systemctl --user daemon-reload
systemctl --user enable nightlight
systemctl --user restart nightlight
