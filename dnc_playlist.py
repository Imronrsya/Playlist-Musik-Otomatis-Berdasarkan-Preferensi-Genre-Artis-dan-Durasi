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

def dnc_playlist(songs, target_duration, preferred_genres, preferred_artists):
    """Algoritma Divide and Conquer sederhana untuk playlist"""
    
    # Base case: Tidak ada lagu tersisa
    if len(songs) == 0:
        return [], 0, 0
    
    # Base case: Hanya satu lagu
    if len(songs) == 1:
        song = songs.iloc[0]
        score = calculate_preference_score(song, preferred_genres, preferred_artists)
        if song['duration'] <= target_duration:
            return [song], song['duration'], score
        else:
            return [], 0, 0
    
    # DIVIDE: Bagi dataset menjadi 2 bagian
    mid = len(songs) // 2
    left_songs = songs.iloc[:mid].reset_index(drop=True)
    right_songs = songs.iloc[mid:].reset_index(drop=True)
    
    # CONQUER: Selesaikan masing-masing bagian secara rekursif
    left_playlist, left_duration, left_score = dnc_playlist(
        left_songs, target_duration, preferred_genres, preferred_artists
    )
    
    right_playlist, right_duration, right_score = dnc_playlist(
        right_songs, target_duration, preferred_genres, preferred_artists
    )
    
    # COMBINE: Pilih solusi terbaik dari 3 kemungkinan
    # Opsi 1: Ambil hasil kiri saja
    best_playlist = left_playlist
    best_duration = left_duration
    best_score = left_score
    
    # Opsi 2: Ambil hasil kanan saja (jika lebih baik)
    if right_score > best_score:
        best_playlist = right_playlist
        best_duration = right_duration
        best_score = right_score
    
    # Opsi 3: Gabungkan kiri + kanan (jika muat dan lebih baik)
    combined_duration = left_duration + right_duration
    combined_score = left_score + right_score
    
    if (combined_duration <= target_duration and 
        combined_score > best_score and 
        left_playlist and right_playlist):
        best_playlist = left_playlist + right_playlist
        best_duration = combined_duration
        best_score = combined_score
    
    return best_playlist, best_duration, best_score

def run_experiment(dataset_size, target_duration=30):
    """Menjalankan eksperimen algoritma DnC untuk ukuran dataset tertentu"""
    
    # Load dataset musik dan ambil subset sesuai ukuran yang diinginkan
    df = pd.read_csv('dataset.csv')
    df_subset = df.head(dataset_size)
    
    # Definisi preferensi pengguna untuk eksperimen
    preferred_genres = ['Rock', 'Pop']
    preferred_artists = ['Queen', 'Ed Sheeran', 'Michael Jackson']
    
    # Jalankan algoritma DnC dan ukur waktu eksekusi
    start_time = time.time()
    playlist, total_duration, total_score = dnc_playlist(
        df_subset, target_duration, preferred_genres, preferred_artists
    )
    execution_time = time.time() - start_time
    
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
    
    print("PLAYLIST MUSIK OTOMATIS - ALGORITMA DIVIDE AND CONQUER")
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
    ax1.bar(sizes, exec_times, color='mediumpurple')
    ax1.set_title('Execution Time (Divide & Conquer)')
    ax1.set_xlabel('Dataset Size')
    ax1.set_ylabel('Time (ms)')
    
    # Grafik 2: Jumlah Lagu Terpilih
    ax2.bar(sizes, song_counts, color='mediumseagreen')
    ax2.set_title('Jumlah Lagu Terpilih')
    ax2.set_xlabel('Dataset Size')
    ax2.set_ylabel('Jumlah Lagu')
    
    # Grafik 3: Total Durasi Playlist
    ax3.bar(sizes, durations, color='orange')
    ax3.set_title('Total Durasi Playlist')
    ax3.set_xlabel('Dataset Size')
    ax3.set_ylabel('Durasi (menit)')
    
    # Grafik 4: Skor Preferensi Total
    ax4.bar(sizes, scores, color='pink')
    ax4.set_title('Total Skor Preferensi')
    ax4.set_xlabel('Dataset Size')
    ax4.set_ylabel('Skor')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Jalankan program utama
    main()