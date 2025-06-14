import pandas as pd
import time
import matplotlib.pyplot as plt

def calculate_preference_score(song, preferred_genres, preferred_artists):
    """Menghitung skor preferensi berdasarkan genre dan artis favorit"""
    score = 0
    if song['genre'] in preferred_genres:
        score += 1  # +1 untuk genre yang disukai
    if song['artist'] in preferred_artists:
        score += 1  # +1 untuk artis yang disukai
    return score

def dp_playlist(songs, target_duration, preferred_genres, preferred_artists):
    """Algoritma Dynamic Programming untuk membuat playlist optimal (0/1 Knapsack)"""
    n = len(songs)
    # Konversi durasi ke integer (dikali 10 untuk presisi 1 desimal)
    capacity = int(target_duration * 10)
    
    # Siapkan data lagu dengan skor preferensi
    song_data = []
    for _, song in songs.iterrows():
        score = calculate_preference_score(song, preferred_genres, preferred_artists)
        duration = int(song['duration'] * 10)
        song_data.append((song, score, duration))
    
    # Inisialisasi DP table: dp[i][w] = maksimum skor dengan i lagu pertama dan kapasitas w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Isi DP table dengan bottom-up approach
    for i in range(1, n + 1):
        song, score, duration = song_data[i-1]
        for w in range(capacity + 1):
            # Pilihan 1: Tidak ambil lagu ke-i
            dp[i][w] = dp[i-1][w]
            # Pilihan 2: Ambil lagu ke-i (jika muat)
            if duration <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-duration] + score)
    
    # Backtrack untuk mendapatkan lagu yang dipilih
    playlist = []
    w = capacity
    total_duration = 0
    
    for i in range(n, 0, -1):
        # Jika nilai berbeda, berarti lagu ke-i dipilih
        if dp[i][w] != dp[i-1][w]:
            song, score, duration = song_data[i-1]
            playlist.append(song)
            total_duration += song['duration']
            w -= duration
    
    return playlist, total_duration

def run_experiment(dataset_size, target_duration=30):
    """Menjalankan eksperimen algoritma DP untuk ukuran dataset tertentu"""
    
    # Load dataset musik dan ambil subset sesuai ukuran yang diinginkan
    df = pd.read_csv('dataset.csv')
    df_subset = df.head(dataset_size)
    
    # Definisi preferensi pengguna untuk eksperimen
    preferred_genres = ['Rock', 'Pop']
    preferred_artists = ['Queen', 'Ed Sheeran', 'Michael Jackson']
    
    # Jalankan algoritma DP dan ukur waktu eksekusi
    start_time = time.time()
    playlist, total_duration = dp_playlist(df_subset, target_duration, preferred_genres, preferred_artists)
    execution_time = time.time() - start_time
    
    # Hitung total skor preferensi
    total_score = sum(calculate_preference_score(song, preferred_genres, preferred_artists) for song in playlist)
    
    # Kembalikan hasil eksperimen dalam bentuk dictionary
    return {
        'dataset_size': dataset_size,
        'execution_time': execution_time * 1000,  # konversi ke milisekon
        'song_count': len(playlist),
        'total_duration': total_duration,
        'preference_score': total_score,
        'selected_songs': playlist
    }

def main():
    """Fungsi utama untuk menjalankan semua eksperimen dan menampilkan hasil"""
    
    # Ukuran dataset yang akan diuji (10, 20, 30 lagu)
    dataset_sizes = [10, 20, 30]
    results = []
    
    print("PLAYLIST MUSIK OTOMATIS - ALGORITMA DYNAMIC PROGRAMMING")
    print("=" * 55)
    
    # Jalankan eksperimen untuk setiap ukuran dataset
    for size in dataset_sizes:
        result = run_experiment(size)
        results.append(result)
        
        # Tampilkan hasil eksperimen
        print(f"\nDATASET UKURAN: {result['dataset_size']} lagu")
        print(f"Execution Time: {result['execution_time']:.2f} ms")
        print(f"Jumlah Lagu Terpilih: {result['song_count']}")
        print(f"Total Durasi: {result['total_duration']:.1f} menit")
        print(f"Total Skor Preferensi: {result['preference_score']}")
        
        print("\nLagu yang Terpilih:")
        for i, song in enumerate(result['selected_songs'], 1):
            print(f"{i}. {song['title']} - {song['artist']} ({song['genre']}, {song['duration']}m)")
    
    # Buat grafik perbandingan hasil eksperimen
    create_comparison_chart(results)

def create_comparison_chart(results):
    """Membuat grafik perbandingan hasil eksperimen untuk visualisasi"""    
    # Ekstrak data untuk visualisasi
    sizes = [r['dataset_size'] for r in results]
    exec_times = [r['execution_time'] for r in results]
    song_counts = [r['song_count'] for r in results]
    durations = [r['total_duration'] for r in results]
    scores = [r['preference_score'] for r in results]
    
    # Buat subplot 2x2 untuk 4 grafik
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    
    # Grafik 1: Waktu Eksekusi
    ax1.bar(sizes, exec_times, color='lightcoral')
    ax1.set_title('Execution Time (Dynamic Programming)')
    ax1.set_xlabel('Dataset Size')
    ax1.set_ylabel('Time (ms)')
    
    # Grafik 2: Jumlah Lagu Terpilih
    ax2.bar(sizes, song_counts, color='lightblue')
    ax2.set_title('Jumlah Lagu Terpilih')
    ax2.set_xlabel('Dataset Size')
    ax2.set_ylabel('Jumlah Lagu')
    
    # Grafik 3: Total Durasi Playlist
    ax3.bar(sizes, durations, color='lightgreen')
    ax3.set_title('Total Durasi Playlist')
    ax3.set_xlabel('Dataset Size')
    ax3.set_ylabel('Durasi (menit)')
    
    # Grafik 4: Skor Preferensi Total
    ax4.bar(sizes, scores, color='lightyellow')
    ax4.set_title('Total Skor Preferensi')
    ax4.set_xlabel('Dataset Size')
    ax4.set_ylabel('Skor')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Jalankan program utama
    main()