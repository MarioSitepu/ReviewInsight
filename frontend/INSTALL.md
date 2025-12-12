# Instalasi Dependencies Modern

## Langkah Instalasi

Setelah upgrade ke design system modern, Anda perlu menginstall semua dependencies baru:

```powershell
cd frontend
npm install
```

Ini akan menginstall:
- **Tailwind CSS 4** - Utility-first CSS framework
- **Framer Motion** - Animasi library
- **Radix UI** - Komponen aksesibel
- **Embla Carousel** - Carousel library
- **Lucide React** - Icon library
- Dan banyak lagi...

## Fitur Baru

### ✨ Design System
- **Tailwind CSS 4** dengan custom theme
- **Dark mode** dengan transisi halus
- **Glassmorphism** effects
- **Responsive design** untuk semua device

### 🎨 Layout
- **Split-screen**: Carousel kiri (fixed), konten kanan (scrollable)
- **Fixed header** dengan navigasi
- **Mobile-friendly** dengan grid adaptif

### 🎭 Animasi
- **Framer Motion** untuk smooth animations
- **Hover effects** pada cards
- **Carousel autoplay** dengan navigasi
- **Transisi halus** antar halaman

### 🎯 UX Improvements
- **Loading states** dengan skeleton
- **Visual feedback** pada interaksi
- **Kontras teks** baik untuk aksesibilitas
- **Smooth scroll** animations

## Troubleshooting

### Error: Module not found
Jika ada error module not found, jalankan:
```powershell
npm install
```

### Error: Tailwind CSS
Pastikan PostCSS sudah terinstall:
```powershell
npm install -D postcss autoprefixer
```

### Error: Path alias @
Pastikan `jsconfig.json` sudah ada dan `vite.config.js` sudah dikonfigurasi dengan path alias.

## Catatan

- Semua styling menggunakan **Tailwind CSS** (tidak ada CSS file terpisah)
- Dark mode bisa di-toggle dengan tombol di header
- Carousel otomatis berputar setiap 5 detik
- Layout responsif untuk mobile, tablet, dan desktop

