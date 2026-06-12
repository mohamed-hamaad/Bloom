/** @type {import('tailwindcss').Config} */
module.exports = {
content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/*.py',
],
theme: {
extend: {
    colors: {
        cream: 'var(--color-cream)',
        dark: 'var(--color-dark)',
        rose: 'var(--color-rose)',
        'rose-light': 'var(--color-rose-light)',
        sage: 'var(--color-sage)',
        gold: 'var(--color-gold)',
        muted: 'var(--color-muted)',
    },
    fontFamily: {
    display: ['Cormorant Garamond', 'serif'],
    sans: ['DM Sans', 'sans-serif'],
    },
},
},
plugins: [],
}