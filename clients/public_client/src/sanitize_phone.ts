export function sanitize_phone(phone: string): string {
  // input
  phone = phone.trim();
  phone = phone.replace("-", "");
  phone = phone.replace("+", "");
  phone = phone.replace(" ", "");
  return phone;
}
