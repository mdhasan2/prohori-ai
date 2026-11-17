export type Theme = 'light' | 'dark'

const STORAGE_KEY = 'prohori:theme'

export function readTheme(): Theme {
    try {
        const saved = localStorage.getItem(STORAGE_KEY)

        if (saved === 'light' || saved === 'dark') {
            return saved
        }
    } catch {
        return 'dark'
    }

    return 'dark'
}

export function saveTheme(theme: Theme): boolean {
    try {
        localStorage.setItem(STORAGE_KEY, theme)
        return true
    } catch {
        return false
    }
}