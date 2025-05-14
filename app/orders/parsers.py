import re
from uuid import uuid4
from datetime import datetime


class PaymentInfoParser:
    # регистронезависимо найдём слово «АППАРАТ» и цифру
    DEVICE_PATTERN = re.compile(r"АППАРАТ\s+(\d+)", re.IGNORECASE)
    # захватим название до «АППАРАТ»
    PAYMENT_NAME_PATTERN = re.compile(r"^🏪\s*(.+?)\s+АППАРАТ", re.MULTILINE | re.IGNORECASE)
    # сумма, как раньше
    AMOUNT_PATTERN = re.compile(r"💰\s*([\d\s,\.]+)")
    # дата+время
    DATETIME_PATTERN = re.compile(r"⏰\s*(\d{2}\.\d{2}\.\d{4})\s+([\d:]{8})")
    # статус
    STATUS_PATTERN = re.compile(r"✅.*Успешно", re.MULTILINE)
    # настоящий ID из чека
    TX_PATTERN = re.compile(r"🆔\s*(\d+)")

    def __init__(self, text: str):
        self.text = text

    def parse(self) -> dict:
        # device_id
        m_dev = self.DEVICE_PATTERN.search(self.text)
        device_id = int(m_dev.group(1)) if m_dev else None

        # payment_name
        m_name = self.PAYMENT_NAME_PATTERN.search(self.text)
        payment_name = m_name.group(1).strip() if m_name else None

        # amount
        m_amt = self.AMOUNT_PATTERN.search(self.text)
        amount = self._normalize_number(m_amt.group(1)) if m_amt else None

        # datetime
        m_dt = self.DATETIME_PATTERN.search(self.text)
        dt = None
        if m_dt:
            date_str, time_str = m_dt.group(1), m_dt.group(2)
            try:
                dt = datetime.strptime(f"{date_str} {time_str}", '%d.%m.%Y %H:%M:%S')
            except ValueError:
                dt = None

        # статус
        status = bool(self.STATUS_PATTERN.search(self.text))

        # transaction_id — сначала поищем в тексте, иначе UUID
        m_tx = self.TX_PATTERN.search(self.text)
        transaction_id = m_tx.group(1) if m_tx else str(uuid4())

        return {
            'device_id': device_id,
            'payment_name': payment_name,
            'amount': float(amount),
            'datetime': str(dt),
            'status': status,
            'transaction_id': transaction_id
        }

    @staticmethod
    def _normalize_number(s: str) -> float | None:
        s = s.replace(' ', '').replace(',', '.')
        try:
            return float(s)
        except ValueError:
            return None
