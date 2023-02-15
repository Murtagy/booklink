export function validate_phone(phone: string): boolean {
  // Belarus only for now!

  for (const ch of phone) {
    // any char not a number
    if (isNaN(Number(ch))) {
      return false;
    }
  }

  // not 8 0xx xxxxxxx
  if (phone.length == 11) {
    if (phone[0] != "8" || phone[1] != "0") {
      return false;
    }
    return true;
    // not 375 xx xxxxxxx
  }
  if (phone.length == 12) {
    const prefix = phone.substring(0, 3);
    if (prefix != "375") {
      return false;
    }
    return true;
  }
  return false;
}
