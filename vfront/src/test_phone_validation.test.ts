
import { assert, expect, test } from 'vitest'
import { sanitize_phone } from '@/sanitize_phone'

test('sanitize_phone', () => {
    expect(sanitize_phone("+375-293827401")).toBe('375293827401')
    expect(sanitize_phone("8 0293827401")).eq('80293827401');
    }
)