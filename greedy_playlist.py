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

def greedy_playlist(songs, target_duration, preferred_genres, preferred_artists):
    """Algoritma Greedy untuk membuat playlist optimal berdasarkan efisiensi"""
    playlist = []
    total_duration = 0
    
    # Hitung skor dan efisiensi untuk setiap lagu
    song_data = []
    for _, song in songs.iterrows():
        score = calculate_preference_score(song, preferred_genres, preferred_artists)
        # Greedy choice: efisiensi = skor per menit
        efficiency = score / song['duration'] if song['duration'] > 0 else 0
        song_data.append((song, score, efficiency))
    
    # Sort berdasarkan efisiensi tertinggi (greedy choice)
    song_data.sort(key=lambda x: -x[2])  # Sort by efficiency descending
    
    # Pilih lagu secara greedy berdasarkan efisiensi
    for song, score, efficiency in song_data:
        if total_duration + song['duration'] <= target_duration:
            playlist.append(song)
            total_duration += song['duration']
    
    return playlist, total_duration

def run_experiment(dataset_size, target_duration=30):
    """Menjalankan eksperimen algoritma Greedy untuk ukuran dataset tertentu"""
    
    # Load dataset musik dan ambil subset sesuai ukuran yang diinginkan
    df = pd.read_csv('dataset.csv')
    df_subset = df.head(dataset_size)
    
    # Definisi preferensi pengguna untuk eksperimen
    preferred_genres = ['Rock', 'Pop']
    preferred_artists = ['Queen', 'Ed Sheeran', 'Michael Jackson']
    
    # Jalankan algoritma Greedy dan ukur waktu eksekusi
    start_time = time.time()
    playlist, total_duration = greedy_playlist(df_subset, target_duration, preferred_genres, preferred_artists)
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
    
    print("PLAYLIST MUSIK OTOMATIS - ALGORITMA GREEDY")
    print("=" * 50)
    
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
    ax1.bar(sizes, exec_times, color='skyblue')
    ax1.set_title('Execution Time (Greedy Algorithm)')
    ax1.set_xlabel('Dataset Size')
    ax1.set_ylabel('Time (ms)')
    
    # Grafik 2: Jumlah Lagu Terpilih
    ax2.bar(sizes, song_counts, color='lightgreen')
    ax2.set_title('Jumlah Lagu Terpilih')
    ax2.set_xlabel('Dataset Size')
    ax2.set_ylabel('Jumlah Lagu')
    
    # Grafik 3: Total Durasi Playlist
    ax3.bar(sizes, durations, color='salmon')
    ax3.set_title('Total Durasi Playlist')
    ax3.set_xlabel('Dataset Size')
    ax3.set_ylabel('Durasi (menit)')
    
    # Grafik 4: Skor Preferensi Total
    ax4.bar(sizes, scores, color='gold')
    ax4.set_title('Total Skor Preferensi')
    ax4.set_xlabel('Dataset Size')
    ax4.set_ylabel('Skor')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Jalankan program utama
    main()