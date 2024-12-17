#!/bin/bash

# Переменные: замените на свои значения
DISK="/dev/sdX"     # Диск для установки
ROOT_PART="/dev/sdX3" # Раздел root
SWAP_PART="/dev/sdX2" # Раздел swap
EFI_PART="/dev/sdX1"  # Раздел EFI
HOSTNAME="myhostname" # Имя хоста
USERNAME="myuser"     # Имя пользователя

# Форматирование разделов
mkfs.fat -F 32 $EFI_PART
mkfs.ext4 $ROOT_PART
mkswap $SWAP_PART
swapon $SWAP_PART

# Монтирование разделов
mount $ROOT_PART /mnt
mount --mkdir $EFI_PART /mnt/boot/efi

# Установка базовой системы
pacstrap /mnt base base-devel linux linux-headers linux-firmware

# Генерация fstab
genfstab -U /mnt >> /mnt/etc/fstab

# Настройка системы в chroot
arch-chroot /mnt bash -c "\
  # Установка загрузчика и необходимых пакетов
  pacman -S --noconfirm grub efibootmgr networkmanager amd-ucode btrfs-progs vim

  # Установка GRUB
  grub-install $DISK
  grub-mkconfig -o /boot/grub/grub.cfg

  # Настройка локали
  sed -i 's/^#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
  locale-gen
  echo \"LANG=en_US.UTF-8\" > /etc/locale.conf

  # Настройка имени хоста
  echo $HOSTNAME > /etc/hostname
  cat <<EOF > /etc/hosts
127.0.0.1    localhost
::1          localhost
127.0.0.1    ${HOSTNAME}.localdomain $HOSTNAME
EOF

  # Включение multilib-репозитория
  sed -i 's/^#\[multilib\]/\[multilib\]/' /etc/pacman.conf
  sed -i '/\[multilib\]/,+1 s/^#//' /etc/pacman.conf
  pacman -Sy

  # Настройка sudo
  chmod u+w /etc/sudoers
  sed -i 's/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers
  chmod u-w /etc/sudoers

  # Создание пользователя
  useradd -m -G wheel $USERNAME
  echo \"Set root password:\"
  passwd
  echo \"Set password for $USERNAME:\"
  passwd $USERNAME

  # Включение NetworkManager
  systemctl enable NetworkManager
"

# Завершение установки
umount -R /mnt
echo "Установка завершена. Перезагрузите систему."
reboot
