import "@testing-library/jest-dom/vitest"
import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"
import App from "./App"

describe('Security Control Center foundation', () => {
    it('provides an accessible page identity', () => {
        render(<App />)

        expect(screen.getByRole('main')).toBeInTheDocument()
        expect(
            screen.getByRole('heading', {
                level: 1,
                name: 'Security Control Center',
            }),
        ).toBeInTheDocument()
    })
})