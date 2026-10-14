def count_spells(n: int) -> int:
  # Inisialisasi counter dengan 0
  counter = 0

  # Loop sampai n menjadi satu digit
  while len(str(n)) > 1:
    # Tambahkan counter
    counter += 1

    # Inisialisasi variabel sum dengan 0
    sum = 0

    # Loop untuk menambahkan semua digit dari n
    for char in str(n):
      sum += int(char)

    # Atur n menjadi hasil penjumlahan digit-digit n
    n = sum

  # Kembalikan counter
  return counter


# Cetak hasil pemanggilan fungsi count_spells
print(count_spells(991))