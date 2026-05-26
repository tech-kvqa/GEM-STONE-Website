const BACKEND_URL = 'https://gem-stone-website.onrender.com'

export const getImageUrl = (path) => {
  if (!path) return ''

  // Already full URL
  if (path.startsWith('http')) {
    return path
  }

  return `${BACKEND_URL}${path}`
}