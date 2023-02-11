import { assert, expect, test } from "vitest";
import { sanitize_phone } from "@/sanitize_phone";
import { validate_phone } from "@/validate_phone";

test("sanitize_phone", () => {
  expect(sanitize_phone("+375-293827401")).toBe("375293827401");
  expect(sanitize_phone("8 0293827401")).eq("80293827401");
});

test("validate_phone", () => {
  // invalid
  expect(validate_phone("m")).eq(false);
  expect(validate_phone("+375-293827401")).eq(false);
  expect(validate_phone("8 0293827401")).eq(false);
  expect(validate_phone("90293827401")).eq(false);
  expect(validate_phone("368293827401")).eq(false);
  expect(validate_phone("37293827401")).eq(false);
  expect(validate_phone("372293827401")).eq(false);
  expect(validate_phone("m2293827401")).eq(false);
  expect(validate_phone("37529382740x")).eq(false);

  // valid
  expect(validate_phone("80293827401")).eq(true);
  expect(validate_phone("375293827401")).eq(true);
  expect(validate_phone("375443827401")).eq(true);
});
