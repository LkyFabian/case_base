import math
import random

# ============================================================
# KONFIGURASI PARAMETER GA
# ============================================================
POP_SIZE    = 50        # Ukuran populasi
N_BITS      = 16        # Bit per variabel
CHROM_LEN   = 32        # Total bit kromosom (x1=16 bit, x2=16 bit)
X_MIN, X_MAX = -10, 10  # Domain
P_C         = 0.8       # Probabilitas crossover
P_M         = 0.01      # Probabilitas mutasi per bit
MAX_GEN     = 500       # Maksimum generasi
ELITISM     = 1         # Jumlah elite yang dipertahankan
TOURN_SIZE  = 3         # Ukuran tournament selection

# ============================================================
# FUNGSI OBJEKTIF (yang akan diminimumkan)
# ============================================================
def f(x1, x2):
    try:
        tan_val = math.tan(x1 + x2)
        exp_val = math.exp(1 - math.sqrt(x2 ** 2))
        result  = -(math.sin(x1) * math.cos(x2) * tan_val + 0.5 * exp_val)
    except (OverflowError, ValueError):
        result = float('inf')  # Penalti jika tidak terdefinisi
    return result

# ============================================================
# 1. INISIALISASI POPULASI
# ============================================================
def init_population():
    """Buat populasi awal secara acak (list of list of bit)."""
    population = []
    for _ in range(POP_SIZE):
        chrom = [random.randint(0, 1) for _ in range(CHROM_LEN)]
        population.append(chrom)
    return population

# ============================================================
# 2. DEKODE KROMOSOM
# ============================================================
def decode(chrom):
    """
    Dekode kromosom biner ke (x1, x2).
    16 bit pertama -> x1, 16 bit berikutnya -> x2.
    Rumus: x = x_min + (decimal / (2^16 - 1)) * (x_max - x_min)
    """
    bits_x1 = chrom[:N_BITS]
    bits_x2 = chrom[N_BITS:]

    dec_x1 = sum(b * (2 ** (N_BITS - 1 - i)) for i, b in enumerate(bits_x1))
    dec_x2 = sum(b * (2 ** (N_BITS - 1 - i)) for i, b in enumerate(bits_x2))

    max_val = (2 ** N_BITS) - 1
    x1 = X_MIN + (dec_x1 / max_val) * (X_MAX - X_MIN)
    x2 = X_MIN + (dec_x2 / max_val) * (X_MAX - X_MIN)
    return x1, x2

# ============================================================
# 3. PERHITUNGAN FITNESS
# ============================================================
def fitness(chrom):
    """
    Fitness untuk minimisasi: semakin kecil f, semakin baik.
    Dikembalikan sebagai nilai negatif agar bisa dipakai 'max fitness'.
    """
    x1, x2 = decode(chrom)
    return -f(x1, x2)   # negasi: fitness tinggi = f kecil

def evaluate_population(population):
    """Hitung fitness semua individu, return list nilai fitness."""
    return [fitness(chrom) for chrom in population]

# ============================================================
# 4. PEMILIHAN ORANGTUA — Tournament Selection
# ============================================================
def tournament_select(population, fitnesses):
    """Pilih 1 orangtua via tournament selection."""
    candidates = random.sample(range(len(population)), TOURN_SIZE)
    best = max(candidates, key=lambda idx: fitnesses[idx])
    return population[best][:]   # copy kromosom terpilih

# ============================================================
# 5. CROSSOVER — Single-Point Crossover
# ============================================================
def crossover(parent1, parent2):
    """
    Single-point crossover dengan probabilitas P_C.
    Jika tidak terjadi crossover, kembalikan salinan orangtua.
    """
    if random.random() < P_C:
        point    = random.randint(1, CHROM_LEN - 1)
        child1   = parent1[:point] + parent2[point:]
        child2   = parent2[:point] + parent1[point:]
    else:
        child1, child2 = parent1[:], parent2[:]
    return child1, child2

# ============================================================
# 6. MUTASI — Bit-Flip Mutation
# ============================================================
def mutate(chrom):
    """Balik setiap bit dengan probabilitas P_M."""
    for i in range(CHROM_LEN):
        if random.random() < P_M:
            chrom[i] = 1 - chrom[i]
    return chrom

# ============================================================
# 7. PERGANTIAN GENERASI — Elitisme
# ============================================================
def next_generation(population, fitnesses):
    """
    Buat generasi baru:
    - Pertahankan ELITISM individu terbaik (elitisme)
    - Sisa slot diisi offspring dari crossover + mutasi
    """
    # Urutkan berdasarkan fitness (descending)
    sorted_idx  = sorted(range(POP_SIZE), key=lambda i: fitnesses[i], reverse=True)
    elite       = [population[i][:] for i in sorted_idx[:ELITISM]]

    new_pop = elite[:]
    while len(new_pop) < POP_SIZE:
        p1 = tournament_select(population, fitnesses)
        p2 = tournament_select(population, fitnesses)
        c1, c2 = crossover(p1, p2)
        c1 = mutate(c1)
        c2 = mutate(c2)
        new_pop.append(c1)
        if len(new_pop) < POP_SIZE:
            new_pop.append(c2)

    return new_pop

# ============================================================
# MAIN — Jalankan GA
# ============================================================
def run_ga():
    random.seed(42)  # Untuk reproduktibilitas hasil

    # Inisialisasi
    population = init_population()
    best_chrom  = None
    best_fit    = float('-inf')
    best_gen    = 0

    print("=" * 55)
    print("  Algoritma Genetika — Minimisasi f(x1, x2)")
    print("=" * 55)
    print(f"  Pop Size : {POP_SIZE}  |  Max Gen : {MAX_GEN}")
    print(f"  Pc={P_C}  |  Pm={P_M}  |  Bits/var={N_BITS}")
    print("=" * 55)

    for gen in range(1, MAX_GEN + 1):
        fitnesses = evaluate_population(population)

        # Cari individu terbaik generasi ini
        gen_best_idx = max(range(POP_SIZE), key=lambda i: fitnesses[i])
        gen_best_fit = fitnesses[gen_best_idx]

        if gen_best_fit > best_fit:
            best_fit   = gen_best_fit
            best_chrom = population[gen_best_idx][:]
            best_gen   = gen

        # Cetak progres setiap 50 generasi
        if gen % 50 == 0 or gen == 1:
            x1, x2 = decode(best_chrom)
            print(f"  Gen {gen:>4} | Best f(x1,x2) = {-best_fit:>10.6f} "
                  f"| x1={x1:>7.4f}, x2={x2:>7.4f}")

        # Pergantian generasi
        population = next_generation(population, fitnesses)

    # ---- HASIL AKHIR ----
    x1_best, x2_best = decode(best_chrom)
    f_best = f(x1_best, x2_best)

    print("=" * 55)
    print("  HASIL AKHIR")
    print("=" * 55)
    print(f"  Ditemukan pada generasi : {best_gen}")
    print(f"  Kromosom terbaik        : {''.join(map(str, best_chrom))}")
    print(f"  x1                      : {x1_best:.6f}")
    print(f"  x2                      : {x2_best:.6f}")
    print(f"  Nilai minimum f(x1,x2)  : {f_best:.6f}")
    print("=" * 55)

    return best_chrom, x1_best, x2_best, f_best

if __name__ == "__main__":
    run_ga()