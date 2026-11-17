import { StrictMode } from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import {
    afterEach,
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from 'vitest'
import OperatorShell from './OperatorShell'

beforeEach(() => {
    localStorage.clear()
})

afterEach(() => {
    vi.restoreAllMocks()
})

function renderShell() {
    return render(
        <StrictMode>
            <OperatorShell
                connection="Connected"
                accessMode="local_only"
                identityMode="unconfigured"
                healthError=""
            >
                <p>Existing console content</p>
            </OperatorShell>
        </StrictMode>
    )
}

function shellElement() {
    return screen.getByRole('main').closest('.operator-shell')
}

describe('OperatorShell theme preference', () => {
    it('defaults to dark when no preference is stored', () => {
        renderShell()

        expect(shellElement()).toHaveAttribute('data-theme', 'dark')
        expect(
            screen.getByRole('button', {
                name: 'Switch to light theme',
            }),
        ).toBeVisible()
    })

    it.each(['light', 'dark'] as const)(
        'restores the saved %s preference',
        (theme) => {
            localStorage.setItem('prohori:theme', theme)

            renderShell()

            expect(shellElement()).toHaveAttribute('data-theme', theme)
        },
    )

    it('ignores an unsupported stored value', () => {
        localStorage.setItem('prohori:theme', 'authenticated')

        renderShell()

        expect(shellElement()).toHaveAttribute('data-theme', 'dark')
        expect(
            screen.getByText('Operator identity: not configured.'),
        ).toBeInTheDocument()
    })

    it('remains usable when reading storage fails', () => {
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
            throw new DOMException('Storage blocked', 'SecurityError')
        })

        renderShell()

        expect(shellElement()).toHaveAttribute('data-theme', 'dark')
        expect(
            screen.getByText('Existing console content'),
        ).toBeInTheDocument()
    })

    it('changes theme and reports a persistence failure', () => {
        vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
            throw new DOMException('Storage blocked', 'SecurityError')
        })

        renderShell()

        fireEvent.click(
            screen.getByRole('button', {
                name: 'Switch to light theme',
            }),
        )

        expect(shellElement()).toHaveAttribute('data-theme', 'light')
        expect(
            screen.getByText(
                'Theme changed for this session. Your browser could not save the preference.',
            ),
        ).toBeInTheDocument()

        expect(
            screen.getByText('Operator identity: not configured.'),
        ).toBeInTheDocument()
    })
})