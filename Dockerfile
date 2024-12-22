FROM archlinux:latest

RUN pacman -Syu --noconfirm

WORKDIR /root

COPY . /root

CMD ["python", "main.py", "--docker"]
