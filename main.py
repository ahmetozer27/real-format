import shutil
import psutil
from tqdm import tqdm
import random
import os

# Oluşturulucak Dosyanın İsmi
dir_name = "test"

# Bağlı diskleri ve isimlerini listele
partitions = psutil.disk_partitions()

print("\n\n\n" + "-" * 19 + "Bağlı Diskler" + "-" * 19 + "\n")
for partition in partitions:
    print(f"Disk Adı: {partition.device}, Tür: {partition.fstype}, Nokta: {partition.mountpoint}")

    # Her disk için boş alanı öğren
    total, used, free = shutil.disk_usage(partition.mountpoint)

    # Boş alanı GB, MB, KB olarak ayır
    free_gb = free / (1024 ** 3)  # GB cinsinden
    free_mb = (free % (1024 ** 3)) / (1024 ** 2)  # MB cinsinden
    free_kb = (free % (1024 ** 2)) / 1024  # KB cinsinden

    # Sonuçları yazdır
    print(f"Toplam Boş Alan: {int(free_gb)} GB, {int(free_mb)} MB, {int(free_kb)} KB")
    print("-" * 50)  # Ayrım için çizgi

# Kullanıcıdan onay al
if input("Emin Misin? (Y/N) ").strip().lower() == "n":
    print("Program sonlandırılıyor...")
    exit()

for partition in partitions:
    # Oluşturulacak klasörün yolu
    target_dir = f"{partition.mountpoint}{dir_name}"

    # Klasör oluşturma
    try:
        os.makedirs(target_dir)  # Alt klasörleriyle birlikte oluşturur
        print(f"\n{target_dir} adlı klasör oluşturuldu.\n")
    except FileExistsError:
        print(f"\n{target_dir} adlı klasör zaten mevcut.\n")
    except Exception as e:
        print(f"\nKlasör oluşturulurken hata oluştu: {e}\n")

    try:
        # Kullanıcıdan onay al
        if input(f"{partition.device[0]} adlı diskin temizliği yapılacak Emin Misin? (Y/N) ").strip().lower() == "n":
            continue
        # Diskteki boş alanı öğren
        total, used, free = shutil.disk_usage(target_dir)

        # Rastgele bir sayı oluştur
        random_number = random.randint(100, 9999999999)  # 10 haneli rastgele bir sayı

        filename = f"space_with_zeros - {random_number} $ahmet$"

        # Dosyayı oluştur ve tüm boş alanı sıfırlarla doldur
        try:
            with open(os.path.join(target_dir, filename), "wb") as f:
                block_size = 4 * 1024 * 1024  # 4 MB # Blokların boyutu
                num_blocks = free // block_size  # Toplamda kaç blok olduğu sayısını verir
                remaining_bytes = free % block_size  # Kalan bayt sayısı

                # İlerleme çubuğu ile yazma işlemi
                for _ in tqdm(range(num_blocks), desc="Yazma İlerlemesi", unit="Blok"):
                    try:
                        f.write(b'\x00' * block_size)  # 4 MB sıfır yaz
                    except:
                        print("Blokta yazarken hata oluştu! (Blok bozuk veya erişilemez olabilir)")
                # Kalan alanı doldur (varsa)
                try:
                    if remaining_bytes > 0:
                        f.write(b'\x00' * remaining_bytes)  # Kalan baytları sıfırla

                    # Bittiğini bildir
                    print("\nDiskteki tüm boş alan sıfırlarla dolduruldu.")

                except:
                    #Temzilenemeyen kısmı bildir
                    print(f"\nKalan {remaining_bytes} miktarda bayt temizlenemedi!\n")

        except Exception as e:
            print(f"Hata oluştu: {e}")

        # Klasörü ve içindeki tüm dosyaları sil
        try:
            shutil.rmtree(target_dir)
            print("\nKlasör ve içindeki tüm dosyalar silindi.")
        except Exception as e:
            print(f"Hata oluştu: {e}")
    except:
        print("Hata")


