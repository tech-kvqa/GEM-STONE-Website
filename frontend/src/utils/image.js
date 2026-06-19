// const BACKEND_URL = 'https://gem-stone-website.onrender.com'

// export const getImageUrl = (path) => {
//   if (!path) return ''

//   // Already full URL
//   if (path.startsWith('http')) {
//     return path
//   }

//   return `${BACKEND_URL}${path}`
// }


const BACKEND_URL = 'https://gem-stone-website.onrender.com'

export const getImageUrl = (path) => {
  if (!path) return ''

  if (typeof path === 'object') {
    path =
      path.url ||
      path.image_url ||
      path.path ||
      path.src ||
      ''
  }

  if (typeof path !== 'string') {
    return ''
  }

  if (path.startsWith('http')) {
    return path
  }

  return `${BACKEND_URL}${path}`
}