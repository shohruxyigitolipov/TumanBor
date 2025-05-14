import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta

from app.devices.device_models import Order
from app.devices.device_service import get_logger

logger = get_logger(__name__)


async def get_orders_excel(period):
    today = datetime.today().date()

    date_ranges = {
        "day": (today, today),
        "week": (today - timedelta(days=today.weekday()), today),
        "month": (today.replace(day=1), today),
        "all": (None, None)
    }

    if period not in date_ranges:
        logger.info('wrong_period')
        return None

    start_date, end_date = date_ranges[period]

    orders = 'Order table'
    if not orders:
        logger.info('no_data')
        return None

    data = [
        {
            "Название оплаты": order.payment_name,
            "ID устройства": order.device_id,
            "Сумма": order.amount,
            "Дата": order.date,
            "Время": order.time,
            "Статус платежа": "✅ Подтверждён" if order.status else "❌ Не подтверждён",
            "Лог": order.log,
            "Создано": order.created_at
        } for order in orders
    ]

    df = pd.DataFrame(data)

    total_orders = len(orders)
    confirmed_orders = sum(order.status for order in orders)
    total_amount = sum(order.amount for order in orders if order.amount)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Заказы', index=False)
        worksheet = writer.sheets['Заказы']

        formats = {
            'bold_format': writer.book.add_format({'bold': True, 'align': 'center'}),
            'money_format': writer.book.add_format({'num_format': '#,##0.00'}),
            'date_format': writer.book.add_format({'num_format': 'yyyy-mm-dd'}),
            'time_format': writer.book.add_format({'num_format': 'hh:mm:ss'}),
            'status_format_confirmed': writer.book.add_format({'bold': True, 'font_color': 'green'}),
            'status_format_pending': writer.book.add_format({'bold': True, 'font_color': 'red'})
        }

        worksheet.set_row(0, None, formats['bold_format'])
        worksheet.set_column('A:A', 20)  # Название оплаты
        worksheet.set_column('B:B', 12)  # ID устройства
        worksheet.set_column('C:C', 10, formats['money_format'])  # Сумма
        worksheet.set_column('D:D', 12, formats['date_format'])  # Дата
        worksheet.set_column('E:E', 10, formats['time_format'])  # Время
        worksheet.set_column('F:F', 15)  # Статус
        worksheet.set_column('G:G', 40)  # Лог
        worksheet.set_column('H:H', 18, formats['date_format'])  # Создано

        for row_num, status in enumerate(df['Статус платежа'], start=1):
            fmt = formats['status_format_confirmed'] if "Подтверждён" in status else formats['status_format_pending']
            worksheet.write(row_num, 5, status, fmt)

        summary_data = {
            "Всего заказов": [total_orders],
            "Подтверждённые заказы": [confirmed_orders],
            "Общая сумма": [total_amount]
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Итог', index=False)

        summary_ws = writer.sheets['Итог']
        summary_ws.set_row(0, None, formats['bold_format'])
        summary_ws.set_column('B:B', 10, formats['money_format'])  # Общая сумма

    output.seek(0)
    excel = BufferedInputFile(output.getvalue(), filename=f"{period}_orders.xlsx")
    return excel

