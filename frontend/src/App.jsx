import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import useEmblaCarousel from 'embla-carousel-react';
import { 
  ChevronLeft, 
  ChevronRight, 
  RefreshCw, 
  TrendingUp, 
  TrendingDown,
  Minus,
  Loader2,
  Send,
  BarChart3,
  Menu,
  X,
  Trash2,
  Github
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { ThemeProvider, useTheme } from '@/components/ThemeProvider';
import { ThemeToggle } from '@/components/ThemeToggle';
import { cn } from '@/lib/utils';

const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? '/api' : 'http://localhost:5000/api');

function AppContent() {
  const { theme } = useTheme();
  const [reviewText, setReviewText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [recentReview, setRecentReview] = useState(null);
  const [allReviews, setAllReviews] = useState([]);
  const [loadingReviews, setLoadingReviews] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  
  const [emblaRef, emblaApi] = useEmblaCarousel({ 
    loop: true,
    align: 'start',
    slidesToScroll: 1
  });

  useEffect(() => {
    fetchReviews();
  }, []);

  useEffect(() => {
    if (emblaApi && allReviews.length > 0) {
      const autoplay = setInterval(() => {
        if (emblaApi.canScrollNext()) {
          emblaApi.scrollNext();
        } else {
          emblaApi.scrollTo(0);
        }
      }, 5000);

      return () => clearInterval(autoplay);
    }
  }, [emblaApi, allReviews]);

  const fetchReviews = async () => {
    setLoadingReviews(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/reviews`);
      setAllReviews(response.data);
    } catch (err) {
      console.error('Error fetching reviews:', err);
      if (err.code === 'ECONNREFUSED' || err.message?.includes('ECONNREFUSED') || !err.response) {
        setError('Backend tidak berjalan. Silakan jalankan backend dengan: cd backend && python app.py');
      } else {
        const errorMessage = err.response?.data?.error || err.message || 'Gagal memuat review';
        setError(`Gagal memuat review: ${errorMessage}`);
      }
    } finally {
      setLoadingReviews(false);
    }
  };

  const handleDeleteReview = async (reviewId) => {
    setDeletingId(reviewId);
    setError(null);
    try {
      await axios.delete(`${API_BASE_URL}/reviews/${reviewId}`);
      // Remove from state immediately for better UX
      setAllReviews(allReviews.filter(review => review.id !== reviewId));
      // If deleted review was the recent one, clear it
      if (recentReview && recentReview.id === reviewId) {
        setRecentReview(null);
      }
      setDeleteConfirm(null);
    } catch (err) {
      console.error('Error deleting review:', err);
      const errorMessage = err.response?.data?.error || err.message || 'Gagal menghapus review';
      setError(`Gagal menghapus review: ${errorMessage}`);
    } finally {
      setDeletingId(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!reviewText.trim()) {
      setError('Mohon masukkan teks review');
      return;
    }

    setLoading(true);
    setError(null);
    setRecentReview(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/analyze-review`, {
        review_text: reviewText
      });

      setRecentReview(response.data);
      setReviewText('');
      fetchReviews();
    } catch (err) {
      console.error('Error analyzing review:', err);
      if (err.code === 'ECONNREFUSED' || err.message?.includes('ECONNREFUSED') || !err.response) {
        setError('Backend tidak berjalan. Silakan jalankan backend dengan: cd backend && python app.py');
      } else {
        const errorMessage = err.response?.data?.error || err.message || 'Gagal menganalisis review';
        setError(`Gagal menganalisis review: ${errorMessage}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const getSentimentIcon = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive':
        return <TrendingUp className="h-4 w-4 sm:h-5 sm:w-5 text-green-600 dark:text-green-400" />;
      case 'negative':
        return <TrendingDown className="h-4 w-4 sm:h-5 sm:w-5 text-red-600 dark:text-red-400" />;
      default:
        return <Minus className="h-4 w-4 sm:h-5 sm:w-5 text-gray-600 dark:text-gray-400" />;
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive':
        return 'bg-green-50 dark:bg-green-950/30 text-green-700 dark:text-green-400 border-green-200 dark:border-green-800';
      case 'negative':
        return 'bg-red-50 dark:bg-red-950/30 text-red-700 dark:text-red-400 border-red-200 dark:border-red-800';
      default:
        return 'bg-gray-50 dark:bg-gray-900/50 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-800';
    }
  };

  const getSentimentLabel = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive':
        return 'POSITIF';
      case 'negative':
        return 'NEGATIF';
      default:
        return 'NETRAL';
    }
  };

  const scrollPrev = () => emblaApi?.scrollPrev();
  const scrollNext = () => emblaApi?.scrollNext();

  const carouselItems = allReviews.slice(0, 5);

  return (
    <div className="min-h-screen bg-white dark:bg-black text-gray-900 dark:text-gray-100 transition-colors duration-300">
      {/* 3D Animated Background Grid */}
      <div className="fixed inset-0 bg-grid opacity-[0.02] dark:opacity-[0.05] pointer-events-none -z-10" />
      
      {/* Fixed Header */}
      <motion.header 
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="sticky top-0 z-50 bg-white/80 dark:bg-black/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-900 shadow-sm"
      >
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="flex items-center gap-2 sm:gap-3"
            >
              <BarChart3 className="h-5 w-5 sm:h-6 sm:w-6 text-gray-900 dark:text-gray-100" />
              <div className="flex flex-col">
                <h1 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-gray-100 leading-tight">
                  <span className="hidden sm:inline">ReviewInsight</span>
                  <span className="sm:hidden">ReviewInsight</span>
                </h1>
                <p className="text-xs text-gray-600 dark:text-gray-400 hidden sm:block">
                  Analisis Review Produk dengan AI
                </p>
              </div>
            </motion.div>
            
            <div className="flex items-center gap-2 sm:gap-4">
              <ThemeToggle />
              {/* Mobile Menu Button */}
              <Button
                variant="ghost"
                size="icon"
                className="lg:hidden"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                aria-label="Toggle menu"
              >
                {mobileMenuOpen ? (
                  <X className="h-5 w-5" />
                ) : (
                  <Menu className="h-5 w-5" />
                )}
              </Button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {/* Mobile Menu Overlay */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
              onClick={() => setMobileMenuOpen(false)}
            />
          )}
        </AnimatePresence>

        {/* Split Screen Layout: Desktop, Stacked: Mobile */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          {/* Left Side: Carousel (Fixed on Desktop, Scrollable on Mobile) */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="lg:sticky lg:top-24 h-fit order-2 lg:order-1"
          >
            <Card className="bg-white/50 dark:bg-gray-950/50 backdrop-blur-md border border-gray-200 dark:border-gray-900 shadow-lg">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg sm:text-xl text-gray-900 dark:text-gray-100">
                  Review Terbaru
                </CardTitle>
                <CardDescription className="text-sm text-gray-600 dark:text-gray-400">
                  5 review terbaru dengan analisis sentimen
                </CardDescription>
              </CardHeader>
              <CardContent>
                {loadingReviews ? (
                  <div className="space-y-3 sm:space-y-4">
                    {[1, 2, 3].map((i) => (
                      <Skeleton key={i} className="h-20 sm:h-24 w-full rounded-lg" />
                    ))}
                  </div>
                ) : carouselItems.length === 0 ? (
                  <div className="text-center py-8 sm:py-12 text-gray-500 dark:text-gray-400 text-sm sm:text-base">
                    Belum ada review. Analisis review pertama Anda!
                  </div>
                ) : (
                  <div className="relative">
                    <div className="overflow-hidden rounded-lg" ref={emblaRef}>
                      <div className="flex">
                        {carouselItems.map((review) => (
                          <div key={review.id} className="flex-[0_0_100%] min-w-0 px-1">
                            <motion.div
                              initial={{ opacity: 0, scale: 0.95 }}
                              animate={{ opacity: 1, scale: 1 }}
                              transition={{ duration: 0.3 }}
                              className="p-4 sm:p-5 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shadow-sm hover:shadow-md transition-shadow duration-200"
                            >
                              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-3">
                                <div className={cn(
                                  "flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs sm:text-sm font-medium w-fit",
                                  getSentimentColor(review.sentiment)
                                )}>
                                  {getSentimentIcon(review.sentiment)}
                                  <span>{getSentimentLabel(review.sentiment)}</span>
                                  {review.sentiment_score && (
                                    <span className="text-xs opacity-75">
                                      ({(review.sentiment_score * 100).toFixed(1)}%)
                                    </span>
                                  )}
                                </div>
                                <span className="text-xs text-gray-500 dark:text-gray-400">
                                  {review.created_at 
                                    ? new Date(review.created_at).toLocaleDateString('id-ID', {
                                        day: 'numeric',
                                        month: 'short',
                                        year: 'numeric'
                                      })
                                    : 'N/A'}
                                </span>
                              </div>
                              <p className="text-sm sm:text-base text-gray-700 dark:text-gray-300 line-clamp-3 mb-3 leading-relaxed">
                                {review.review_text}
                              </p>
                              {review.key_points && (
                                <details className="mt-2">
                                  <summary className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 cursor-pointer hover:text-gray-900 dark:hover:text-gray-200 transition-colors font-medium">
                                    Poin Penting
                                  </summary>
                                  <pre className="mt-2 text-xs sm:text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap font-sans leading-relaxed">
                                    {review.key_points}
                                  </pre>
                                </details>
                              )}
                            </motion.div>
                          </div>
                        ))}
                      </div>
                    </div>
                    {carouselItems.length > 1 && (
                      <div className="flex justify-center gap-2 mt-4">
                        <Button
                          variant="outline"
                          size="icon"
                          onClick={scrollPrev}
                          className="h-8 w-8 sm:h-9 sm:w-9 border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800"
                          aria-label="Previous slide"
                        >
                          <ChevronLeft className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="icon"
                          onClick={scrollNext}
                          className="h-8 w-8 sm:h-9 sm:w-9 border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800"
                          aria-label="Next slide"
                        >
                          <ChevronRight className="h-4 w-4" />
                        </Button>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          {/* Right Side: Scrollable Content */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="space-y-6 sm:space-y-8 order-1 lg:order-2"
          >
            {/* Input Section */}
            <Card className="bg-white/50 dark:bg-gray-950/50 backdrop-blur-md border border-gray-200 dark:border-gray-900 shadow-lg">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg sm:text-xl text-gray-900 dark:text-gray-100">
                  Analisis Review Baru
                </CardTitle>
                <CardDescription className="text-sm text-gray-600 dark:text-gray-400">
                  Masukkan review produk untuk dianalisis sentimen dan ekstrak poin penting dengan AI
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-5">
                  <div>
                    <label htmlFor="review" className="text-sm sm:text-base font-medium mb-2 block text-gray-900 dark:text-gray-100">
                      Review Produk
                    </label>
                    <textarea
                      id="review"
                      value={reviewText}
                      onChange={(e) => setReviewText(e.target.value)}
                      placeholder="Masukkan review produk Anda di sini..."
                      rows="6"
                      disabled={loading}
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-400 dark:focus:ring-gray-600 focus:ring-offset-2 dark:focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed resize-none transition-all text-sm sm:text-base"
                    />
                  </div>

                  <AnimatePresence>
                    {error && (
                      <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="p-3 sm:p-4 rounded-lg bg-red-50 dark:bg-red-950/30 text-red-700 dark:text-red-400 border border-red-200 dark:border-red-800 text-sm sm:text-base"
                      >
                        {error}
                      </motion.div>
                    )}
                  </AnimatePresence>

                  <Button
                    type="submit"
                    disabled={loading || !reviewText.trim()}
                    className="w-full bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-gray-200 transition-colors h-11 sm:h-12 text-sm sm:text-base font-semibold"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 sm:h-5 sm:w-5 animate-spin" />
                        <span className="hidden sm:inline">Menganalisis...</span>
                        <span className="sm:hidden">Loading...</span>
                      </>
                    ) : (
                      <>
                        <Send className="mr-2 h-4 w-4 sm:h-5 sm:w-5" />
                        Analisis Review
                      </>
                    )}
                  </Button>
                </form>

                {/* Recent Result */}
                <AnimatePresence>
                  {recentReview && (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                      className="mt-6 sm:mt-8"
                    >
                      <Card className="border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900">
                        <CardHeader className="pb-4">
                          <CardTitle className="text-lg sm:text-xl text-gray-900 dark:text-gray-100">
                            Hasil Analisis
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4 sm:space-y-5">
                          <div className={cn(
                            "flex items-center gap-3 sm:gap-4 px-4 sm:px-5 py-3 sm:py-4 rounded-lg border",
                            getSentimentColor(recentReview.sentiment)
                          )}>
                            {getSentimentIcon(recentReview.sentiment)}
                            <div>
                              <div className="font-semibold text-sm sm:text-base">
                                {getSentimentLabel(recentReview.sentiment)}
                              </div>
                              {recentReview.sentiment_score && (
                                <div className="text-xs sm:text-sm opacity-75 mt-1">
                                  Skor: {(recentReview.sentiment_score * 100).toFixed(1)}%
                                </div>
                              )}
                            </div>
                          </div>

                          {recentReview.key_points && (
                            <div>
                              <h4 className="text-sm sm:text-base font-semibold mb-2 sm:mb-3 text-gray-900 dark:text-gray-100">
                                Poin Penting:
                              </h4>
                              <div className="p-4 sm:p-5 rounded-lg bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800">
                                <pre className="text-sm sm:text-base text-gray-700 dark:text-gray-300 whitespace-pre-wrap font-sans leading-relaxed">
                                  {recentReview.key_points}
                                </pre>
                              </div>
                            </div>
                          )}
                        </CardContent>
                      </Card>
                    </motion.div>
                  )}
                </AnimatePresence>
              </CardContent>
            </Card>

            {/* All Reviews Section */}
            <Card className="bg-white/50 dark:bg-gray-950/50 backdrop-blur-md border border-gray-200 dark:border-gray-900 shadow-lg">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-6 pb-4 gap-4">
                <div>
                  <CardTitle className="text-lg sm:text-xl text-gray-900 dark:text-gray-100">
                    Semua Review
                  </CardTitle>
                  <CardDescription className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                    Total {allReviews.length} review
                  </CardDescription>
                </div>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={fetchReviews}
                  disabled={loadingReviews}
                  className="border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800 self-start sm:self-auto"
                  aria-label="Refresh reviews"
                >
                  <RefreshCw className={cn(
                    "h-4 w-4 sm:h-5 sm:w-5",
                    loadingReviews && "animate-spin"
                  )} />
                </Button>
              </div>
              <CardContent>
                {loadingReviews ? (
                  <div className="space-y-4 sm:space-y-5">
                    {[1, 2, 3].map((i) => (
                      <Skeleton key={i} className="h-32 sm:h-40 w-full rounded-lg" />
                    ))}
                  </div>
                ) : allReviews.length === 0 ? (
                  <div className="text-center py-12 sm:py-16 text-gray-500 dark:text-gray-400 text-sm sm:text-base">
                    Belum ada review. Analisis review pertama Anda!
                  </div>
                ) : (
                  <div className="space-y-4 sm:space-y-5 max-h-[600px] sm:max-h-[700px] overflow-y-auto pr-2">
                    <AnimatePresence>
                      {allReviews.map((review, index) => (
                        <motion.div
                          key={review.id}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.05, duration: 0.3 }}
                          whileHover={{ scale: 1.01 }}
                          className="p-4 sm:p-5 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shadow-sm hover:shadow-md hover:border-gray-300 dark:hover:border-gray-700 transition-all duration-200"
                        >
                          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-3">
                            <div className={cn(
                              "flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs sm:text-sm font-medium w-fit",
                              getSentimentColor(review.sentiment)
                            )}>
                              {getSentimentIcon(review.sentiment)}
                              <span>{getSentimentLabel(review.sentiment)}</span>
                              {review.sentiment_score && (
                                <span className="text-xs opacity-75">
                                  ({(review.sentiment_score * 100).toFixed(1)}%)
                                </span>
                              )}
                            </div>
                            <div className="flex items-center gap-2 sm:gap-3">
                              <span className="text-xs sm:text-sm text-gray-500 dark:text-gray-400">
                                {review.created_at 
                                  ? new Date(review.created_at).toLocaleString('id-ID', {
                                      year: 'numeric',
                                      month: 'short',
                                      day: 'numeric',
                                      hour: '2-digit',
                                      minute: '2-digit'
                                    })
                                  : 'Tidak tersedia'}
                              </span>
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => setDeleteConfirm(review.id)}
                                disabled={deletingId === review.id}
                                className="h-7 w-7 sm:h-8 sm:w-8 text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 hover:bg-red-50 dark:hover:bg-red-950/30"
                                aria-label="Hapus review"
                              >
                                {deletingId === review.id ? (
                                  <Loader2 className="h-3 w-3 sm:h-4 sm:w-4 animate-spin" />
                                ) : (
                                  <Trash2 className="h-3 w-3 sm:h-4 sm:w-4" />
                                )}
                              </Button>
                            </div>
                          </div>
                          <p className="text-sm sm:text-base text-gray-700 dark:text-gray-300 mb-3 sm:mb-4 whitespace-pre-wrap leading-relaxed">
                            {review.review_text}
                          </p>
                          {review.key_points && (
                            <details className="mt-3">
                              <summary className="text-sm sm:text-base font-medium text-gray-600 dark:text-gray-400 cursor-pointer hover:text-gray-900 dark:hover:text-gray-200 transition-colors">
                                Poin Penting
                              </summary>
                              <div className="mt-3 p-3 sm:p-4 rounded-lg bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800">
                                <pre className="text-sm sm:text-base text-gray-700 dark:text-gray-300 whitespace-pre-wrap font-sans leading-relaxed">
                                  {review.key_points}
                                </pre>
                              </div>
                            </details>
                          )}
                        </motion.div>
                      ))}
                    </AnimatePresence>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>

      {/* Delete Confirmation Dialog */}
      <AnimatePresence>
        {deleteConfirm && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setDeleteConfirm(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 shadow-xl max-w-md w-full p-6"
            >
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
                Hapus Review?
              </h3>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 mb-6">
                Apakah Anda yakin ingin menghapus review ini? Tindakan ini tidak dapat dibatalkan.
              </p>
              <div className="flex gap-3 justify-end">
                <Button
                  variant="outline"
                  onClick={() => setDeleteConfirm(null)}
                  className="border-gray-300 dark:border-gray-700"
                >
                  Batal
                </Button>
                <Button
                  onClick={() => handleDeleteReview(deleteConfirm)}
                  disabled={deletingId === deleteConfirm}
                  className="bg-red-600 dark:bg-red-700 text-white hover:bg-red-700 dark:hover:bg-red-800"
                >
                  {deletingId === deleteConfirm ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Menghapus...
                    </>
                  ) : (
                    <>
                      <Trash2 className="mr-2 h-4 w-4" />
                      Hapus
                    </>
                  )}
                </Button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Footer with GitHub Credit */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="mt-12 sm:mt-16 py-6 sm:py-8 border-t border-gray-200 dark:border-gray-900"
      >
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-sm text-gray-600 dark:text-gray-400 text-center sm:text-left">
              © 2025 Review Analyzer. Dibuat dengan ❤️
            </p>
            <a
              href="https://github.com/MarioSitepu"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors group"
            >
              <Github className="h-4 w-4 sm:h-5 sm:w-5 group-hover:scale-110 transition-transform" />
              <span className="font-medium">MarioSitepu</span>
            </a>
          </div>
        </div>
      </motion.footer>
    </div>
  );
}

function App() {
  return (
    <ThemeProvider defaultTheme="dark">
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
