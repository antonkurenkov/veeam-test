# Дан файл, содержащий текстовую строку – указание пути к дисковому устройству в системе
# Linux. Прочитайте файл и выведите на экран (stdout) следующую информацию о дисковом
# устройстве:
# -- Тип устройства, например: disk, part, lvm, rom;
# -- Общий объем в гигабайтах;
# -- В тех случаях, когда имеет смысл (например, если путь – это раздел диска), выведите
# также:
# -- Объём свободного пространства в мегабайтах;
# -- Тип файловой системы, например: ext4, swap;
# -- Точку монтирования.
# На Linux-системе, где будет исполняться код, установлены пакеты coreutils и util-linux.

# Пример 1:
# Входной файл:
# /dev/sda
# Вывод:
# /dev/sda disk 64G

# Пример 2:
# Входной файл:
# /dev/sda1
# Вывод:
# /dev/sda1 part 1G 238M ext2 /boot


DRIVE=$(head -n 1 input.txt)

DRIVETYPE=`lsblk $DRIVE --output=type | head -n 2 | tail -n 1`
DRIVESIZE=`df -BG $DRIVE --output=size | head -n 2 | tail -n 1`

if [ $DRIVETYPE = "part" ]
then
	DRIVEDETAILS=`df $DRIVE -BM --output=used,fstype,target | tail -n 1`
else
	DRIVEDETAILS=``
fi

echo $DRIVE $DRIVETYPE $DRIVESIZE $DRIVEDETAILS