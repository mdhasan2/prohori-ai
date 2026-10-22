import "@testing-library/jest-dom/vitest"
import { render, screen, within } from "@testing-library/react"
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

    it('clearly identifies demo mode and no backend connection', () => {
        render(<App />)

        const environment = screen.getByRole('region', {
            name: 'Environment',
        })

        expect(within(environment).getByText('demo')).toBeVisible()
        expect(within(environment).getByText('Not connected')).toBeVisible()
        expect(
            screen.getByText('Live backend integration has not been implemented.'),
        ).toBeVisible()
    })
})